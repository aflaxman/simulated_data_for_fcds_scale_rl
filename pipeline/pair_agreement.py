"""Field-level agreement between the two records of each true match: the difficulty portrait's core.

Pipeline tier, light (one DuckDB join per finder file, seconds). For every
released field, the share of true matches (registry row and finder row of the
same simulant) whose values agree exactly when both are present, and the share
with a blank on either side; plus the two summaries the deterministic ladder
turns on — exact agreement on first name, last name and date of birth together
(a blank counts as disagreement) and the share of pairs with a usable,
agreeing SSN. Writes ``results/pair_agreement.json`` for §3.3 (Table 5).

    uv run python pipeline/pair_agreement.py
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
FIELDS = ["first_name", "middle_initial", "last_name", "date_of_birth", "sex", "race_ethnicity",
          "street_number", "street_name", "unit_number", "city", "state", "zipcode", "ssn"]


def present(alias: str, f: str) -> str:
    return f"({alias}.{f} IS NOT NULL AND {alias}.{f} <> '')"


def main() -> None:
    con = duckdb.connect()
    out = {}
    for finder in ("finder_500k.csv", "finder_100k.csv"):
        sel = ", ".join(
            f"avg(CASE WHEN {present('r', f)} AND {present('f', f)} THEN (r.{f} = f.{f})::INT END) AS agree_{f}, "
            f"avg((NOT ({present('r', f)} AND {present('f', f)}))::INT) AS blank_{f}"
            for f in FIELDS
        )
        name_dob = " AND ".join(f"{present('r', f)} AND {present('f', f)} AND r.{f} = f.{f}"
                                for f in ("first_name", "last_name", "date_of_birth"))
        row = con.execute(f"""
            WITH r AS (SELECT * FROM read_csv('{RELEASE / "registry.csv"}', {READ_OPTS})
                       QUALIFY row_number() OVER (PARTITION BY simulant_id) = 1),
                 f AS (SELECT * FROM read_csv('{RELEASE / finder}', {READ_OPTS})
                       QUALIFY row_number() OVER (PARTITION BY simulant_id) = 1)
            SELECT count(*) AS pairs, {sel},
                   avg(({name_dob})::INT) AS name_dob_all_agree,
                   avg(({present('r', 'ssn')} AND {present('f', 'ssn')} AND r.ssn = f.ssn)::INT) AS ssn_usable_and_agree
            FROM r JOIN f USING (simulant_id)
        """).df().iloc[0]
        out[finder] = {
            "pairs": int(row["pairs"]),
            "fields": {f: {"agree_when_both_present": float(row[f"agree_{f}"]),
                           "blank_on_either_side": float(row[f"blank_{f}"])} for f in FIELDS},
            "name_dob_all_agree": float(row["name_dob_all_agree"]),
            "ssn_usable_and_agree": float(row["ssn_usable_and_agree"]),
        }
        print(f"{finder}: {int(row['pairs']):,} true matches; name+DOB all agree {row['name_dob_all_agree']:.3f}; "
              f"SSN usable and agreeing {row['ssn_usable_and_agree']:.3f}")
        for f in ("first_name", "last_name", "date_of_birth", "street_name", "ssn"):
            print(f"  {f:14} agree {row[f'agree_{f}']:.3f}  blank {row[f'blank_{f}']:.3f}")
    # Per-file blank shares for every released field (the error-structure table in Results §3.3
    # sets them against the rates that were configured).
    blank_by_file = {}
    for fname in ("registry.csv", "finder_500k.csv", "finder_100k.csv"):
        sel = ", ".join(f"avg((NOT {present('r', f)})::INT) AS {f}" for f in FIELDS)
        row = con.execute(f"SELECT {sel} FROM read_csv('{RELEASE / fname}', {READ_OPTS}) r").df().iloc[0]
        blank_by_file[fname] = {f: float(row[f]) for f in FIELDS}
    out["blank_share_by_file"] = blank_by_file
    (RESULTS / "pair_agreement.json").write_text(json.dumps(out, indent=2) + "\n")
    print("wrote results/pair_agreement.json")


if __name__ == "__main__":
    main()
