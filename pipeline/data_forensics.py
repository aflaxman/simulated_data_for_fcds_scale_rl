"""Data forensics for Results §3.3–3.4: quasi-identifier uniqueness, blocking feasibility, sentinel checks, common names.

Pipeline tier, light (DuckDB over the released CSVs; a minute or two). Writes
``results/forensics.json``:

* ``uniqueness`` — among the registry's people (one row per simulant), the share
  whose first name + last name + date of birth is unique in the file, likewise
  last name + date of birth, and ZIP + date of birth + sex; and the share whose
  full name is shared with at least one other person;
* ``blocking`` — for each finder file against the registry, the naive comparison
  space, and for two blocking keys (full date of birth; last-name initial + year
  of birth) the number of candidate pairs and the share of true pairs the block
  keeps (pairs completeness);
* ``sentinels`` — per file: dates of birth blank and unparseable, "John/Jane Doe"
  names, repeated-digit SSNs and SSNs the SSA could not have issued;
* ``top_names`` — the ten commonest first and last names in the registry.

    uv run python pipeline/data_forensics.py
"""

from __future__ import annotations

import json
from pathlib import Path

import duckdb
import yaml

ROOT = Path(__file__).resolve().parent.parent
CFG = yaml.safe_load((ROOT / "config.yaml").read_text())
RELEASE = Path(CFG["paths"]["release_dir"])
RESULTS = ROOT / CFG["paths"]["results"]
READ_OPTS = "header=true, all_varchar=true, quote='\"'"
NORMALISE = """
    simulant_id,
    lower(trim(first_name)) AS fn, lower(trim(last_name)) AS ln, date_of_birth AS dob,
    lower(trim(sex)) AS sex, lower(trim(zipcode)) AS zip,
    nullif(replace(ssn, '-', ''), '') AS ssn, substr(date_of_birth, 7, 4) AS yob, substr(last_name, 1, 1) AS ln1
"""
FILES = ["registry.csv", "finder_500k.csv", "finder_100k.csv"]


def load(con, name, csv, one_per_simulant=False):
    q = f"SELECT {NORMALISE} FROM read_csv('{csv}', {READ_OPTS})"
    if one_per_simulant:
        q += " QUALIFY row_number() OVER (PARTITION BY simulant_id) = 1"
    con.execute(f"CREATE OR REPLACE TABLE {name} AS {q}")


def uniqueness(con) -> dict:
    out = {}
    for label, keys in [("name_dob", ["fn", "ln", "dob"]), ("lastname_dob", ["ln", "dob"]), ("zip_dob_sex", ["zip", "dob", "sex"])]:
        cols = ", ".join(keys)
        notnull = " AND ".join(f"{k} IS NOT NULL" for k in keys)
        unique_share = con.execute(f"""
            WITH k AS (SELECT {cols}, count(*) AS c FROM R1 WHERE {notnull} GROUP BY {cols})
            SELECT sum(c) FILTER (WHERE c = 1)::DOUBLE / (SELECT count(*) FROM R1) FROM k
        """).fetchone()[0]
        out[f"unique_{label}"] = unique_share
    shared = con.execute("""
        WITH k AS (SELECT fn, ln, count(*) AS c FROM R1 WHERE fn IS NOT NULL AND ln IS NOT NULL GROUP BY fn, ln)
        SELECT sum(c) FILTER (WHERE c >= 2), (SELECT count(*) FROM R1) FROM k
    """).fetchone()
    out["people_sharing_full_name"] = int(shared[0])
    out["share_sharing_full_name"] = shared[0] / shared[1]
    out["registry_people"] = int(shared[1])
    return out


