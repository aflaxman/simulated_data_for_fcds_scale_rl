"""Age/sex/race composition and top first names of the released files.

Pipeline tier (reads the 5M-row registry CSV), but light: one DuckDB pass per
file, a few seconds each. Writes three small summaries for Figure 1 and the
master-graphic candidates:

* ``results/registry_age_sex.csv`` — long table: file, sex, age_group,
  age_start, race_ethnicity, count. Age is derived from the *noised*
  ``date_of_birth`` as of Census Day 2020 (the released files carry no age
  column); rows whose date fails to parse, whose sex is not Male/Female, or
  whose age falls outside the bins are counted in the JSON below, not here.
* ``results/registry_top_names.csv`` — top-3 first names per file, sex and
  age group, as they appear in the file (noise included).
* ``results/age_sex_qa.json`` — per file: rows, rows binned, rows excluded and why.

Age bins are the FCDS table's (``config.yaml``, ``paths.age_sex_weights``), so
the simulated registry can be compared with FCDS's reported case counts.

    uv run python pipeline/qa_age_sex.py
"""

from __future__ import annotations

import json
from pathlib import Path

import duckdb
import pandas as pd
import yaml

from simulated_data_for_fcds_scale_rl.age_sex_weights import load_age_sex_weights

ROOT = Path(__file__).resolve().parent.parent
CFG = yaml.safe_load((ROOT / "config.yaml").read_text())
RELEASE = Path(CFG["paths"]["release_dir"])
RESULTS = ROOT / CFG["paths"]["results"]
FILES = ["registry.csv", "finder_500k.csv", "finder_100k.csv"]
REFERENCE_DATE = f"{CFG['cohorts']['year']}-04-01"  # Census Day
# Quoted fields are rare, so DuckDB's sniffer must be told the quote character.
READ_OPTS = "header=true, all_varchar=true, quote='\"'"
TOP_N = 3


def age_bins() -> pd.DataFrame:
    w = load_age_sex_weights(ROOT / CFG["paths"]["age_sex_weights"])
    bins = w[w["sex"] == "Female"][["age_start", "age_end"]].drop_duplicates().sort_values("age_start")
    bins["age_group"] = [
        f"{s}+" if e >= 200 else f"{s}–{e - 1}" for s, e in zip(bins["age_start"], bins["age_end"])
    ]
    return bins.reset_index(drop=True)


def main() -> None:
    con = duckdb.connect()
    con.register("bins", age_bins())
    counts, names, qa = [], [], {}
    for fname in FILES:
        csv = RELEASE / fname
        con.execute(f"""
            CREATE OR REPLACE TABLE rows AS
            WITH parsed AS (
                SELECT sex, race_ethnicity, first_name,
                       try_strptime(date_of_birth, '%m/%d/%Y') AS dob
                FROM read_csv('{csv}', {READ_OPTS})
            ),
            aged AS (
                SELECT *,
                       CASE WHEN dob IS NULL THEN NULL
                            ELSE year(DATE '{REFERENCE_DATE}') - year(dob)
                                 - CASE WHEN (month(dob), day(dob)) > (month(DATE '{REFERENCE_DATE}'), day(DATE '{REFERENCE_DATE}'))
                                        THEN 1 ELSE 0 END
                       END AS age
                FROM parsed
            )
            SELECT a.*, b.age_group, b.age_start
            FROM aged a
            LEFT JOIN bins b ON a.age >= b.age_start AND a.age < b.age_end
        """)
        total, dob_bad, sex_bad, unbinned = con.execute("""
            SELECT count(*),
                   count(*) FILTER (WHERE dob IS NULL),
                   count(*) FILTER (WHERE sex NOT IN ('Male', 'Female') OR sex IS NULL),
                   count(*) FILTER (WHERE dob IS NOT NULL AND age_group IS NULL)
            FROM rows
        """).fetchone()
        kept = con.execute("""
            SELECT sex, age_group, age_start, coalesce(race_ethnicity, 'Unknown') AS race_ethnicity, count(*) AS count
            FROM rows
            WHERE age_group IS NOT NULL AND sex IN ('Male', 'Female')
            GROUP BY ALL ORDER BY sex, age_start, race_ethnicity
        """).df()
        kept.insert(0, "file", fname)
        counts.append(kept)
        top = con.execute(f"""
            SELECT * FROM (
                SELECT sex, age_group, age_start, first_name, count(*) AS count
                FROM rows
                WHERE age_group IS NOT NULL AND sex IN ('Male', 'Female')
                  AND first_name IS NOT NULL AND first_name <> ''
                GROUP BY sex, age_group, age_start, first_name
            )
            QUALIFY row_number() OVER (PARTITION BY sex, age_group ORDER BY count DESC, first_name) <= {TOP_N}
            ORDER BY sex, age_start, count DESC
        """).df()
        top["rank"] = top.groupby(["sex", "age_group"]).cumcount() + 1
        top.insert(0, "file", fname)
        names.append(top)
        qa[fname] = {
            "rows": int(total),
            "rows_binned": int(kept["count"].sum()),
            "dob_unparseable": int(dob_bad),
            "sex_not_male_female": int(sex_bad),
            "age_outside_bins": int(unbinned),
            "reference_date": REFERENCE_DATE,
        }
        print(f"{fname}: {total:,} rows, {kept['count'].sum():,} binned "
              f"({dob_bad:,} unparseable DOB, {sex_bad:,} sex not M/F, {unbinned:,} outside bins)")
    pd.concat(counts).to_csv(RESULTS / "registry_age_sex.csv", index=False)
    pd.concat(names).to_csv(RESULTS / "registry_top_names.csv", index=False)
    (RESULTS / "age_sex_qa.json").write_text(json.dumps(qa, indent=2) + "\n")
    print("wrote registry_age_sex.csv, registry_top_names.csv, age_sex_qa.json")


if __name__ == "__main__":
    main()
