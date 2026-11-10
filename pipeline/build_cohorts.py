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
* pseudopeople's row noise (non-response, omit-row, duplicate-with-guardian) is
  switched off (``noise.row_noise``), so each file holds exactly the people the
  keyed-hash draw selected and nothing is oversampled or trimmed; the build
  asserts that pseudopeople returned exactly the staged rows (v0.4; earlier
  builds drew oversize and trimmed back, which v0.2 got wrong);
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
DOC_FILES = ["data_dictionary.csv", "README.md", "pseudopeople_config.yaml"]
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
    """Per-stratum registry quotas: target age/sex shares × the registry target, capped by the pool.

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
    n_sample = int(cfg["cohorts"]["registry_target"])
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


def sample_cohorts(con: duckdb.DuckDBPyConnection, cfg: dict) -> None:
    """Cohort ID tables at exactly the design targets: the registry by stratum quotas, the finders by keyed-hash draws.

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
    finder_year = int(c["finder_year"])
    n1a_sample = int(c["finder_500k_target"])
    n1b_sample = int(c["finder_100k_target"])
    overlap_a_sample = int(c["overlap_500k_target"])
    overlap_b_sample = int(c["overlap_100k_target"])

    log("Sampling cohorts at their exact targets: stratified registry, then finders...")
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

    # The finder files must share no people (cohorts.overlap_finder_finder_target is 0),
    # so the second file's draws exclude everyone the first file took; with row noise
    # off nothing is trimmed afterwards, so the draw itself has to be disjoint.
    for table, overlap_salt, rest_salt, overlap_n, total_n, exclude in [
        ("df_1a_ids", "df1a_overlap", "df1a_rest", overlap_a_sample, n1a_sample, ""),
        ("df_1b_ids", "df1b_overlap", "df1b_rest", overlap_b_sample, n1b_sample,
         "AND simulant_id NOT IN (SELECT simulant_id FROM df_1a_ids)"),
    ]:
        con.execute(f"""
            CREATE OR REPLACE TABLE {table} AS
            SELECT * FROM (
                SELECT simulant_id, year
                FROM df_2_ids
                WHERE year = {finder_year} {exclude}
                ORDER BY md5_number_lower(CAST(simulant_id AS VARCHAR) || ':{overlap_salt}:{seed}')
                LIMIT {overlap_n}
            )
            UNION ALL
            SELECT * FROM (
                SELECT simulant_id, year
                FROM pool_finder
                WHERE simulant_id NOT IN (SELECT simulant_id FROM df_2_ids) {exclude}
                ORDER BY md5_number_lower(CAST(simulant_id AS VARCHAR) || ':{rest_salt}:{seed}')
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


def noise_config(addr_missing: float, row_noise: dict) -> dict:
    """pseudopeople configuration for one file: address blanking at the file's rate, and the
    three row-noise probabilities (all 0 in config.yaml, so rows out equal rows in)."""
    return {
        "decennial_census": {
            "row_noise": {
                "do_not_respond": {"row_probability": row_noise["do_not_respond"]},
                "omit_row": {"row_probability": row_noise["omit_row"]},
                "duplicate_with_guardian": {
                    "row_probability_in_households_under_18": row_noise["duplicate_with_guardian"],
                    "row_probability_in_college_group_quarters_under_24": row_noise["duplicate_with_guardian"],
                },
            },
            "column_noise": {
                field: {"leave_blank": {"cell_probability": addr_missing}}
                for field in ADDRESS_FIELDS
            }
        }
    }


def attach_noised_ssn(con: duckdb.DuckDBPyConnection, df_census: pd.DataFrame,
                      *, missing_target_rate: float, transposed_rate: float,
                      wrong_digit_rate: float, seed: int, label: str) -> tuple[pd.DataFrame, dict]:
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
        wrong_digit_rate=wrong_digit_rate,
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


_MDAYS = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])


def mdy_parts(series: pd.Series) -> pd.DataFrame:
    """Strict MM/DD/YYYY calendar parse into integer year, month, day columns (NaN where invalid).

    Integer arithmetic rather than timestamps, because noised dates reach years such as 0976 or
    9876, which overflow pandas' nanosecond timestamps. A value is valid only if it matches the
    layout, the month is 1-12 and the day exists in that month of that year.
    """
    parts = series.astype("string").str.extract(r"^(\d{2})/(\d{2})/(\d{4})$")
    m, d, y = (pd.to_numeric(parts[i], errors="coerce").astype("float64") for i in range(3))  # plain floats: NaN compares False
    leap = ((y % 4 == 0) & (y % 100 != 0)) | (y % 400 == 0)
    month_index = m.fillna(1).astype(int).clip(1, 12) - 1
    days_in_month = pd.Series(_MDAYS[month_index.to_numpy()], index=series.index) + ((m == 2) & leap).astype(int)
    valid = y.notna() & m.between(1, 12) & d.ge(1) & (d <= days_in_month)
    return pd.DataFrame({"y": y.where(valid), "m": m.where(valid), "d": d.where(valid)})


def dob_summary(frame: pd.DataFrame, ref: pd.DataFrame) -> dict:
    """Blank, unparseable (strict MM/DD/YYYY calendar parse) and implausible-age shares of date_of_birth.

    ``ref`` has integer columns y, m, d giving the date each age is measured at (the diagnosis
    date for the registry, census day of the finder year for a finder file); implausible means
    an age below 0 or above 110.
    """
    dob = frame["date_of_birth"]
    blank = dob.isna() | (dob == "")
    b = mdy_parts(dob)
    parsed = b["y"].notna()
    unparseable = ~blank & ~parsed
    birthday_passed = (ref["m"] > b["m"]) | ((ref["m"] == b["m"]) & (ref["d"] >= b["d"]))
    age = (ref["y"] - b["y"]) - (~birthday_passed).astype(int)
    implausible = parsed & ((age < 0) | (age > 110))
    return {"blank": float(blank.mean()), "unparseable": float(unparseable.mean()),
            "implausible_age": float(implausible.mean()), "any": float((blank | unparseable | implausible).mean())}


def write_release_docs(release_dir: Path, release_name: str, cfg: dict, frames: dict, ssn_stats: dict) -> None:
    """README.md (release notes with set and realised noise rates) and the effective pseudopeople config.

    Both are deterministic given the configuration and seeds: no timestamps, and the realised
    values are computed from the frames about to be written, so the zip's bytes stay a pure
    function of the build and the run-twice identity test covers them.
    """
    noise, c = cfg["noise"], cfg["cohorts"]
    psp_cfg = {kind: psp.get_config(noise_config(noise[kind]["address_missing"], noise["row_noise"]))["decennial_census"]
               for kind in ("registry", "finder")}
    (release_dir / "pseudopeople_config.yaml").write_text(
        "# The pseudopeople noise configuration actually applied to each file (decennial_census dataset), as\n"
        "# returned by pseudopeople.get_config() for the overrides in config.yaml. cell_probability is the share\n"
        "# of cells a mechanism touches; token_probability is the chance that each digit or character of a\n"
        "# touched cell is altered. Row noise is zero: each file holds exactly the people drawn.\n"
        + yaml.safe_dump(psp_cfg, sort_keys=True))

    def census_day(frame):  # April 1 of the finder year, one row per record
        return pd.DataFrame({"y": int(c["finder_year"]), "m": 4, "d": 1}, index=frame.index)
    dob = {
        "registry.csv": dob_summary(frames["registry.csv"], mdy_parts(frames["registry.csv"]["diagnosis_date"])),
        "finder_500k.csv": dob_summary(frames["finder_500k.csv"], census_day(frames["finder_500k.csv"])),
        "finder_100k.csv": dob_summary(frames["finder_100k.csv"], census_day(frames["finder_100k.csv"])),
    }
    pct = lambda x, d=2: f"{100 * x:.{d}f}%"  # noqa: E731
    rows = []
    for fname, kind in (("registry.csv", "registry"), ("finder_500k.csv", "finder"), ("finder_100k.csv", "finder")):
        s, f = ssn_stats[fname], frames[fname]
        present = s["n"] - int(f["ssn"].isna().sum())
        rows.append(f"| {fname} | {len(f):,} | {pct(noise[kind]['ssn_missing'], 0)} | {pct(f['ssn'].isna().mean())} "
                    f"({pct(s['structural_missing'] / s['n'])} never held one) | {pct(noise[kind]['ssn_transposed'], 0)} | "
                    f"{s['transposed']:,} ({pct(s['transposed'] / present if present else 0)}) | {pct(noise[kind]['ssn_wrong_digit'], 1)} | "
                    f"{s['wrong_digit']:,} ({pct(s['wrong_digit'] / present if present else 0)}) |")
    dob_rows = [f"| {fname} | {pct(d['blank'])} | {pct(d['unparseable'])} | {pct(d['implausible_age'])} | {pct(d['any'])} |"
                for fname, d in dob.items()]
    readme = f"""# {release_name}: release notes

Simulated record-linkage test files in the size and shape of the Florida Cancer Data System's linkage
task: a simulated registry and two finder files drawn from the pseudopeople simulated United States
population, with a ground-truth key. Every person is simulated; nothing here describes a real person.
The accompanying Data Resource Profile describes the design, the measurements and the limitations.

## Files

| file | contents |
|---|---|
| `registry.csv` | the simulated registry, one row per person, with a `diagnosis_date` |
| `finder_500k.csv`, `finder_100k.csv` | two finder files (researcher cohorts), one row per person, each sharing 20% of its people with the registry and none with each other |
| `data_dictionary.csv` | one row per field: type, format, example, blank convention, source, noise mechanisms |
| `pseudopeople_config.yaml` | the pseudopeople noise configuration applied to each file, as pseudopeople reports it |

The same `simulant_id` in two files is the same simulated person. A registry row and a finder row with
the same identifier are a true match; every other pairing is a true non-match. Files are UTF-8 CSV with a
header row, blanks as empty fields, dates as `MM/DD/YYYY` and SSNs as `ddd-dd-dddd`. A field is quoted only
when it contains a comma, which is rare enough that some CSV readers need the quote character named
explicitly (DuckDB: `quote='"'`). MD5 and SHA-256 digests of every file are in the manifest deposited beside
this archive.

## Noise, set and realised

Column noise is pseudopeople's default suite (`pseudopeople_config.yaml`): each listed mechanism touches
1% of a column's cells, and the digit- and character-level mechanisms (`write_wrong_digits`,
`make_ocr_errors`, `make_typos`) then alter each digit or character of a touched cell with probability 0.1,
so a touched date of birth may change one digit, several, or none. Row noise (non-response, omission,
duplication) is off, so each file holds exactly the people drawn. The SSN is handled outside pseudopeople,
with the rates below.

