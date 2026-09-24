"""Age- and sex-specific sampling weights for the registry stand-in.

The registry draw in ``pipeline/build_cohorts.py`` is weighted sampling without
replacement (Efraimidis-Spirakis keyed-hash draws), so only the *relative* weights
matter and any rate table with contiguous, exclusive-end age bins by sex will do.
Which table is used is named in ``config.yaml`` (``paths.age_sex_weights``): since
2026-09-24 that is the FCDS age- and sex-specific cancer incidence table; the v0.3
build used GBD all-neoplasm prevalence for Florida, which stays in ``reference/``
as the comparator for the age/sex QA figure.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {"age_start", "age_end", "sex"}
# The first of these present in the table is taken as the weight column.
WEIGHT_COLUMNS = ("rate", "prevalence_pct")
# pseudopeople's coding of sex, which the census extract joins on.
SEXES = ("Female", "Male")


def load_age_sex_weights(path: str | Path) -> pd.DataFrame:
    """Read a reference rate table into ``age_start, age_end, sex, weight``.

    ``age_end`` is exclusive; sex is recoded to pseudopeople's ``Male``/``Female``.
    The weight is the table's rate as given (per 100,000 for the FCDS table,
    percent for the GBD table) and is deliberately not rescaled: its scale is
    irrelevant to weighted sampling, and leaving it alone means it can never be
    mistaken for a probability. Raises ``ValueError`` if the bins of either sex
    do not start at age 0 or leave a gap, or if a weight is missing or negative.
    """
    path = Path(path)
    raw = pd.read_csv(path, comment="#")
    missing = REQUIRED_COLUMNS - set(raw.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")
    weight_col = next((c for c in WEIGHT_COLUMNS if c in raw.columns), None)
    if weight_col is None:
        raise ValueError(f"{path}: no weight column; expected one of {WEIGHT_COLUMNS}")

    out = pd.DataFrame(
        {
            "age_start": raw["age_start"].astype(int),
            "age_end": raw["age_end"].astype(int),
            "sex": raw["sex"].astype(str).str.strip().str.capitalize(),
            "weight": raw[weight_col].astype(float),
        }
    )
    unknown_sex = set(out["sex"]) - set(SEXES)
    if unknown_sex:
        raise ValueError(f"{path}: unrecognised sex values {sorted(unknown_sex)}")
    if out["weight"].isna().any() or (out["weight"] < 0).any():
        raise ValueError(f"{path}: weights must be present and non-negative")

    out = out.sort_values(["sex", "age_start"]).reset_index(drop=True)
    for sex, bins in out.groupby("sex"):
        if bins["age_start"].iloc[0] != 0:
            raise ValueError(f"{path}: {sex} bins must start at age 0")
        if (bins["age_end"].to_numpy()[:-1] != bins["age_start"].to_numpy()[1:]).any():
            raise ValueError(f"{path}: {sex} bins must be contiguous (age_end is exclusive)")
        if (bins["age_end"] <= bins["age_start"]).any():
            raise ValueError(f"{path}: {sex} has an empty age bin")
    return out
