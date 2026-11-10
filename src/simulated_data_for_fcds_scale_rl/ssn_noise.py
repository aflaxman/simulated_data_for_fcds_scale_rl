"""Targeted SSN noise: missingness by target count, adjacent-digit transposition, one wrong digit.

pseudopeople's noise taxonomy has no adjacent-digit SSN transposition, so it is
applied by hand after clean SSNs are joined from the Social Security observer —
the concrete affordance gap the paper's Discussion generalises.

Missingness is set by target *count*, not an independent Bernoulli draw: count
what is already missing (simulants who never held an SSN in the source
population) and blank only the shortfall. When the structural rate already
exceeds the target, nothing further is blanked — the v0.2 registry landed at
5.77% against its 5% target this way, while the finder files were topped up to
exactly 20%. One mechanism, two outcomes (paper §3.3).

RNG discipline: one numpy Generator per file, missingness drawn first,
transposition second and the wrong digit third, over a series whose row order
the caller has already pinned (sorted by simulant_id). A mechanism whose rate is
zero draws nothing, so switching one on leaves the earlier draws, and every other
file, exactly as they were (the registry's wrong digit was added this way for
v0.4, 2026-11-09, at the second author's request).
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def swap_adjacent_digits(value, rng: np.random.Generator):
    """Swap one randomly chosen adjacent pair of digits, preserving non-digits.

    ``123-45-6789`` can become ``213-45-6789`` but never loses its dashes;
    values with fewer than two digits (and NA) come back unchanged.
    """
    if pd.isna(value):
        return value
    s = str(value)
    digits = [ch for ch in s if ch.isdigit()]
    if len(digits) < 2:
        return s
    i = int(rng.integers(0, len(digits) - 1))
    digits[i], digits[i + 1] = digits[i + 1], digits[i]
    it = iter(digits)
    return "".join(next(it) if ch.isdigit() else ch for ch in s)


def replace_one_digit(value, rng: np.random.Generator):
    """Replace one randomly chosen digit with a different digit, preserving non-digits.

    ``123-45-6789`` can become ``123-45-6289`` but never keeps the same number, so a
    hit always changes the value (unlike pseudopeople's ``write_wrong_digits``, whose
    per-digit token probability leaves many hit cells unchanged). NA comes back as is.
    """
    if pd.isna(value):
        return value
    s = str(value)
    positions = [i for i, ch in enumerate(s) if ch.isdigit()]
    if not positions:
        return s
    i = positions[int(rng.integers(0, len(positions)))]
    new = str((int(s[i]) + int(rng.integers(1, 10))) % 10)  # any digit but the current one
    return s[:i] + new + s[i + 1:]


def apply_targeted_ssn_noise(
    ssn: pd.Series,
    *,
    missing_target_rate: float,
    transposed_rate: float,
    rng: np.random.Generator,
    wrong_digit_rate: float = 0.0,
) -> tuple[pd.Series, dict]:
    """Blank SSNs up to the target count, transpose digits in a share of the rest, then put one
    wrong digit in another share.

    Returns the noised series and a stats dict recording the structural
    missingness found, how many values were blanked and transposed, whether the
    structural floor exceeded the target (the caller should warn), and the
    realised missing rate.
    """
    ssn = ssn.copy()
    total = len(ssn)
    structural_missing = int(ssn.isna().sum())
    target_count = int(total * missing_target_rate)
    to_remove = target_count - structural_missing

    if to_remove > 0:
        present = ssn.index[ssn.notna()].to_numpy()
        remove = rng.choice(present, size=to_remove, replace=False)
        ssn.loc[remove] = pd.NA

    transposed = 0
    if transposed_rate > 0:
        valid = ssn.notna()
        n_valid = int(valid.sum())
        if n_valid > 0:
            transpose_mask = rng.random(n_valid) < transposed_rate
            target_idx = ssn.index[valid][transpose_mask]
            ssn.loc[target_idx] = [swap_adjacent_digits(v, rng) for v in ssn.loc[target_idx]]
            transposed = int(len(target_idx))

    wrong_digit = 0
    if wrong_digit_rate > 0:
        valid = ssn.notna()
        n_valid = int(valid.sum())
        if n_valid > 0:
            wrong_mask = rng.random(n_valid) < wrong_digit_rate
            target_idx = ssn.index[valid][wrong_mask]
            ssn.loc[target_idx] = [replace_one_digit(v, rng) for v in ssn.loc[target_idx]]
            wrong_digit = int(len(target_idx))

    stats = {
        "n": total,
        "structural_missing": structural_missing,
        "target_missing": target_count,
        "blanked": max(to_remove, 0),
        "structural_exceeds_target": bool(to_remove < 0),
        "realised_missing_rate": float(ssn.isna().mean()),
        "transposed": transposed,
        "wrong_digit": wrong_digit,
    }
    return ssn, stats
