"""Targeted SSN noise must hit its missingness target exactly and transpose safely."""

import numpy as np
import pandas as pd

from simulated_data_for_fcds_scale_rl.ssn_noise import (
    apply_targeted_ssn_noise,
    replace_one_digit,
    swap_adjacent_digits,
)


def make_ssns(n=10_000, structural_missing=0.03, seed=7):
    rng = np.random.default_rng(seed)
    vals = [
        f"{rng.integers(100, 900):03d}-{rng.integers(10, 99):02d}-{rng.integers(1000, 9999):04d}"
        for _ in range(n)
    ]
    s = pd.Series(vals, dtype="object")
    s[s.sample(frac=structural_missing, random_state=seed).index] = pd.NA
    return s


def test_missingness_topped_up_to_exact_target():
    s = make_ssns()
    out, stats = apply_targeted_ssn_noise(
        s, missing_target_rate=0.20, transposed_rate=0.0, rng=np.random.default_rng(1)
    )
    assert int(out.isna().sum()) == int(len(s) * 0.20)
    assert not stats["structural_exceeds_target"]
    assert stats["realised_missing_rate"] == 0.20


def test_structural_floor_leaves_missingness_alone():
    # The registry case: more simulants never held an SSN than the target asks
    # to blank, so nothing further is removed and the caller is told to warn.
    s = make_ssns(structural_missing=0.10)
    out, stats = apply_targeted_ssn_noise(
        s, missing_target_rate=0.05, transposed_rate=0.0, rng=np.random.default_rng(1)
    )
    assert int(out.isna().sum()) == int(s.isna().sum())
    assert stats["structural_exceeds_target"]
    assert stats["blanked"] == 0


def test_transposition_preserves_digits_and_format():
    s = make_ssns(structural_missing=0.0)
    out, stats = apply_targeted_ssn_noise(
        s, missing_target_rate=0.0, transposed_rate=1.0, rng=np.random.default_rng(1)
    )
    assert stats["transposed"] == len(s)
    for before, after in zip(s, out):
        assert sorted(before.replace("-", "")) == sorted(after.replace("-", ""))
        assert [i for i, c in enumerate(after) if c == "-"] == [3, 6]


def test_deterministic_given_seed():
    s = make_ssns()
    a, _ = apply_targeted_ssn_noise(
        s, missing_target_rate=0.2, transposed_rate=0.01, rng=np.random.default_rng(9)
    )
    b, _ = apply_targeted_ssn_noise(
        s, missing_target_rate=0.2, transposed_rate=0.01, rng=np.random.default_rng(9)
    )
    assert a.equals(b)


def test_wrong_digit_changes_exactly_one_digit_and_keeps_the_format():
    s = make_ssns(structural_missing=0.0)
    out, stats = apply_targeted_ssn_noise(
        s, missing_target_rate=0.0, transposed_rate=0.0, wrong_digit_rate=1.0, rng=np.random.default_rng(3)
    )
    assert stats["wrong_digit"] == len(s)
    for before, after in zip(s, out):
        assert [i for i, c in enumerate(after) if c == "-"] == [3, 6]
        assert sum(a != b for a, b in zip(before, after)) == 1
        assert after != before


def test_wrong_digit_rate_is_honoured_and_a_zero_rate_draws_nothing():
    s = make_ssns(n=200_000, structural_missing=0.0)
    out, stats = apply_targeted_ssn_noise(
        s, missing_target_rate=0.0, transposed_rate=0.0, wrong_digit_rate=0.005, rng=np.random.default_rng(5)
    )
    assert 0.004 <= stats["wrong_digit"] / len(s) <= 0.006
    # with the rate at zero the output equals the pre-wrong-digit behaviour draw for draw
    s2 = make_ssns()
    a, _ = apply_targeted_ssn_noise(s2, missing_target_rate=0.2, transposed_rate=0.01, rng=np.random.default_rng(9))
    b, _ = apply_targeted_ssn_noise(s2, missing_target_rate=0.2, transposed_rate=0.01, wrong_digit_rate=0.0, rng=np.random.default_rng(9))
    assert a.equals(b)


def test_swap_handles_edge_values():
    rng = np.random.default_rng(0)
    assert swap_adjacent_digits("7", rng) == "7"
    assert pd.isna(swap_adjacent_digits(pd.NA, rng))
    assert pd.isna(replace_one_digit(pd.NA, rng))
    assert replace_one_digit("abc", rng) == "abc"
