"""Build the released cohorts: registry stand-in plus two finder files.

Heavy pipeline tier — the v0.3 rebuild entry point (run-list items 2-4),
ported from the working notebook
``2026_02_11b_duckdb_psp_reproducible_randomness.ipynb`` with the v0.3 fixes:

* the exact-target trim is ``stratified_trim`` (``src/``), which hits every
  design target exactly and makes the finder files disjoint — v0.2's
  unstratified trim overshot the overlap targets by roughly a third;
* ``race_ethnicity`` is carried into the released schema;
* the GBD prevalence weights are read from ``reference/`` instead of being
  hard-coded;
* checksums (MD5 and SHA-256), a release manifest, realised error rates, a
  population summary, and environment info are written to ``results/``.

Every stochastic step is a pure function of the seeds in ``config.yaml``; run
the script twice and compare checksums for the run-twice identity test.

Run on a compute node, never a login/dev node:

    srun --mem=120G -c 8 uv run python pipeline/build_cohorts.py

On success: bump ``dataset.version`` and ``paths.release_dir`` in
``config.yaml``, re-run ``pipeline/linkage_baseline.py``, and re-render the
paper once.
"""

from __future__ import annotations

import argparse
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
    """Deduplicated Florida census view plus the raw SSN view (read-only)."""
    root_path = Path(cfg["paths"]["psp_source"])
    census_glob = find_parquet_source(root_path, ["decennial_census", "decennial_census_observer"])
    ssn_glob = find_parquet_source(root_path, ["social_security", "social_security_observer"])
    state = cfg["cohorts"]["state"]
    year = cfg["cohorts"]["year"]

    con.execute(f"""
        CREATE OR REPLACE VIEW raw_census AS
        SELECT * FROM read_parquet('{census_glob}')
        WHERE state = '{state}' AND year = {year}
        QUALIFY row_number() OVER (PARTITION BY simulant_id ORDER BY year DESC) = 1
    """)
    con.execute(f"CREATE OR REPLACE VIEW raw_ssn AS SELECT simulant_id, ssn FROM read_parquet('{ssn_glob}')")

    fl_count = con.execute("SELECT count(*) FROM raw_census").fetchone()[0]
    if fl_count == 0:
        raise SystemExit(f"CRITICAL: no records found for state='{state}'. Check paths.psp_source.")
    log(f"Florida extract: {fl_count:,} simulants after deduplication.")


def load_rates(con: duckdb.DuckDBPyConnection) -> None:
    """GBD all-neoplasm prevalence weights (percentages) from reference/."""
    rates_csv = ROOT / "reference" / "gbd_neoplasm_prevalence_florida.csv"
    long_rates = pd.read_csv(rates_csv, comment="#")
    expected = {"age_start", "age_end", "sex", "prevalence_pct"}
    if set(long_rates.columns) != expected:
        raise SystemExit(f"{rates_csv} columns {list(long_rates.columns)} != {sorted(expected)}")
    con.register("long_rates", long_rates)
    con.execute("CREATE OR REPLACE TABLE rates AS SELECT * FROM long_rates")