def blocking(con) -> dict:
    n_r = con.execute("SELECT count(*) FROM R").fetchone()[0]
    n_f = con.execute("SELECT count(*) FROM F").fetchone()[0]
    out = {"naive_pairs": n_r * n_f}
    for label, keys in [("dob", ["dob"]), ("lastname_initial_yob", ["ln1", "yob"])]:
        cols = ", ".join(keys)
        notnull = " AND ".join(f"{k} IS NOT NULL" for k in keys)
        cand = con.execute(f"""
            SELECT sum(f.c * r.c) FROM
              (SELECT {cols}, count(*) AS c FROM F WHERE {notnull} GROUP BY {cols}) f
            JOIN (SELECT {cols}, count(*) AS c FROM R WHERE {notnull} GROUP BY {cols}) r USING ({cols})
        """).fetchone()[0]
        agree = " AND ".join(f"a.{k} = b.{k}" for k in keys)
        completeness = con.execute(f"""
            SELECT avg(CASE WHEN {agree} THEN 1 ELSE 0 END) FROM F a JOIN R b USING (simulant_id)
        """).fetchone()[0]
        out[f"block_{label}"] = {"candidate_pairs": int(cand), "pairs_completeness": completeness,
                                 "reduction_ratio": 1 - cand / (n_r * n_f)}
    return out


def sentinels(con, table) -> dict:
    row = con.execute(f"""
        SELECT count(*),
               avg((dob IS NULL)::INT),
               avg((try_strptime(dob, '%m/%d/%Y') IS NULL)::INT) FILTER (WHERE dob IS NOT NULL),
               count(*) FILTER (WHERE fn IN ('john', 'jane') AND ln = 'doe'),
               count(*) FILTER (WHERE ssn IN ('000000000', '111111111', '222222222', '333333333', '444444444',
                                              '555555555', '666666666', '777777777', '888888888', '999999999')),
               count(*) FILTER (WHERE ssn IS NOT NULL AND (substr(ssn, 1, 3) IN ('000', '666') OR substr(ssn, 1, 3) >= '900'
                                                          OR substr(ssn, 4, 2) = '00' OR substr(ssn, 6, 4) = '0000')),
               count(*) FILTER (WHERE ssn IS NOT NULL)
        FROM {table}
    """).fetchone()
    return {"rows": row[0], "dob_blank_share": row[1], "dob_unparseable_share_of_present": row[2],
            "doe_names": row[3], "ssn_repeated_digit": row[4], "ssn_not_issuable": row[5], "ssn_present": row[6]}


def top_names(con) -> dict:
    out = {}
    for col, key in (("fn", "first"), ("ln", "last")):
        rows = con.execute(f"SELECT {col}, count(*) AS c FROM R WHERE {col} IS NOT NULL GROUP BY {col} ORDER BY c DESC, {col} LIMIT 10").fetchall()
        out[key] = [{"name": r[0], "count": r[1]} for r in rows]
    return out


def main() -> None:
    con = duckdb.connect()
    load(con, "R", RELEASE / "registry.csv")
    load(con, "R1", RELEASE / "registry.csv", one_per_simulant=True)
    out = {"uniqueness": uniqueness(con), "top_names_registry": top_names(con), "blocking": {}, "sentinels": {}}
    out["sentinels"]["registry.csv"] = sentinels(con, "R")
    for finder in ("finder_500k.csv", "finder_100k.csv"):
        load(con, "F", RELEASE / finder)
        out["blocking"][finder] = blocking(con)
        out["sentinels"][finder] = sentinels(con, "F")
        print(finder, "blocking:", {k: (v if not isinstance(v, dict) else {kk: round(vv, 4) if isinstance(vv, float) else vv for kk, vv in v.items()}) for k, v in out["blocking"][finder].items()})
    print("uniqueness:", {k: round(v, 4) if isinstance(v, float) else v for k, v in out["uniqueness"].items()})
    print("sentinels registry:", out["sentinels"]["registry.csv"])
    (RESULTS / "forensics.json").write_text(json.dumps(out, indent=2) + "\n")
    print("wrote results/forensics.json")


if __name__ == "__main__":
    main()
