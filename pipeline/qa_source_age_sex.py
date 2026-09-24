"""Florida simulants by census year, sex and FCDS age bin, from the pseudopeople source population.

Pipeline tier: one pass over the decennial-census observer (52 GB, ~100 s on
two threads within a 64 GB allocation). Writes ``results/fl_census_age_sex.csv``
with four pools, each a count per (sex, age_start):

* ``2020``, ``2030``, ``2040`` — Florida residents in that census (one row per
  simulant per year);
* ``last_seen`` — every simulant ever recorded in Florida, once, at their last
  census appearance (the pool a registry that keeps deceased and departed cases
  would draw from).

Used to decide the registry's size and source year (§2.2, decision #16) and as
the Florida-population panel of Figure 1.

    uv run python pipeline/qa_source_age_sex.py
"""

from __future__ import annotations

import time
from pathlib import Path

import duckdb
import pandas as pd
import yaml

from simulated_data_for_fcds_scale_rl.age_sex_weights import load_age_sex_weights

ROOT = Path(__file__).resolve().parent.parent
CFG = yaml.safe_load((ROOT / "config.yaml").read_text())
RESULTS = ROOT / CFG["paths"]["results"]


def main() -> None:
    src = Path(CFG["paths"]["psp_source"]) / "decennial_census" / "*.parquet"
    w = load_age_sex_weights(ROOT / CFG["paths"]["age_sex_weights"])
    bins = w[w["sex"] == "Female"][["age_start", "age_end"]].reset_index(drop=True)
    con = duckdb.connect()
    con.execute("SET memory_limit='48GB'; SET threads=2; SET preserve_insertion_order=false;")
    con.register("bins", bins)
    t0 = time.time()
    con.execute(f"""
        CREATE TABLE fl AS
        SELECT simulant_id, year, any_value(sex) AS sex, min(age) AS age
        FROM read_parquet('{src}')
        WHERE state = '{CFG["cohorts"]["state"]}'
        GROUP BY simulant_id, year
    """)
    n = con.execute("SELECT count(*) FROM fl").fetchone()[0]
    print(f"scan done in {time.time() - t0:.0f}s; {n:,} Florida person-census rows")
    snap = con.execute("""
        SELECT CAST(f.year AS VARCHAR) AS pool, f.sex, b.age_start, count(*) AS n
        FROM fl f JOIN bins b ON f.age >= b.age_start AND f.age < b.age_end
        WHERE f.sex IN ('Male', 'Female') GROUP BY ALL
    """).df()
    last = con.execute("""
        SELECT 'last_seen' AS pool, f.sex, b.age_start, count(*) AS n
        FROM (SELECT * FROM fl QUALIFY row_number() OVER (PARTITION BY simulant_id ORDER BY year DESC) = 1) f
        JOIN bins b ON f.age >= b.age_start AND f.age < b.age_end
        WHERE f.sex IN ('Male', 'Female') GROUP BY ALL
    """).df()
    out = pd.concat([snap, last]).sort_values(["pool", "sex", "age_start"])
    out.to_csv(RESULTS / "fl_census_age_sex.csv", index=False)
    print("wrote results/fl_census_age_sex.csv")


if __name__ == "__main__":
    main()