| file | rows | SSN blank, set | SSN blank, realised | adjacent-digit swap, set | swaps applied | one wrong digit, set | wrong digits applied |
|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}

SSN blanking is by count: people who never held a number in the simulation are counted first and only the
shortfall is blanked, so the registry, whose never-held share already exceeds its 5% target, has no SSN
blanked by the build. The swap exchanges one randomly chosen adjacent pair of digits (about one swap in ten
hits two equal digits and changes nothing, so the visible rate runs a little under the applied rate). The
wrong digit replaces one randomly chosen digit with a different digit, so every hit changes the value. Both
keep the `ddd-dd-dddd` form, so a format check cannot see them; a true-match join can.

Because the finder files' true matches are registry people, who carry the registry's cancer-age profile,
and SSN coverage in the source population falls with age, finder SSNs are blank somewhat more often among
true matches than among non-matches (about 21% against 20% in the 500k file). This is an age effect of the
design, not a marker of match status.

Date of birth, realised, with ages measured at the diagnosis date (registry) or census day of
{c['finder_year']} (finder files); unparseable means a strict `MM/DD/YYYY` calendar parse fails (month 13,
30 February, a letter from an OCR error); implausible means an age below 0 or above 110 after parsing.

| file | blank | unparseable | implausible age | any of the three |
|---|---|---|---|---|
{chr(10).join(dob_rows)}

