"""Exact-target trimming of oversampled, noised cohorts.

pseudopeople's row-level omission noise drops an unpredictable number of rows,
so cohorts are drawn oversize (``cohorts.oversample`` in ``config.yaml``) and
trimmed back to their design targets afterwards. The trim must be *stratified*:
overlap members and filler are selected separately, and every filler draw
excludes the entire surviving overlap pool, not just the members chosen from
it.

Dataset v0.2 trimmed unstratified — the registry kept every surviving overlap
candidate, and finder filler was drawn from a pool that still contained the
unchosen candidates — so realised overlaps overshot their targets by roughly a
third (129,356 against 100,000) and the two finder files accidentally shared
2,508 simulants. ``stratified_trim`` makes those counts exact by construction;
``tests/test_stratified_trim.py`` holds it to that.

Targets are counts of *simulants*. Row counts can exceed simulant counts when
pseudopeople's duplication noise emits two rows for one simulant (the v0.2
registry carried 19 such pairs); filter rows by membership, e.g.
``df[df.simulant_id.isin(ids["registry"])]``.
"""

from __future__ import annotations

from typing import Hashable, Iterable

import numpy as np


def _draw(rng: np.random.Generator, candidates: list, size: int, what: str) -> set:
    """Deterministically sample ``size`` items from sorted ``candidates``."""
    if size < 0:
        raise ValueError(f"negative draw for {what}: check that the targets are consistent")
    if len(candidates) < size:
        raise ValueError(
            f"not enough {what}: need {size}, have {len(candidates)}; "
            "raise cohorts.oversample and rebuild"
        )
    if size == 0:
        return set()
    idx = rng.choice(len(candidates), size=size, replace=False)
    return {candidates[i] for i in idx}


def stratified_trim(
    registry_ids: Iterable[Hashable],
    finder_a_ids: Iterable[Hashable],
    finder_b_ids: Iterable[Hashable],
    *,
    registry_target: int,
    finder_a_target: int,
    finder_b_target: int,
    overlap_a_target: int,
    overlap_b_target: int,
    seed: int,
) -> dict[str, set]:
    """Select simulant IDs so every design target is hit exactly.

    Inputs are the post-noise survivor IDs of each oversampled cohort and the
    design targets from ``config.yaml``. Returns ``{"registry", "finder_a",
    "finder_b"}`` as sets of IDs guaranteeing:

    - ``len(registry) == registry_target``, and likewise for both finders;
    - ``len(registry & finder_a) == overlap_a_target``;
    - ``len(registry & finder_b) == overlap_b_target``;
    - ``finder_a & finder_b == set()`` — the finder files are disjoint by
      design, so the 100k file is a clean held-out replicate of the 500k file;
    - the same inputs and seed reproduce the same selection: candidates are
      sorted before every draw, and the five draws happen in a fixed order
      (overlap A, filler A, overlap B, filler B, registry filler).

    Raises ``ValueError`` when a survivor pool is too small for its target;
    the remedy is a larger ``cohorts.oversample``.
    """
    if overlap_a_target > finder_a_target or overlap_b_target > finder_b_target:
        raise ValueError("an overlap target exceeds its finder-file target")
    if overlap_a_target + overlap_b_target > registry_target:
        raise ValueError("overlap targets exceed the registry target")

    registry_pool = set(registry_ids)
    a_pool = set(finder_a_ids)
    b_pool = set(finder_b_ids)
    rng = np.random.default_rng(seed)

    overlap_a_candidates = registry_pool & a_pool
    overlap_b_candidates = registry_pool & b_pool

    # Finder A: exactly the target number of overlap members, then filler drawn
    # from survivors outside the ENTIRE overlap pool — an unchosen candidate
    # re-admitted here is guaranteed to also sit in the registry (v0.2's bug).
    chosen_a = _draw(
        rng, sorted(overlap_a_candidates), overlap_a_target,
        "surviving registry∩finder_a overlap candidates",
    )
    filler_a = _draw(
        rng, sorted(a_pool - overlap_a_candidates), finder_a_target - overlap_a_target,
        "finder_a filler candidates",
    )
    finder_a = chosen_a | filler_a

    # Finder B: same construction, additionally excluding everything already in
    # finder A so the two finder files share no simulants.
    chosen_b = _draw(
        rng, sorted(overlap_b_candidates - finder_a), overlap_b_target,
        "surviving registry∩finder_b overlap candidates",
    )
    filler_b = _draw(
        rng, sorted(b_pool - overlap_b_candidates - finder_a), finder_b_target - overlap_b_target,
        "finder_b filler candidates",
    )
    finder_b = chosen_b | filler_b

    # Registry: only the CHOSEN overlap members stay by right; filler avoids
    # both overlap pools so no unchosen candidate can recreate excess overlap.
    registry_filler = _draw(
        rng, sorted(registry_pool - overlap_a_candidates - overlap_b_candidates),
        registry_target - overlap_a_target - overlap_b_target,
        "registry filler candidates",
    )
    registry = chosen_a | chosen_b | registry_filler

    # The postconditions are the whole point; fail loudly if any slips.
    assert len(finder_a) == finder_a_target
    assert len(finder_b) == finder_b_target
    assert len(registry) == registry_target
    assert len(registry & finder_a) == overlap_a_target
    assert len(registry & finder_b) == overlap_b_target
    assert not finder_a & finder_b

    return {"registry": registry, "finder_a": finder_a, "finder_b": finder_b}
