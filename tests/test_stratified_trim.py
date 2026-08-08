"""stratified_trim must hit every design target exactly.

The v0.2 build's unstratified trim overshot its overlap targets by roughly a
third, because unchosen overlap survivors re-entered through the filler draws
and the registry kept the whole surviving pool. These tests pin the corrected
behaviour on a small analogue of the real cohort design: oversampled draws,
independent per-file omission, then the trim.
"""

import numpy as np
import pytest

from simulated_data_for_fcds_scale_rl.downsample import stratified_trim

REGISTRY_TARGET = 5_000
FINDER_A_TARGET = 1_000
FINDER_B_TARGET = 200
OVERLAP_A_TARGET = 200
OVERLAP_B_TARGET = 40
OVERSAMPLE = 1.5


def make_survivors(seed=12345, omission=0.08):
    """Oversampled cohorts with designed overlap, after per-file omission."""
    rng = np.random.default_rng(seed)
    universe = np.array([f"sim_{i}" for i in range(50_000)])

    registry_draw = rng.choice(universe, int(REGISTRY_TARGET * OVERSAMPLE), replace=False)
    outside = np.setdiff1d(universe, registry_draw)

    def finder_draw(finder_target, overlap_target):
        n_overlap = int(overlap_target * OVERSAMPLE)
        n_rest = int(finder_target * OVERSAMPLE) - n_overlap
        return np.concatenate([
            rng.choice(registry_draw, n_overlap, replace=False),
            rng.choice(outside, n_rest, replace=False),
        ])

    def omit(ids):
        return set(ids[rng.random(len(ids)) >= omission])

    return (
        omit(registry_draw),
        omit(finder_draw(FINDER_A_TARGET, OVERLAP_A_TARGET)),
        omit(finder_draw(FINDER_B_TARGET, OVERLAP_B_TARGET)),
    )


def trim(survivors, seed=999):
    return stratified_trim(
        *survivors,
        registry_target=REGISTRY_TARGET,
        finder_a_target=FINDER_A_TARGET,
        finder_b_target=FINDER_B_TARGET,
        overlap_a_target=OVERLAP_A_TARGET,
        overlap_b_target=OVERLAP_B_TARGET,
        seed=seed,
    )


def test_targets_hit_exactly():
    survivors = make_survivors()
    registry_ids, a_ids, b_ids = survivors

    # The v0.2 overshoot precondition: more overlap survivors than the target,
    # so an unstratified trim would overshoot here too.
    assert len(registry_ids & a_ids) > OVERLAP_A_TARGET
    assert len(registry_ids & b_ids) > OVERLAP_B_TARGET

    ids = trim(survivors)
    assert len(ids["registry"]) == REGISTRY_TARGET
    assert len(ids["finder_a"]) == FINDER_A_TARGET
    assert len(ids["finder_b"]) == FINDER_B_TARGET
    assert len(ids["registry"] & ids["finder_a"]) == OVERLAP_A_TARGET
    assert len(ids["registry"] & ids["finder_b"]) == OVERLAP_B_TARGET
    assert not ids["finder_a"] & ids["finder_b"]


def test_outputs_are_survivors():
    survivors = make_survivors()
    registry_ids, a_ids, b_ids = survivors
    ids = trim(survivors)
    assert ids["registry"] <= registry_ids
    assert ids["finder_a"] <= a_ids
    assert ids["finder_b"] <= b_ids


def test_deterministic_given_seed():
    assert trim(make_survivors(), seed=999) == trim(make_survivors(), seed=999)
    assert trim(make_survivors(), seed=999) != trim(make_survivors(), seed=1000)


def test_duplicate_input_ids_tolerated():
    registry_ids, a_ids, b_ids = make_survivors()
    doubled = list(registry_ids) * 2
    ids = trim((doubled, a_ids, b_ids))
    assert len(ids["registry"]) == REGISTRY_TARGET
    assert len(ids["registry"] & ids["finder_a"]) == OVERLAP_A_TARGET


def test_insufficient_overlap_pool_raises():
    # Omission heavy enough that fewer than OVERLAP_A_TARGET overlap members
    # survive in both files: the trim must refuse, naming the remedy.
    survivors = make_survivors(omission=0.75)
    with pytest.raises(ValueError, match="oversample"):
        trim(survivors)


def test_inconsistent_targets_raise():
    survivors = make_survivors()
    with pytest.raises(ValueError):
        stratified_trim(
            *survivors,
            registry_target=REGISTRY_TARGET,
            finder_a_target=100,
            finder_b_target=FINDER_B_TARGET,
            overlap_a_target=200,  # exceeds its finder-file target
            overlap_b_target=OVERLAP_B_TARGET,
            seed=999,
        )