## Not in this version

* **Borrowed SSNs** (a household member's number on a person's record) are out of scope. SSNs come from
  the simulated Social Security observer; pseudopeople's copy-from-household-member mechanism lives in its
  tax datasets, and this build does not carry household membership into the SSN step. It is feasible in a
  later version.
* **No move, ageing or surname change between the two records of a true match:** both are the same census
  record noised twice. **No wrong digits in finder-file SSNs**, only the adjacent swap. **No telephone or
  email fields.** Addresses place people in real Florida cities at no real street location and must not be
  geocoded.

## Changes from v0.3

Row noise switched off, so every file is exactly one row per person; cohorts drawn at their exact targets
with the finder files disjoint by construction; one wrong digit in 0.5% of registry SSNs (requested by the
second author after reviewing v0.3); this README, the data dictionary and the pseudopeople configuration
added to the archive. Every noise draw was re-made, so v0.3 counts do not carry over.
"""
    (release_dir / "README.md").write_text(readme)


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

    # --- 2. Stratified sampling at the exact targets ---------------------------
    quota_table = load_targets(con, cfg)
    sample_cohorts(con, cfg)

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
        config=noise_config(noise["registry"]["address_missing"], noise["row_noise"]))
    log("Running pseudopeople generation (finder_500k)...")
    df_1a = psp.generate_decennial_census(
        source=path_1a, seed=seeds["psp_finder"], year=None,
        config=noise_config(noise["finder"]["address_missing"], noise["row_noise"]))
    log("Running pseudopeople generation (finder_100k)...")
    df_1b = psp.generate_decennial_census(
        source=path_1b, seed=seeds["psp_finder"], year=None,
        config=noise_config(noise["finder"]["address_missing"], noise["row_noise"]))

    # --- 5. Row noise is off, so pseudopeople must have returned exactly the staged rows
    log("Checking that pseudopeople returned exactly the staged rows...")
    for label, frame, table in (("registry", df_2, "df_2_ids"), ("finder_500k", df_1a, "df_1a_ids"), ("finder_100k", df_1b, "df_1b_ids")):
        staged = set(con.execute(f"SELECT simulant_id FROM {table}").df()["simulant_id"].astype(str))
        if len(frame) != len(staged) or set(frame.simulant_id.astype(str)) != staged:
            raise SystemExit(f"CRITICAL: pseudopeople returned {len(frame):,} rows for {label} against {len(staged):,} staged "
                             f"people; row noise must be off (noise.row_noise in config.yaml).")
        log(f"  {label}: {len(frame):,} rows, one per staged person")

    # --- 5b. Diagnosis date: a day within the record's census year --------
    log("Assigning diagnosis dates (uniform within each record's census year)...")
    df_2["diagnosis_date"] = diagnosis_dates(df_2["simulant_id"], df_2["year"], seeds["diagnosis_date"])

    # --- 6. SSN join + targeted noise --------------------------------------
    log("Attaching SSNs with targeted noise...")
    df_2, ssn_stats_2 = attach_noised_ssn(
        con, df_2, missing_target_rate=noise["registry"]["ssn_missing"],
        transposed_rate=noise["registry"]["ssn_transposed"],
        wrong_digit_rate=noise["registry"]["ssn_wrong_digit"],
        seed=seeds["psp_registry"], label="registry")
    df_1a, ssn_stats_1a = attach_noised_ssn(
        con, df_1a, missing_target_rate=noise["finder"]["ssn_missing"],
        transposed_rate=noise["finder"]["ssn_transposed"],
        wrong_digit_rate=noise["finder"]["ssn_wrong_digit"],
        seed=seeds["psp_finder"], label="finder_500k")
    df_1b, ssn_stats_1b = attach_noised_ssn(
        con, df_1b, missing_target_rate=noise["finder"]["ssn_missing"],
        transposed_rate=noise["finder"]["ssn_transposed"],
        wrong_digit_rate=noise["finder"]["ssn_wrong_digit"],
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

    shutil.copyfile(DATA_DICTIONARY, release_dir / "data_dictionary.csv")
    write_release_docs(release_dir, release_name, cfg, frames, {"registry.csv": ssn_stats_2, "finder_500k.csv": ssn_stats_1a, "finder_100k.csv": ssn_stats_1b})
    for fname in DOC_FILES:
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
    if all(v == 0 for v in noise["row_noise"].values()):
        # row noise is switched off, so every file must be exactly one row per person
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
        entry = checksums(release_dir / fname)
        if fname.endswith(".csv"):
            with open(release_dir / fname, newline="") as f:
                entry["rows"] = sum(1 for _ in csv.reader(f)) - 1
        manifest["files"][fname] = entry

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
            "ssn_wrong_digit": stats["wrong_digit"],
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
