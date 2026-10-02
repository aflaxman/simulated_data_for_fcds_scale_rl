"""Build the released cohorts: registry stand-in plus two finder files.

Heavy pipeline tier — the build entry point, ported from the working
notebook ``2026_02_11b_duckdb_psp_reproducible_randomness.ipynb``,
redesigned 2026-09-24 (v0.3) and bumped to v0.4 on 2026-10-01, when pseudopeople's
row duplication was switched off and the data dictionary joined the archive:

* the registry stand-in is drawn from the *last-seen pool*: every simulant ever
  recorded in Florida in the configured censuses (2020, 2030, 2040), once, at
  their last appearance, so like a real registry it holds people who have
  since died or left the state; the finder files are residents of
  ``cohorts.finder_year`` (2040);
* the registry's age/sex distribution is that of the cases FCDS reports
  (``paths.age_sex_target``, the table's ``count`` column as shares): each
  age/sex stratum contributes an exact quota, drawn by keyed hash within the
  stratum, instead of the weighted random draw of the 2026-08-12 build, which
  compressed the weight ratios at a high sampling fraction;
* the exact-target trim is ``stratified_trim`` (``src/``), which hits every
  design target exactly and makes the finder files disjoint — v0.2's
  unstratified trim overshot the overlap targets by roughly a third;
* ``race_ethnicity`` is carried into the released schema, and each registry
  record carries a ``diagnosis_date``: a day drawn uniformly within the record's
  census year by keyed hash (``seeds.diagnosis_date``), so age at diagnosis is
  within a year of the age the FCDS target was matched on (dates therefore
  heap on the census years);
* checksums (MD5 and SHA-256), a release manifest, realised error rates, a
  population summary, the age/sex/race composition and top first names of
  each file (from the source's true ages), and environment info are written
  to ``results/``.

Every stochastic step is a pure function of the seeds in ``config.yaml``; run
the script twice and compare checksums for the run-twice identity test.

Run on a compute node, never a login/dev node (``sbatch --wrap``, not ``srun``
from inside an interactive allocation):

    sbatch --mem=120G -c 8 --wrap "uv run python pipeline/build_cohorts.py"

The version comes from ``--version`` (default: the current one) and must match
``dataset.version`` and ``paths.release_dir`` in ``config.yaml``, which the light
scripts read. ``--force`` rebuilds a version in place. Either way, re-run
``pipeline/linkage_baseline.py`` and re-render the paper once afterwards.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import resource
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import duckdb
import numpy as np
import pandas as pd
import pseudopeople as psp
import yaml

from simulated_data_for_fcds_scale_rl.age_sex_weights import allocate_by_share, load_age_sex_targets
from simulated_data_for_fcds_scale_rl.diagnosis_date import diagnosis_dates
from simulated_data_for_fcds_scale_rl.downsample import stratified_trim
from simulated_data_for_fcds_scale_rl.ssn_noise import apply_targeted_ssn_noise

ROOT = Path(__file__).resolve().parent.parent

# Order matters: this is the published column order (simulant_id is the index).
# race_ethnicity is new in v0.3 — FCDS's own submission layout carries race.
RELEASE_COLUMNS = [
    "first_name", "middle_initial", "last_name", "date_of_birth", "sex",
    "race_ethnicity",
    "street_number", "street_name", "unit_number", "city", "state", "zipcode",
    "ssn",
]
ADDRESS_FIELDS = ["street_number", "street_name", "unit_number", "city", "state", "zipcode"]
RELEASE_FILES = ["registry.csv", "finder_500k.csv", "finder_100k.csv"]
# Documentation shipped inside the archive beside the data files (copied verbatim).
DATA_DICTIONARY = ROOT / "reference" / "data_dictionary.csv"
DOC_FILES = ["data_dictionary.csv"]
# The registry alone carries a diagnosis date; a finder file is a cohort roster.
REGISTRY_EXTRA_COLUMNS = ["diagnosis_date"]

# Official 2020 Census count for Florida (cited literal; see OUTLINE.md for
# the pending Census Bureau citekey).
FL_CENSUS_2020 = 21_538_187


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def find_parquet_source(root: Path, possible_names: list[str]) -> str:
    if root.is_file():
        return str(root)
    for name in possible_names:
        candidate = root / name
        if candidate.exists():
            return str(candidate / "*.parquet")
    raise FileNotFoundError(f"Could not find any of {possible_names} in {root}")


def create_source_views(con: duckdb.DuckDBPyConnection, cfg: dict) -> None:
    """Florida census rows for the configured census years (one per simulant per year) and the raw SSN view."""
    root_path = Path(cfg["paths"]["psp_source"])
    census_glob = find_parquet_source(root_path, ["decennial_census", "decennial_census_observer"])
    ssn_glob = find_parquet_source(root_path, ["social_security", "social_security_observer"])
    state = cfg["cohorts"]["state"]
    years = ", ".join(str(int(y)) for y in cfg["cohorts"]["census_years"])
    con.execute(f"""
        CREATE OR REPLACE VIEW census_fl AS
        SELECT * FROM read_parquet('{census_glob}')
        WHERE state = '{state}' AND year IN ({years})
        QUALIFY row_number() OVER (PARTITION BY simulant_id, year ORDER BY age) = 1
    """)
    con.execute(f"CREATE OR REPLACE VIEW raw_ssn AS SELECT simulant_id, ssn FROM read_parquet('{ssn_glob}')")


def build_pools(con: duckdb.DuckDBPyConnection, cfg: dict) -> dict:
    """The two sampling pools, as small id tables derived from ``census_fl`` in one scan.

    ``pool_registry`` is the last-seen pool: every simulant ever recorded in
    Florida, once, at their latest census, with the columns the stratified draw
    and the QA need. ``pool_finder`` is the residents of ``finder_year``. Staging
    later re-reads the full rows from parquet for the chosen ids. Returns the
    pool sizes and the per-census counts.
    """
    c = cfg["cohorts"]
    if c.get("registry_pool", "last_seen") != "last_seen":
        raise SystemExit("only cohorts.registry_pool: last_seen is implemented")
    finder_year = int(c["finder_year"])
    log("Reading the Florida census rows (all configured years)...")
    con.execute("""
        CREATE OR REPLACE TABLE census_small AS
        SELECT simulant_id, year, sex, age, race_ethnicity FROM census_fl
    """)
    con.execute("""
        CREATE OR REPLACE TABLE pool_registry AS
        SELECT * FROM census_small
        QUALIFY row_number() OVER (PARTITION BY simulant_id ORDER BY year DESC) = 1
    """)
    con.execute(f"CREATE OR REPLACE TABLE pool_finder AS SELECT * FROM census_small WHERE year = {finder_year}")
    sizes = {
        "pool_registry": con.execute("SELECT count(*) FROM pool_registry").fetchone()[0],
        "pool_finder": con.execute("SELECT count(*) FROM pool_finder").fetchone()[0],
        "by_year": {int(y): int(n) for y, n in
                    con.execute("SELECT year, count(*) FROM census_small GROUP BY year ORDER BY year").fetchall()},
    }
    con.execute("DROP TABLE census_small")
    if sizes["pool_registry"] == 0 or sizes["pool_finder"] == 0:
        raise SystemExit(f"CRITICAL: empty pool for state='{c['state']}'; check paths.psp_source and cohorts.census_years.")
    log(f"Florida: {sizes['pool_registry']:,} simulants ever recorded (last-seen pool); "
        f"{sizes['pool_finder']:,} residents in {finder_year}; per census: "
        + ", ".join(f"{y}: {n:,}" for y, n in sizes["by_year"].items()))
    return sizes


def load_targets(con: duckdb.DuckDBPyConnection, cfg: dict) -> pd.DataFrame:
    """Per-stratum registry quotas: target age/sex shares × the oversampled registry target, capped by the pool.

    Maps every ``pool_registry`` simulant to its (sex, age bin) stratum in
    ``strata`` and registers the quota table as ``quotas``. Simulants whose sex
    is not Male/Female or whose age falls outside the bins cannot enter the
    registry and are counted in the log. Returns the quota table.
    """
    targets = load_age_sex_targets(ROOT / cfg["paths"]["age_sex_target"])
    con.register("bins", targets)
    con.execute("""
        CREATE OR REPLACE TABLE strata AS
        SELECT p.simulant_id, p.year, p.sex, b.age_start
        FROM pool_registry p
        JOIN bins b ON p.sex = b.sex AND p.age >= b.age_start AND p.age < b.age_end
    """)
    n_pool, n_strata = con.execute(
        "SELECT (SELECT count(*) FROM pool_registry), (SELECT count(*) FROM strata)").fetchone()
    if n_strata == 0:
        raise SystemExit("CRITICAL: no simulant matched an age/sex stratum; check the sex coding and age units.")
    if n_strata < n_pool:
        log(f"{n_pool - n_strata:,} of {n_pool:,} pool simulants have no age/sex stratum and cannot enter the registry.")
    avail = con.execute("SELECT sex, age_start, count(*) AS available FROM strata GROUP BY ALL").df()
    q = targets.merge(avail, on=["sex", "age_start"], how="left").fillna({"available": 0})
    q["available"] = q["available"].astype(int)
    idx = pd.MultiIndex.from_frame(q[["sex", "age_start"]])
    n_sample = int(cfg["cohorts"]["registry_target"] * cfg["cohorts"]["oversample"])
    quota = allocate_by_share(pd.Series(q["share"].to_numpy(), index=idx), n_sample,
                              pd.Series(q["available"].to_numpy(), index=idx))
    q["quota"] = quota.to_numpy()
    q["take"] = q["quota"] / q["available"].where(q["available"] > 0, 1)
    capped = q[q["quota"] >= q["available"]]
    if len(capped):
        log("WARNING: strata capped at their pool size, so the age/sex target is not met there: "
            + ", ".join(f"{r.sex} {r.age_start}" for r in capped.itertuples()))
    top = q.loc[q["take"].idxmax()]
    log(f"Registry draw: {n_sample:,} simulants across {len(q)} age/sex strata; the largest share of any "
        f"stratum taken is {top['take']:.2f} ({top['sex']} {top['age_start']}).")
    con.register("quotas", q[["sex", "age_start", "quota"]])
    return q


def sample_oversized_cohorts(con: duckdb.DuckDBPyConnection, cfg: dict) -> None:
    """Oversampled cohort ID tables: the registry by exact stratum quotas, the finders by keyed-hash draws.

    We intentionally avoid DuckDB's built-in random() so results are
    reproducible across threads and runs: every draw is a pure function of
    (simulant_id, salt, seed) via md5_number_lower(). Within each age/sex
    stratum the registry takes the ``quota`` simulants with the smallest hash.
    Finder overlap members are registry members present in the finder year
    (their last-seen record *is* that year's record); finder filler comes from
    the finder-year residents outside the registry cohort. Each id table
    carries the census ``year`` of the record to stage.
    """
    c = cfg["cohorts"]
    seed = cfg["seeds"]["duckdb_sample"]
    oversample = c["oversample"]
    finder_year = int(c["finder_year"])
    n1a_sample = int(c["finder_500k_target"] * oversample)
    n1b_sample = int(c["finder_100k_target"] * oversample)
    overlap_a_sample = int(c["overlap_500k_target"] * oversample)
    overlap_b_sample = int(c["overlap_100k_target"] * oversample)

    log(f"Sampling oversized cohorts ({oversample}x): stratified registry, then finders...")
    con.execute(f"""
        CREATE OR REPLACE TABLE df_2_ids AS
        SELECT simulant_id, year FROM (
            SELECT s.simulant_id, s.year, s.sex, s.age_start,
                   row_number() OVER (
                       PARTITION BY s.sex, s.age_start
                       ORDER BY md5_number_lower(CAST(s.simulant_id AS VARCHAR) || ':df2_stratified:{seed}')
                   ) AS rn
            FROM strata s
        ) x
        JOIN quotas q ON x.sex = q.sex AND x.age_start = q.age_start
        WHERE x.rn <= q.quota
    """)
    n_reg, n_reg_fy = con.execute(
        f"SELECT count(*), count(*) FILTER (WHERE year = {finder_year}) FROM df_2_ids").fetchone()
    log(f"Registry cohort: {n_reg:,} simulants, {n_reg_fy:,} of them residents in {finder_year} "
        f"(the overlap candidates).")
    if n_reg_fy < overlap_a_sample + overlap_b_sample:
        raise SystemExit("CRITICAL: too few registry members in the finder year to supply the overlaps.")

    for table, overlap_salt, rest_salt, overlap_n, total_n in [
        ("df_1a_ids", "df1a_overlap", "df1a_rest", overlap_a_sample, n1a_sample),
        ("df_1b_ids", "df1b_overlap", "df1b_rest", overlap_b_sample, n1b_sample),
    ]:
        con.execute(f"""
            CREATE OR REPLACE TABLE {table} AS
            SELECT * FROM (
                SELECT simulant_id, year
                FROM df_2_ids
                WHERE year = {finder_year}
                ORDER BY md5_number_lower(CAST(simulant_id AS VARCHAR) || ':{overlap_salt}:{seed}')
                LIMIT {overlap_n}
            )
            UNION ALL
            SELECT * FROM (
                SELECT p.simulant_id, p.year
                FROM pool_finder p
                WHERE p.simulant_id NOT IN (SELECT simulant_id FROM df_2_ids)
                ORDER BY md5_number_lower(CAST(p.simulant_id AS VARCHAR) || ':{rest_salt}:{seed}')
                LIMIT {total_n - overlap_n}
            )
        """)


def stage_for_psp(con: duckdb.DuckDBPyConnection, table_name: str, dataset_name: str,
                  scratch: Path, changelog_src: Path | None) -> str:
    """Stage a cohort as a parquet directory pseudopeople can consume.

    The staged parquet MUST be written ORDER BY simulant_id: pseudopeople
    walks rows in file order, so an unpinned row order silently changes which
    rows the (seeded, deterministic) noise lands on.
    """
    root_out = scratch / dataset_name
    target_dir = root_out / "decennial_census"
    target_dir.mkdir(parents=True, exist_ok=True)
    if changelog_src is not None and changelog_src.exists():
        shutil.copy(changelog_src, root_out / "CHANGELOG.rst")

    log(f"Staging {dataset_name} to {target_dir}...")
    con.execute(f"""
        COPY (
            SELECT c.* FROM census_fl c
            JOIN {table_name} t ON c.simulant_id = t.simulant_id AND c.year = t.year
            ORDER BY c.simulant_id, c.year
        ) TO '{target_dir}/decennial_census_observer.parquet' (FORMAT PARQUET)
    """)
    return str(root_out)


def noise_config(addr_missing: float, duplicate_with_guardian: float) -> dict:
    """pseudopeople configuration for one file: address blanking at the file's rate, and
    the duplicate-with-guardian row probability (0 means exactly one row per person)."""
    return {
        "decennial_census": {
            "row_noise": {
                "duplicate_with_guardian": {
                    "row_probability_in_households_under_18": duplicate_with_guardian,
                    "row_probability_in_college_group_quarters_under_24": duplicate_with_guardian,
                }
            },
            "column_noise": {
                field: {"leave_blank": {"cell_probability": addr_missing}}
                for field in ADDRESS_FIELDS
            }
        }
    }


def attach_noised_ssn(con: duckdb.DuckDBPyConnection, df_census: pd.DataFrame,
                      *, missing_target_rate: float, transposed_rate: float,
                      seed: int, label: str) -> tuple[pd.DataFrame, dict]:
    """Join clean SSNs from the Social Security observer, then noise them.

    ORDER BY simulant_id pins the row order so the numpy draws land on the
    same people every run.
    """
    ids_to_fetch = pd.DataFrame({"simulant_id": df_census.simulant_id.unique()})
    con.register("request_ids", ids_to_fetch)
    ssn_df = con.execute("""
        SELECT t.simulant_id, s.ssn
        FROM request_ids t
        LEFT JOIN raw_ssn s ON t.simulant_id = s.simulant_id
        QUALIFY row_number() OVER (PARTITION BY t.simulant_id ORDER BY s.ssn) = 1
        ORDER BY t.simulant_id
    """).df()
    con.unregister("request_ids")

    rng = np.random.default_rng(seed)
    ssn_df["ssn"], stats = apply_targeted_ssn_noise(
        ssn_df["ssn"],
        missing_target_rate=missing_target_rate,
        transposed_rate=transposed_rate,
        rng=rng,
    )
    if stats["structural_exceeds_target"]:
        log(f"WARNING [{label}]: structural SSN missingness "
            f"{stats['structural_missing'] / stats['n']:.2%} already exceeds the "
            f"{missing_target_rate:.0%} target; nothing further blanked "
            f"(realised {stats['realised_missing_rate']:.2%}).")

    if "ssn" in df_census.columns:
        df_census = df_census.drop(columns=["ssn"])
    return df_census.merge(ssn_df, on="simulant_id", how="left"), stats


def age_label(start: int, end: int) -> str:
    return f"{start}+" if end >= 200 else f"{start}\u2013{end - 1}"


def write_age_sex_qa(con: duckdb.DuckDBPyConnection, frames: dict, targets: pd.DataFrame,
                     results_dir: Path) -> dict:
    """Composition of each released file by sex, age bin and race/ethnicity, and its top first names.

    Sex, age and race/ethnicity are the source's (true) values at the record's
    census year, joined back by simulant_id, so the binning is exact; first
    names are as released (noise included). Writes ``registry_age_sex.csv``,
    ``registry_top_names.csv`` and ``age_sex_qa.json`` (rows by census year and,
    for the registry, the largest deviation of a realised stratum share from
    its target, in percentage points). Returns the QA dict.
    """
    con.register("bins_qa", targets[["sex", "age_start", "age_end", "share"]])
    counts, names, qa = [], [], {}
    for fname, frame in frames.items():
        pool = "pool_registry" if fname == "registry.csv" else "pool_finder"
        con.register("released", frame.reset_index()[["simulant_id", "first_name"]])
        con.execute(f"""
            CREATE OR REPLACE TABLE qa_rows AS
            SELECT r.simulant_id, r.first_name, p.sex, p.year, coalesce(p.race_ethnicity, 'Unknown') AS race_ethnicity,
                   b.age_start, b.age_end
            FROM released r
            JOIN {pool} p ON r.simulant_id = p.simulant_id
            LEFT JOIN bins_qa b ON p.sex = b.sex AND p.age >= b.age_start AND p.age < b.age_end
        """)
        cnt = con.execute("""
            SELECT sex, age_start, age_end, race_ethnicity, count(*) AS count FROM qa_rows
            WHERE age_start IS NOT NULL GROUP BY ALL ORDER BY sex, age_start, race_ethnicity
        """).df()
        cnt["age_group"] = [age_label(a, b) for a, b in zip(cnt["age_start"], cnt["age_end"])]
        cnt.insert(0, "file", fname)
        counts.append(cnt[["file", "sex", "age_group", "age_start", "race_ethnicity", "count"]])
        top = con.execute("""
            SELECT * FROM (
                SELECT sex, age_start, age_end, first_name, count(*) AS count FROM qa_rows
                WHERE age_start IS NOT NULL AND first_name IS NOT NULL AND first_name <> ''
                GROUP BY sex, age_start, age_end, first_name
            )
            QUALIFY row_number() OVER (PARTITION BY sex, age_start ORDER BY count DESC, first_name) <= 3
            ORDER BY sex, age_start, count DESC
        """).df()
        top["age_group"] = [age_label(a, b) for a, b in zip(top["age_start"], top["age_end"])]
        top["rank"] = top.groupby(["sex", "age_start"]).cumcount() + 1
        top.insert(0, "file", fname)
        names.append(top[["file", "sex", "age_group", "age_start", "first_name", "count", "rank"]])
        by_year = dict(con.execute("SELECT year, count(*) FROM qa_rows GROUP BY year ORDER BY year").fetchall())
        entry = {"rows": int(len(frame)), "rows_binned": int(cnt["count"].sum()),
                 "rows_by_census_year": {str(int(y)): int(n) for y, n in by_year.items()}}
        if fname == "registry.csv":
            realised = cnt.groupby(["sex", "age_start"])["count"].sum()
            realised = realised / realised.sum()
            tgt = targets.set_index(["sex", "age_start"])["share"]
            dev = (realised.reindex(tgt.index).fillna(0) - tgt) * 100
            entry["max_abs_share_deviation_pct"] = float(dev.abs().max())
            entry["max_abs_share_deviation_stratum"] = " ".join(str(x) for x in dev.abs().idxmax())
        qa[fname] = entry
        con.unregister("released")
    pd.concat(counts).to_csv(results_dir / "registry_age_sex.csv", index=False)
    pd.concat(names).to_csv(results_dir / "registry_top_names.csv", index=False)
    (results_dir / "age_sex_qa.json").write_text(json.dumps(qa, indent=2) + "\n")
    return qa


def prep_for_save(df: pd.DataFrame, extra: list[str] | None = None) -> pd.DataFrame:
    columns = RELEASE_COLUMNS + list(extra or [])
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise SystemExit(f"Release columns missing from generated data: {missing}")
    out = df.set_index("simulant_id").filter(columns)
    # Stable sort: duplicated simulants (pseudopeople row-duplication noise)
    # keep a deterministic relative order.
    return out.sort_index(kind="stable")


def checksums(path: Path) -> dict:
    md5, sha256 = hashlib.md5(), hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            md5.update(chunk)
            sha256.update(chunk)
    return {"size_bytes": path.stat().st_size, "md5": md5.hexdigest(), "sha256": sha256.hexdigest()}


def write_deterministic_zip(zip_path: Path, release_dir: Path, arc_prefix: str) -> None:
    """Fixed timestamps and permissions so archive metadata is identical across runs."""
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
        for fname in sorted(RELEASE_FILES + DOC_FILES):
            zi = ZipInfo(f"{arc_prefix}/{fname}", date_time=(2020, 1, 1, 0, 0, 0))
            zi.compress_type = ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(release_dir / fname, "rb") as src, zf.open(zi, "w") as dst:
                shutil.copyfileobj(src, dst, 1024 * 1024)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", default="0.4",
                        help="dataset version to build (default: 0.4; must match config.yaml)")
    parser.add_argument("--config", default=str(ROOT / "config.yaml"))
    parser.add_argument("--force", action="store_true",
                        help="overwrite an existing non-empty release directory")
    parser.add_argument("--keep-scratch", action="store_true",
                        help="keep the staged parquet instead of deleting it at the end")
    args = parser.parse_args()

    t0 = time.time()
    cfg = yaml.safe_load(Path(args.config).read_text())
    c = cfg["cohorts"]
    seeds = cfg["seeds"]
    noise = cfg["noise"]

    configured_release = Path(cfg["paths"]["release_dir"])
    release_name = f"{cfg['dataset']['name']}_{args.version}"
    release_dir = configured_release.parent / release_name
    zip_path = configured_release.parent / f"{release_name}.zip"
    scratch = Path(cfg["paths"]["scratch"]).parent / f"temp_psp_staging_{args.version}"
    results_dir = ROOT / cfg["paths"]["results"]
    results_dir.mkdir(exist_ok=True)

    if release_dir.exists() and any(release_dir.iterdir()) and not args.force:
        raise SystemExit(f"{release_dir} already exists and is not empty; pass --force to overwrite.")
    release_dir.mkdir(parents=True, exist_ok=True)
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True, exist_ok=True)

    log(f"Building {release_name} -> {release_dir}")
    con = duckdb.connect()

    # --- 1. Source views, pools, population summary ------------------------
    create_source_views(con, cfg)
    pools = build_pools(con, cfg)
    log("Measuring SSN coverage of the registry pool (pop_ssn_never)...")
    pop_ssn_never = con.execute("""
        SELECT 1.0 - count(DISTINCT s.simulant_id)::DOUBLE / count(DISTINCT p.simulant_id)
        FROM pool_registry p
        LEFT JOIN raw_ssn s ON p.simulant_id = s.simulant_id
    """).fetchone()[0]

    # --- 2. Stratified oversampling ------------------------------------------
    quota_table = load_targets(con, cfg)
    sample_oversized_cohorts(con, cfg)

    # --- 3. Stage parquet for pseudopeople --------------------------------
    source_root = Path(cfg["paths"]["psp_source"])
    changelog_src = source_root / "CHANGELOG.rst"
    if not changelog_src.exists():
        changelog_src = source_root.parent / "CHANGELOG.rst"
    path_2 = stage_for_psp(con, "df_2_ids", "df_2", scratch, changelog_src)
    path_1a = stage_for_psp(con, "df_1a_ids", "df_1a", scratch, changelog_src)
    path_1b = stage_for_psp(con, "df_1b_ids", "df_1b", scratch, changelog_src)

    # --- 4. pseudopeople noise --------------------------------------------
    log("Running pseudopeople generation (registry)...")
    df_2 = psp.generate_decennial_census(
        source=path_2, seed=seeds["psp_registry"], year=None,
        config=noise_config(noise["registry"]["address_missing"], noise["duplicate_with_guardian"]))
    log("Running pseudopeople generation (finder_500k)...")
    df_1a = psp.generate_decennial_census(
        source=path_1a, seed=seeds["psp_finder"], year=None,
        config=noise_config(noise["finder"]["address_missing"], noise["duplicate_with_guardian"]))
    log("Running pseudopeople generation (finder_100k)...")
    df_1b = psp.generate_decennial_census(
        source=path_1b, seed=seeds["psp_finder"], year=None,
        config=noise_config(noise["finder"]["address_missing"], noise["duplicate_with_guardian"]))

    # --- 5. Stratified trim to exact targets (the v0.3 fix) ---------------
    log("Trimming to exact targets with stratified_trim...")
    ids = stratified_trim(
        df_2.simulant_id, df_1a.simulant_id, df_1b.simulant_id,
        registry_target=c["registry_target"],
        finder_a_target=c["finder_500k_target"],
        finder_b_target=c["finder_100k_target"],
        overlap_a_target=c["overlap_500k_target"],
        overlap_b_target=c["overlap_100k_target"],
        seed=seeds["postprocess"],
    )
    df_2 = df_2[df_2.simulant_id.isin(ids["registry"])].copy()
    df_1a = df_1a[df_1a.simulant_id.isin(ids["finder_a"])].copy()
    df_1b = df_1b[df_1b.simulant_id.isin(ids["finder_b"])].copy()

    # --- 5b. Diagnosis date: a day within the record's census year --------
    log("Assigning diagnosis dates (uniform within each record's census year)...")
    df_2["diagnosis_date"] = diagnosis_dates(df_2["simulant_id"], df_2["year"], seeds["diagnosis_date"])

    # --- 6. SSN join + targeted noise --------------------------------------
    log("Attaching SSNs with targeted noise...")
    df_2, ssn_stats_2 = attach_noised_ssn(
        con, df_2, missing_target_rate=noise["registry"]["ssn_missing"],
        transposed_rate=noise["registry"]["ssn_transposed"],
        seed=seeds["psp_registry"], label="registry")
    df_1a, ssn_stats_1a = attach_noised_ssn(
        con, df_1a, missing_target_rate=noise["finder"]["ssn_missing"],
        transposed_rate=noise["finder"]["ssn_transposed"],
        seed=seeds["psp_finder"], label="finder_500k")
    df_1b, ssn_stats_1b = attach_noised_ssn(
        con, df_1b, missing_target_rate=noise["finder"]["ssn_missing"],
        transposed_rate=noise["finder"]["ssn_transposed"],
        seed=seeds["psp_finder"], label="finder_100k")

    # --- 7. Write release CSVs ---------------------------------------------
    frames = {
        "registry.csv": prep_for_save(df_2, REGISTRY_EXTRA_COLUMNS),
        "finder_500k.csv": prep_for_save(df_1a),
        "finder_100k.csv": prep_for_save(df_1b),
    }
    fixed_mtime = datetime(2020, 1, 1).timestamp()
    for fname, frame in frames.items():
        out = release_dir / fname
        log(f"Writing {out} ({len(frame):,} rows)...")
        frame.to_csv(out)
        os.utime(out, (fixed_mtime, fixed_mtime))

    for fname in DOC_FILES:
        shutil.copyfile(DATA_DICTIONARY, release_dir / fname)
        os.utime(release_dir / fname, (fixed_mtime, fixed_mtime))
    log("Writing deterministic zip...")
    write_deterministic_zip(zip_path, release_dir, release_name)

    # --- 8. Acceptance checks ----------------------------------------------
    log("Running acceptance checks...")
    reg_ids = set(frames["registry.csv"].index)
    fa_ids = set(frames["finder_500k.csv"].index)
    fb_ids = set(frames["finder_100k.csv"].index)
    targets = {
        "registry simulants": (len(reg_ids), c["registry_target"]),
        "finder_500k simulants": (len(fa_ids), c["finder_500k_target"]),
        "finder_100k simulants": (len(fb_ids), c["finder_100k_target"]),
        "overlap registry∩finder_500k": (len(reg_ids & fa_ids), c["overlap_500k_target"]),
        "overlap registry∩finder_100k": (len(reg_ids & fb_ids), c["overlap_100k_target"]),
        "overlap finder∩finder": (len(fa_ids & fb_ids), c["overlap_finder_finder_target"]),
    }
    if noise["duplicate_with_guardian"] == 0:
        # row duplication is switched off, so every file must be exactly one row per person
        for fname, frame in frames.items():
            targets[f"{fname} rows = people"] = (len(frame), int(frame.index.nunique()))
    failed = {k: v for k, v in targets.items() if v[0] != v[1]}
    for name, (realised, target) in targets.items():
        status = "PASS" if realised == target else "FAIL"
        log(f"  {status}: {name} = {realised:,} (target {target:,})")
    if failed:
        raise SystemExit(f"ACCEPTANCE FAILED: {failed}")

    # --- 9. results/ summaries ----------------------------------------------
    reg_counts = frames["registry.csv"].index.value_counts()

    def overlap_stats(frame: pd.DataFrame, overlap_target: int) -> dict:
        in_reg = frame.index.isin(reg_ids)
        pairs = int(reg_counts.reindex(frame.index[in_reg]).sum())
        return {
            "overlap_simulants": int(len(set(frame.index) & reg_ids)),
            "overlap_target": overlap_target,
            "true_pairs": pairs,
            "match_prevalence": float(in_reg.mean()),
        }

    manifest = {
        "dataset": cfg["dataset"]["name"],
        "version": args.version,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "release_dir": str(release_dir),
        "files": {},
        "zip": {"name": zip_path.name, **checksums(zip_path)},
        "overlaps": {
            "finder_500k": overlap_stats(frames["finder_500k.csv"], c["overlap_500k_target"]),
            "finder_100k": overlap_stats(frames["finder_100k.csv"], c["overlap_100k_target"]),
            "finder_finder_simulants": len(fa_ids & fb_ids),
        },
        "registry_duplicate_rows": int(len(frames["registry.csv"]) - len(reg_ids)),
        "columns": ["simulant_id"] + RELEASE_COLUMNS,
        "registry_columns": ["simulant_id"] + RELEASE_COLUMNS + REGISTRY_EXTRA_COLUMNS,
        "diagnosis_date": "registry only: a day uniform within the record's census year, keyed hash of simulant_id (seeds.diagnosis_date)",
        "age_sex_target": cfg["paths"]["age_sex_target"],
        "registry_pool": "last_seen",
        "census_years": [int(y) for y in c["census_years"]],
        "finder_year": int(c["finder_year"]),
    }
    for fname, frame in frames.items():
        manifest["files"][fname] = {
            "rows": int(len(frame)),
            "distinct_simulants": int(frame.index.nunique()),
            **checksums(release_dir / fname),
        }

    for fname in DOC_FILES:
        with open(release_dir / fname, newline="") as f:
            n_rows = sum(1 for _ in csv.reader(f)) - 1
        manifest["files"][fname] = {"rows": n_rows, **checksums(release_dir / fname)}

    error_rates = {"targets": noise, "realised": {}}
    for fname, frame, stats in [
        ("registry.csv", frames["registry.csv"], ssn_stats_2),
        ("finder_500k.csv", frames["finder_500k.csv"], ssn_stats_1a),
        ("finder_100k.csv", frames["finder_100k.csv"], ssn_stats_1b),
    ]:
        error_rates["realised"][fname] = {
            "ssn_missing": float(frame["ssn"].isna().mean()),
            "ssn_structural_missing": stats["structural_missing"] / stats["n"],
            "ssn_blanked": stats["blanked"],
            "ssn_transposed": stats["transposed"],
            **{f"{field}_missing": float(frame[field].isna().mean()) for field in ADDRESS_FIELDS},
        }

    fl_2020 = int(pools["by_year"].get(2020, 0))
    population_summary = {
        "fl_pool_last_seen": int(pools["pool_registry"]),
        "fl_residents_finder_year": int(pools["pool_finder"]),
        "finder_year": int(c["finder_year"]),
        "fl_simulants_by_census": {str(y): int(n) for y, n in pools["by_year"].items()},
        "fl_simulants": fl_2020,  # 2020 residents, kept for the official-count QA below
        "fl_census_2020": FL_CENSUS_2020,
        "fl_share_census": fl_2020 / FL_CENSUS_2020,
        "pop_ssn_never": float(pop_ssn_never),  # share of the last-seen registry pool never holding an SSN
    }
    log("Writing age/sex/race composition and top names from the source's true ages...")
    age_sex_qa = write_age_sex_qa(con, frames, quota_table, results_dir)
    reg_qa = age_sex_qa["registry.csv"]
    log(f"  registry age/sex shares vs target: max deviation {reg_qa['max_abs_share_deviation_pct']:.3f} pp "
        f"({reg_qa['max_abs_share_deviation_stratum']}); rows by census year "
        + ", ".join(f"{y}: {n:,}" for y, n in reg_qa["rows_by_census_year"].items()))

    environment = {
        "built_utc": manifest["created_utc"],
        "dataset_version": args.version,
        "python": platform.python_version(),
        "pseudopeople": psp.__version__,
        "duckdb": duckdb.__version__,
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "hostname": platform.node(),
        "platform": platform.platform(),
        "cpu_count": os.cpu_count(),
        "build_wall_seconds": round(time.time() - t0, 1),
        "peak_rss_mb": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 1),
    }

    for name, payload in [
        ("release_manifest.json", manifest),
        ("error_rates.json", error_rates),
        ("population_summary.json", population_summary),
        ("environment.json", environment),
    ]:
        out = results_dir / name
        out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        log(f"Wrote {out}")

    if not args.keep_scratch:
        shutil.rmtree(scratch, ignore_errors=True)

    log(f"DONE in {environment['build_wall_seconds']:.0f}s "
        f"(peak RSS {environment['peak_rss_mb']:.0f} MB).")
    log("All design targets hit exactly. Next steps:")
    log("  1. Re-run this script and compare checksums (run-twice identity test).")
    log(f"  2. Bump dataset.version to {args.version} and paths.release_dir to "
        f"{release_dir} in config.yaml.")
    log("  3. Re-run pipeline/linkage_baseline.py and re-render paper.qmd.")


if __name__ == "__main__":
    main()
