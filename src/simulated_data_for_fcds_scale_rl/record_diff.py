"""Name the mechanism behind a field-level discrepancy between two records of one simulant.

Used by ``pipeline/example_pair.py`` to pick and annotate the worked example
(Table 2 / the record-pair panel). The labels are heuristics over the two
values only, so they name what the discrepancy *looks like* (a typo, an
adjacent-digit swap), not which pseudopeople noise function produced it.
"""

from __future__ import annotations

import math
from datetime import date

NAME_FIELDS = {"first_name", "middle_initial", "last_name", "street_name", "city"}
CATEGORY_FIELDS = {"sex", "race_ethnicity", "state"}
DIGIT_FIELDS = {"zipcode", "street_number", "unit_number"}


def _clean(v) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return ""
    return str(v).strip()


def levenshtein(a: str, b: str) -> int:
    """Plain edit distance; the strings here are short, so O(len a * len b) is fine."""
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def is_adjacent_transposition(a: str, b: str) -> bool:
    """True when ``a`` and ``b`` differ only by one swap of two neighbouring characters."""
    if len(a) != len(b) or a == b:
        return False
    diff = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    return len(diff) == 2 and diff[1] == diff[0] + 1 and a[diff[0]] == b[diff[1]] and a[diff[1]] == b[diff[0]]


def parse_mdy(s: str) -> date | None:
    try:
        m, d, y = (int(p) for p in s.split("/"))
        return date(y, m, d)
    except (ValueError, AttributeError):
        return None


def classify(field: str, registry_value, finder_value) -> str | None:
    """Return a short label for how the two values differ, or ``None`` when they agree.

    Labels: ``blank``, ``month and day swapped``, ``adjacent digits swapped``,
    ``digits changed``, ``typo``, ``nickname or different name``,
    ``different category``, ``different value``.
    """
    a, b = _clean(registry_value), _clean(finder_value)
    if a == b:
        return None
    if a == "" or b == "":
        return "blank"
    if field == "ssn":
        da, db = a.replace("-", ""), b.replace("-", "")
        return "adjacent digits swapped" if is_adjacent_transposition(da, db) else "digits changed"
    if field == "date_of_birth":
        pa, pb = parse_mdy(a), parse_mdy(b)
        if pa and pb and pa.year == pb.year and pa.month == pb.day and pa.day == pb.month and pa.month != pa.day:
            return "month and day swapped"
        return "digits changed"
    if field in NAME_FIELDS:
        if a.lower() == b.lower():
            return "case changed"
        if levenshtein(a.lower(), b.lower()) <= 2:
            return "typo"
        return "nickname or different name" if field == "first_name" else "different value"
    if field in CATEGORY_FIELDS:
        return "different category"
    if field in DIGIT_FIELDS:
        return "digits changed" if len(a) == len(b) else "different value"
    return "different value"