def sample_oversized_cohorts(con: duckdb.DuckDBPyConnection, cfg: dict) -> None:
    """Oversampled cohort ID tables via keyed-hash Efraimidis-Spirakis draws.

    We intentionally avoid DuckDB's built-in random() so results are
    reproducible across threads and runs: every draw is a pure function of
    (simulant_id, salt, seed) via md5_number_lower(). Salt strings are kept
    identical to the v0.2 notebook so the draws are comparable.
    """
    c = cfg["cohorts"]
    seed = cfg["seeds"]["duckdb_sample"]
    oversample = c["oversample"]
    n2_sample = int(c["registry_target"] * oversample)
    n1a_sample = int(c["finder_500k_target"] * oversample)
    n1b_sample = int(c["finder_100k_target"] * oversample)
    overlap_a_sample = int(c["overlap_500k_target"] * oversample)
    overlap_b_sample = int(c["overlap_100k_target"] * oversample)

    log(f"Sampling oversized cohorts ({oversample}x)...")
    con.execute(f"""
        CREATE OR REPLACE TABLE df_2_ids AS
        WITH weighted_pop AS (
            SELECT
                c.simulant_id,
                (r.prevalence_pct / 100.0) AS prob_weight
            FROM raw_census c
            JOIN rates r
              ON c.sex = r.sex
              AND c.age >= r.age_start
              AND c.age < r.age_end
            WHERE (r.prevalence_pct / 100.0) > 0
        )
        SELECT simulant_id
        FROM weighted_pop
        ORDER BY
            -ln(
                (
                    md5_number_lower(
                        CAST(simulant_id AS VARCHAR) || ':df2_weighted:{seed}'
                    )::DOUBLE + 1
                ) / 18446744073709551617.0
            ) / prob_weight
        LIMIT {n2_sample}
    """)

    for table, overlap_salt, rest_salt, overlap_n, total_n in [
        ("df_1a_ids", "df1a_overlap", "df1a_rest", overlap_a_sample, n1a_sample),
        ("df_1b_ids", "df1b_overlap", "df1b_rest", overlap_b_sample, n1b_sample),
    ]:
        con.execute(f"""
            CREATE OR REPLACE TABLE {table} AS
            SELECT * FROM (
                SELECT simulant_id
                FROM df_2_ids
                ORDER BY md5_number_lower(CAST(simulant_id AS VARCHAR) || ':{overlap_salt}:{seed}')
                LIMIT {overlap_n}
            )
            UNION ALL
            SELECT * FROM (
                SELECT c.simulant_id
                FROM raw_census c
                WHERE c.simulant_id NOT IN (SELECT simulant_id FROM df_2_ids)
                ORDER BY md5_number_lower(CAST(c.simulant_id AS VARCHAR) || ':{rest_salt}:{seed}')
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
            SELECT c.* FROM raw_census c
            JOIN {table_name} t ON c.simulant_id = t.simulant_id
            ORDER BY c.simulant_id
        ) TO '{target_dir}/decennial_census_observer.parquet' (FORMAT PARQUET)
    """)
    return str(root_out)


def noise_config(addr_missing: float) -> dict:
    return {
        "decennial_census": {
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


def prep_for_save(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in RELEASE_COLUMNS if c not in df.columns]
    if missing:
        raise SystemExit(f"Release columns missing from generated data: {missing}")
    out = df.set_index("simulant_id").filter(RELEASE_COLUMNS)
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
        for fname in sorted(RELEASE_FILES):
            zi = ZipInfo(f"{arc_prefix}/{fname}", date_time=(2020, 1, 1, 0, 0, 0))
            zi.compress_type = ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(release_dir / fname, "rb") as src, zf.open(zi, "w") as dst:
                shutil.copyfileobj(src, dst, 1024 * 1024)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", default="0.3", help="dataset version to build (default: 0.3)")
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

    # --- 1. Source views, population summary ------------------------------
    create_source_views(con, cfg)
    fl_simulants = con.execute("SELECT count(*) FROM raw_census").fetchone()[0]
    log("Measuring population-level SSN coverage (pop_ssn_never)...")
    pop_ssn_never = con.execute("""
        SELECT 1.0 - count(DISTINCT s.simulant_id)::DOUBLE / count(DISTINCT c.simulant_id)
        FROM raw_census c
        LEFT JOIN raw_ssn s ON c.simulant_id = s.simulant_id
    """).fetchone()[0]

    # --- 2. Weighted oversampling -----------------------------------------
    load_rates(con)
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
        source=path_2, seed=seeds["psp_registry"],
        config=noise_config(noise["registry"]["address_missing"]))
    log("Running pseudopeople generation (finder_500k)...")
    df_1a = psp.generate_decennial_census(
        source=path_1a, seed=seeds["psp_finder"],
        config=noise_config(noise["finder"]["address_missing"]))
    log("Running pseudopeople generation (finder_100k)...")
    df_1b = psp.generate_decennial_census(
        source=path_1b, seed=seeds["psp_finder"],
        config=noise_config(noise["finder"]["address_missing"]))

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
        "registry.csv": prep_for_save(df_2),
        "finder_500k.csv": prep_for_save(df_1a),
        "finder_100k.csv": prep_for_save(df_1b),
    }
    fixed_mtime = datetime(2020, 1, 1).timestamp()
    for fname, frame in frames.items():
        out = release_dir / fname
        log(f"Writing {out} ({len(frame):,} rows)...")
        frame.to_csv(out)
        os.utime(out, (fixed_mtime, fixed_mtime))

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
    }
    for fname, frame in frames.items():
        manifest["files"][fname] = {
            "rows": int(len(frame)),
            "distinct_simulants": int(frame.index.nunique()),
            **checksums(release_dir / fname),
        }

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

    population_summary = {
        "fl_simulants": int(fl_simulants),
        "fl_census_2020": FL_CENSUS_2020,
        "fl_share_census": fl_simulants / FL_CENSUS_2020,
        "pop_ssn_never": float(pop_ssn_never),
    }

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
