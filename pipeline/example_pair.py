"""Pick worked-example simulants: the same person in the registry and in the 500k finder file.

Pipeline tier, light: one DuckDB join of the 100,000 overlap simulants, then
Python over the matched pairs. Writes ``results/example_pair.csv`` — two rows
per chosen simulant (source = registry / finder_500k) over the released
columns, plus a ``discrepancies`` column naming each differing field and the
mechanism it looks like (``record_diff.classify``).

Selection is deterministic (ordered by simulant_id) and greedy: it takes the
fewest pairs, each with at most ``MAX_DIFFS`` differing fields so the panel
stays readable, that together show every mechanism in ``WANTED``. Pass
``--ids`` to pin simulants chosen earlier so Table 2 stays stable.

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
WANTED = [
    ("first_name", "nickname or different name"),
    ("*", "typo"),
    ("date_of_birth", "month and day swapped"),
    ("ssn", "adjacent digits swapped"),
    ("*", "blank"),
]
MAX_DIFFS = 4
MAX_PAIRS = 3


def matched_pairs(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    reg, fin = RELEASE / "registry.csv", RELEASE / "finder_500k.csv"
    cols_r = ", ".join(f"r.{c} AS r_{c}" for c in FIELDS)
    cols_f = ", ".join(f"f.{c} AS f_{c}" for c in FIELDS)
    return con.execute(f"""
        WITH r AS (SELECT * FROM read_csv('{reg}', {READ_OPTS})
                   QUALIFY row_number() OVER (PARTITION BY simulant_id) = 1),
             f AS (SELECT * FROM read_csv('{fin}', {READ_OPTS})
                   QUALIFY row_number() OVER (PARTITION BY simulant_id) = 1)
        SELECT r.simulant_id, {cols_r}, {cols_f}
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


def covers(d: list[tuple[str, str]], want: tuple[str, str]) -> bool:
    field, label = want
    return any(lab == label and (field == "*" or fld == field) for fld, lab in d)


def choose(pairs: pd.DataFrame) -> list[tuple[str, list[tuple[str, str]]]]:
    cands = []
    for _, row in pairs.iterrows():
        d = diffs(row)
        if 1 <= len(d) <= MAX_DIFFS:
            cands.append((row["simulant_id"], d))
    chosen, uncovered = [], list(WANTED)
    while uncovered and len(chosen) < MAX_PAIRS:
        best = max(cands, key=lambda c: (sum(covers(c[1], w) for w in uncovered), -len(c[1]), c[0] * -1 if False else 0))
        gain = sum(covers(best[1], w) for w in uncovered)
        if gain == 0:
            break
        chosen.append(best)
        uncovered = [w for w in uncovered if not covers(best[1], w)]
        cands = [c for c in cands if c[0] != best[0]]
    if uncovered:
        print("not all mechanisms found in readable pairs; missing:", uncovered)
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
                         **{c: row[f"{prefix}{c}"] for c in FIELDS}, "discrepancies": note})
        print(f"pair {k}: {sid}: {note}")
    pd.DataFrame(rows).to_csv(RESULTS / "example_pair.csv", index=False)
    print("wrote results/example_pair.csv")


if __name__ == "__main__":
    main()
