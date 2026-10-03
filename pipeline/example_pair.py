"""Pick worked-example simulants: the same person in the registry and in the 500k finder file.

Pipeline tier, light: one DuckDB join of the 100,000 overlap simulants, then
Python over the matched pairs. Writes ``results/example_pair.csv`` — two rows
per chosen simulant (source = registry / finder_500k) over the released
columns, plus a ``discrepancies`` column naming each differing field and the
mechanism it looks like (``record_diff.classify``).

Selection is deterministic and profile-driven (author's spec, 2026-09-25): one
pair where the first name is a verified nickname of the other, one where two or
more address fields differ, and one with a month/day swap and an SSN digit swap
together; within each profile the pair showing the most distinct mechanisms wins,
ties broken by simulant_id, and no pair may have more than ``MAX_DIFFS``
differing fields so the panel stays readable. A true match's two records are the
same census record noised twice, so an address "change" here is noise on the
address fields, never a move. Pass ``--ids`` to pin simulants instead.

    uv run python pipeline/example_pair.py [--ids ID ...]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import duckdb
import pandas as pd
import yaml

from simulated_data_for_fcds_scale_rl.record_diff import classify

ROOT = Path(__file__).resolve().parent.parent
CFG = yaml.safe_load((ROOT / "config.yaml").read_text())
RELEASE = Path(CFG["paths"]["release_dir"])
RESULTS = ROOT / CFG["paths"]["results"]
READ_OPTS = "header=true, all_varchar=true, quote='\"'"
FIELDS = ["first_name", "middle_initial", "last_name", "date_of_birth", "sex", "race_ethnicity",
          "street_number", "street_name", "unit_number", "city", "state", "zipcode", "ssn"]
ADDRESS_FIELDS = {"street_number", "street_name", "city", "zipcode"}
CHANGED = {"typo", "digits changed", "different value"}
MAX_DIFFS = 5


def has(d, field, label):
    return any(f == field and lab == label for f, lab in d)


def address_changes(d):
    return sum(1 for f, lab in d if f in ADDRESS_FIELDS and lab in CHANGED)


PROFILES = [
    ("nickname", lambda d: has(d, "first_name", "nickname") and len(d) >= 2),
    ("address", lambda d: address_changes(d) >= 2 and not any(f in ("first_name", "last_name", "date_of_birth") for f, _ in d)),
    ("dates and digits", lambda d: has(d, "date_of_birth", "month and day swapped") and has(d, "ssn", "adjacent digits swapped")),
]


def matched_pairs(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    reg, fin = RELEASE / "registry.csv", RELEASE / "finder_500k.csv"
    cols_r = ", ".join(f"r.{c} AS r_{c}" for c in FIELDS)
    cols_f = ", ".join(f"f.{c} AS f_{c}" for c in FIELDS)
    return con.execute(f"""
        WITH r AS (SELECT * FROM read_csv('{reg}', {READ_OPTS})
                   QUALIFY row_number() OVER (PARTITION BY simulant_id) = 1),
             f AS (SELECT * FROM read_csv('{fin}', {READ_OPTS})
                   QUALIFY row_number() OVER (PARTITION BY simulant_id) = 1)
        SELECT r.simulant_id, {cols_r}, {cols_f}, r.diagnosis_date AS r_diagnosis_date
        FROM r JOIN f USING (simulant_id)
        ORDER BY r.simulant_id
    """).df()


def diffs(row: pd.Series) -> list[tuple[str, str]]:
    out = []
    for c in FIELDS:
        label = classify(c, row[f"r_{c}"], row[f"f_{c}"])
        if label:
            out.append((c, label))
    return out


def richness(d: list[tuple[str, str]]) -> int:
    """How many distinct mechanisms a pair shows (blanks count once)."""
    return len({lab for _, lab in d})


def choose(pairs: pd.DataFrame) -> list[tuple[str, list[tuple[str, str]]]]:
    cands = []
    for _, row in pairs.iterrows():
        d = diffs(row)
        if 1 <= len(d) <= MAX_DIFFS:
            cands.append((row["simulant_id"], d))
    chosen, used = [], set()
    for name, fits in PROFILES:
        pool = [c for c in cands if c[0] not in used and fits(c[1])]
        if not pool:
            print(f"no readable pair fits profile '{name}'")
            continue
        best = max(pool, key=lambda c: (richness(c[1]), len(c[1]), c[0] and -1 * 0))  # richest, then most fields
        best = sorted([c for c in pool if (richness(c[1]), len(c[1])) == (richness(best[1]), len(best[1]))], key=lambda c: c[0])[0]
        chosen.append(best)
        used.add(best[0])
        print(f"profile '{name}': {len(pool):,} candidates")
    return chosen


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ids", nargs="*", default=None, help="pin these simulant_ids instead of searching")
    args = ap.parse_args()
    con = duckdb.connect()
    pairs = matched_pairs(con)
    print(f"{len(pairs):,} simulants appear in both files")
    if args.ids:
        sel = pairs[pairs["simulant_id"].isin(args.ids)]
        chosen = [(r["simulant_id"], diffs(r)) for _, r in sel.iterrows()]
    else:
        chosen = choose(pairs)
    rows = []
    for k, (sid, d) in enumerate(chosen, 1):
        row = pairs[pairs["simulant_id"] == sid].iloc[0]
        note = "; ".join(f"{f}: {lab}" for f, lab in d)
        for source, prefix in (("registry", "r_"), ("finder_500k", "f_")):
            rows.append({"pair": k, "simulant_id": sid, "source": source,
                         **{c: row[f"{prefix}{c}"] for c in FIELDS},
                         "diagnosis_date": row["r_diagnosis_date"] if source == "registry" else "",
                         "discrepancies": note})
        print(f"pair {k}: {sid}: {note}")
    pd.DataFrame(rows).to_csv(RESULTS / "example_pair.csv", index=False)
    print("wrote results/example_pair.csv")


if __name__ == "__main__":
    main()
