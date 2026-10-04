"""The cohort draw must hit every design target exactly and keep the finder files disjoint.

With pseudopeople's row noise off nothing is trimmed after noising, so the DuckDB draw
in ``pipeline/build_cohorts.py`` is the only place the counts and the finder-finder
disjointness are enforced. This runs it on a small synthetic pool.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("build_cohorts", ROOT / "pipeline" / "build_cohorts.py")
build_cohorts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build_cohorts)

CFG = {
    "seeds": {"duckdb_sample": 42},
    "cohorts": {"finder_year": 2040, "finder_500k_target": 300, "finder_100k_target": 120,
                "overlap_500k_target": 60, "overlap_100k_target": 30},
}


def _synthetic_pool(con: duckdb.DuckDBPyConnection, n_pool: int = 4000) -> None:
    """A registry pool of n_pool people over three census years, two sexes and two age bins."""
    years = [2020, 2030, 2040]
    pool = pd.DataFrame({
        "simulant_id": [f"0_{i}" for i in range(n_pool)],
        "year": [years[i % 3] for i in range(n_pool)],
        "sex": ["Female" if i % 2 else "Male" for i in range(n_pool)],
        "age_start": [40 if i % 4 < 2 else 65 for i in range(n_pool)],
    })
    con.register("strata_df", pool)
    con.execute("CREATE TABLE strata AS SELECT * FROM strata_df")
    # the finder pool is the 2040 residents, including people outside the registry
    con.execute("CREATE TABLE pool_finder AS SELECT simulant_id, year FROM strata WHERE year = 2040")
    quotas = pd.DataFrame({"sex": ["Female", "Male", "Female", "Male"], "age_start": [40, 40, 65, 65],
                           "quota": [200, 200, 300, 300]})
    con.register("quotas_df", quotas)
    con.execute("CREATE TABLE quotas AS SELECT * FROM quotas_df")


def test_draw_hits_targets_and_keeps_finder_files_disjoint():
    con = duckdb.connect()
    _synthetic_pool(con)
    build_cohorts.sample_cohorts(con, CFG)
    reg = set(con.execute("SELECT simulant_id FROM df_2_ids").df()["simulant_id"])
    fa = set(con.execute("SELECT simulant_id FROM df_1a_ids").df()["simulant_id"])
    fb = set(con.execute("SELECT simulant_id FROM df_1b_ids").df()["simulant_id"])
    assert len(reg) == 1000  # the sum of the quotas
    assert len(fa) == CFG["cohorts"]["finder_500k_target"]
    assert len(fb) == CFG["cohorts"]["finder_100k_target"]
    assert len(reg & fa) == CFG["cohorts"]["overlap_500k_target"]
    assert len(reg & fb) == CFG["cohorts"]["overlap_100k_target"]
    assert not (fa & fb), "the two finder files must share no people"
    # every finder member is a 2040 resident, and overlap members are the registry's 2040 members
    years = con.execute("SELECT DISTINCT year FROM df_1a_ids UNION SELECT DISTINCT year FROM df_1b_ids").df()["year"]
    assert set(years) == {2040}


def test_draw_is_deterministic():
    draws = []
    for _ in range(2):
        con = duckdb.connect()
        _synthetic_pool(con)
        build_cohorts.sample_cohorts(con, CFG)
        draws.append(tuple(sorted(con.execute("SELECT simulant_id FROM df_1b_ids").df()["simulant_id"])))
    assert draws[0] == draws[1]
