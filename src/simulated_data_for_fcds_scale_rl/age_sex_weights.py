"""Age/sex tables for the registry stand-in: the FCDS target shares and a validated rate loader.

``load_age_sex_targets`` reads the table named in ``config.yaml`` (``paths.age_sex_target``:
FCDS's reported cases by age and sex) into shares, and ``allocate_by_share`` turns them
into exact per-stratum quotas for the registry draw in ``pipeline/build_cohorts.py``.
``load_age_sex_weights`` reads any rate table with contiguous, exclusive-end age bins
(the same FCDS file, or the GBD prevalence table kept as the QA comparator) and recodes
sex to pseudopeople's ``Male``/``Female``; the 2026-08-12 build used it to weight a random
draw, which the exact quotas replaced on 2026-09-24 because weighted successive sampling
compresses weight ratios at a high sampling fraction.
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


def load_age_sex_targets(path: str | Path) -> pd.DataFrame:
    """Read a reference table with a ``count`` column into ``age_start, age_end, sex, share``.

    The shares (summing to 1) are the age/sex distribution the registry stand-in is
    drawn to match exactly, stratum by stratum; for the FCDS table they are the
    distribution of the cases FCDS reports. Bins and sex coding are validated as in
    ``load_age_sex_weights``.
    """
    path = Path(path)
    raw = pd.read_csv(path, comment="#")
    if "count" not in raw.columns:
        raise ValueError(f"{path}: no 'count' column to derive target shares from")
    bins = load_age_sex_weights(path)  # validates bins and recodes sex
    counts = pd.DataFrame(
        {
            "age_start": raw["age_start"].astype(int),
            "sex": raw["sex"].astype(str).str.strip().str.capitalize(),
            "count": raw["count"].astype(float),
        }
    )
    if counts["count"].isna().any() or (counts["count"] < 0).any() or counts["count"].sum() <= 0:
        raise ValueError(f"{path}: counts must be present, non-negative and not all zero")
    out = bins.drop(columns="weight").merge(counts, on=["age_start", "sex"], how="left")
    out["share"] = out["count"] / out["count"].sum()
    return out.drop(columns="count")


def allocate_by_share(shares: pd.Series, total: int, caps: pd.Series | None = None) -> pd.Series:
    """Split ``total`` across strata in proportion to ``shares``, as integers summing to ``total``.

    Largest-remainder rounding keeps the sum exact. ``caps`` (same index) are the
    number available per stratum: a stratum whose quota exceeds its cap is fixed
    at the cap and the excess is re-spread over the others in proportion to their
    shares, repeating until nothing is over cap. Raises ``ValueError`` if the caps
    cannot hold ``total`` at all.
    """
    if total < 0:
        raise ValueError("total must be non-negative")
    shares = shares.astype(float)
    if (shares < 0).any() or shares.sum() <= 0:
        raise ValueError("shares must be non-negative and not all zero")
    if caps is not None:
        caps = caps.reindex(shares.index).fillna(0).astype(int)
        if caps.sum() < total:
            raise ValueError(f"caps hold {int(caps.sum()):,} but {total:,} are requested")
    fixed = pd.Series(0, index=shares.index, dtype=int)
    free = pd.Series(True, index=shares.index)
    while True:
        remaining = total - int(fixed[~free].sum())
        w = shares.where(free, 0.0)
        raw = w / w.sum() * remaining if w.sum() > 0 else w * 0
        base = raw.astype(int)
        short = remaining - int(base.sum())
        order = (raw - base).sort_values(ascending=False).index
        base.loc[order[:short]] += 1
        quota = fixed.where(~free, base)
        if caps is None:
            return quota
        over = free & (quota > caps)
        if not over.any():
            return quota
        fixed = fixed.where(~over, caps)
        free = free & ~over
        if not free.any():
            if int(fixed.sum()) != total:
                raise ValueError("caps cannot hold the requested total")
            return fixed
