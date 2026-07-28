"""Deterministic-linkage baselines on the released benchmark.

Links each finder file against the registry with a ladder of exact-match rules
and scores every candidate pair against the ``simulant_id`` ground truth, which
is published alongside the identifying fields precisely so that this is possible.

Writes ``results/linkage_baseline.json`` — small enough to commit, and the only
thing the paper reads. Run it from the repo root:

    uv run python pipeline/linkage_baseline.py

The whole thing is a handful of hash joins over 5M rows, so it finishes in well
under a minute on one node; it does not need srun.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import duckdb
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = yaml.safe_load((ROOT / "config.yaml").read_text())
RELEASE = Path(CONFIG["paths"]["release_dir"])
RESULTS = ROOT / CONFIG["paths"]["results"]

FINDERS = ["finder_100k.csv", "finder_500k.csv"]
REGISTRY = "registry.csv"

# A record pair is a predicted link when it agrees on every key of any one
# key-set. Expressing rules this way keeps each one a hash join; the disjunctive
# rules become a UNION rather than an OR, which would force a nested-loop join
# over 5e11 pairs.
RULES: list[tuple[str, str, list[list[str]]]] = [
    ("name_dob", "First + last name and full date of birth",
     [["fn", "ln", "dob"]]),
    ("name_dob_sex", "First + last name, full date of birth and sex",
     [["fn", "ln", "dob", "sex"]]),
    ("ssn_only", "Social Security Number alone",
     [["ssn"]]),
    ("fcds_min_ssn", "FCDS minimum rule: first + last name, SSN and sex",
     [["fn", "ln", "ssn", "sex"]]),
    ("fcds_min_monthyear", "FCDS minimum rule: first + last name, month and year of birth, and sex",
     [["fn", "ln", "mob", "yob", "sex"]]),
    ("fcds_min_either", "Either FCDS minimum rule",
     [["fn", "ln", "ssn", "sex"], ["fn", "ln", "mob", "yob", "sex"]]),
    ("fcds_current_dob_ssn", "Current FCDS layout rule: name, sex, date of birth and SSN",
     [["fn", "ln", "sex", "dob", "ssn"]]),
    ("name_dob_or_ssn", "First + last name and date of birth, or SSN",
     [["fn", "ln", "dob"], ["ssn"]]),
    ("lastname_dob", "Last name and date of birth only",
     [["ln", "dob"]]),
]

# Quoted fields are rare enough in these CSVs that DuckDB's sniffer infers
# quote=(empty) and then fails on the few values containing a comma, such as a
# street_number of "64,66". Naming the quote character explicitly is required.
READ_OPTS = "header=true, all_varchar=true, quote='\"'"

NORMALISE = """
    simulant_id, rid,
    lower(trim(first_name)) AS fn,
    lower(trim(last_name))  AS ln,
    date_of_birth           AS dob,
    lower(trim(sex))        AS sex,
    nullif(replace(ssn, '-', ''), '') AS ssn,
    substr(date_of_birth, 1, 2) AS mob,
    substr(date_of_birth, 7, 4) AS yob
"""


def load(con: duckdb.DuckDBPyConnection, name: str, csv: Path) -> None:
    con.execute(
        f"CREATE OR REPLACE TABLE {name}_raw AS "
        f"SELECT *, row_number() OVER () AS rid FROM read_csv('{csv}', {READ_OPTS})"
    )
    con.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT {NORMALISE} FROM {name}_raw")


def evaluate(con: duckdb.DuckDBPyConnection, keysets: list[list[str]], truth_pairs: int) -> dict:
    parts = []
    for keys in keysets:
        on = " AND ".join(f"a.{k} = b.{k}" for k in keys)
        # A blank field must never link. SQL equality already yields NULL rather
        # than true, but the explicit filter documents the intent and lets the
        # planner drop the rows early.
        notnull = " AND ".join(f"a.{k} IS NOT NULL" for k in keys)
        parts.append(
            f"SELECT a.rid AS rid_f, b.rid AS rid_r, a.simulant_id AS sid_f, "
            f"b.simulant_id AS sid_r FROM F a JOIN R b ON {on} WHERE {notnull}"
        )
    predicted, tp, rows_matched, rows_correct = con.execute(f"""
        WITH pairs AS ({" UNION ".join(parts)})
        SELECT count(*),
               count(*) FILTER (WHERE sid_f = sid_r),
               count(DISTINCT rid_f),
               count(DISTINCT rid_f) FILTER (WHERE sid_f = sid_r)
        FROM pairs
    """).fetchone()

    precision = tp / predicted if predicted else float("nan")
    recall = tp / truth_pairs if truth_pairs else float("nan")
    return {
        "predicted_pairs": predicted,
        "true_positives": tp,
        "false_positives": predicted - tp,
        "false_negatives": truth_pairs - tp,
        "precision": precision,
        "recall": recall,
        "f1": (2 * precision * recall / (precision + recall)) if tp else 0.0,
        "finder_rows_matched": rows_matched,
        "finder_rows_matched_correctly": rows_correct,
    }


def main() -> None:
    con = duckdb.connect()
    con.execute("PRAGMA threads=8")

    out: dict = {
        "dataset_version": CONFIG["dataset"]["version"],
        "duckdb_version": duckdb.__version__,
        "finder_files": {},
    }

    load(con, "R", RELEASE / REGISTRY)
    out["registry"] = {
        "rows": con.execute("SELECT count(*) FROM R").fetchone()[0],
        "simulants": con.execute("SELECT count(DISTINCT simulant_id) FROM R").fetchone()[0],
        "ssn_missing": con.execute(
            "SELECT avg(CASE WHEN ssn IS NULL THEN 1.0 ELSE 0 END) FROM R").fetchone()[0],
    }

    for finder in FINDERS:
        t0 = time.time()
        load(con, "F", RELEASE / finder)
        truth_pairs = con.execute(
            "SELECT count(*) FROM F a JOIN R b USING (simulant_id)").fetchone()[0]

        entry = {
            "rows": con.execute("SELECT count(*) FROM F").fetchone()[0],
            "simulants": con.execute("SELECT count(DISTINCT simulant_id) FROM F").fetchone()[0],
            "ssn_missing": con.execute(
                "SELECT avg(CASE WHEN ssn IS NULL THEN 1.0 ELSE 0 END) FROM F").fetchone()[0],
            "true_pairs": truth_pairs,
            "rules": [],
        }
        for key, label, keysets in RULES:
            scores = evaluate(con, keysets, truth_pairs)
            entry["rules"].append({"rule": key, "label": label, "keysets": keysets, **scores})
            print(f"{finder:16s} {key:22s} P={scores['precision']:.4f} "
                  f"R={scores['recall']:.4f} F1={scores['f1']:.4f}", flush=True)
        entry["seconds"] = round(time.time() - t0, 1)
        out["finder_files"][finder] = entry

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "linkage_baseline.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"wrote {RESULTS / 'linkage_baseline.json'}")


if __name__ == "__main__":
    main()
