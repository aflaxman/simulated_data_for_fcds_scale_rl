"""Name the mechanism behind a field-level discrepancy between two records of one simulant.

Used by ``pipeline/example_pair.py`` to pick and annotate the worked example
(Table 2 / the record-pair panel). The labels are heuristics over the two
values only, so they name what the discrepancy *looks like* (a typo, an
adjacent-digit swap), not which pseudopeople noise function produced it.
"""

from __future__ import annotations

import csv
import math
from datetime import date
from functools import lru_cache
from pathlib import Path

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


@lru_cache(maxsize=1)
def nickname_pairs() -> frozenset[tuple[str, str]]:
    """Unordered (name, nickname) pairs from pseudopeople's own nickname table, lower-cased."""
    try:
        import pseudopeople
    except ImportError:  # pragma: no cover - the classifier still works, just without verified nicknames
        return frozenset()
    path = Path(pseudopeople.__file__).parent / "data" / "nicknames.csv"
    if not path.exists():
        return frozenset()
    pairs = set()
    with open(path, newline="") as fh:
        for row in csv.reader(fh):
            names = [c.strip().lower() for c in row if c.strip()]
            if len(names) < 2 or names[0] == "name":
                continue
            for nick in names[1:]:
                pairs.add(tuple(sorted((names[0], nick))))
    return frozenset(pairs)


def is_nickname_pair(a: str, b: str) -> bool:
    return tuple(sorted((a.lower(), b.lower()))) in nickname_pairs()


def classify(field: str, registry_value, finder_value) -> str | None:
    """Return a short label for how the two values differ, or ``None`` when they agree.

    Labels: ``blank``, ``month and day swapped``, ``adjacent digits swapped``,
    ``one digit changed`` (the registry's SSN wrong digit), ``digits changed``, ``typo``, ``nickname`` (a pair in pseudopeople's nickname table),
    ``different name`` (any other first-name change, usually pseudopeople's fake-name
    noise), ``different category``, ``different value``.
    """
    a, b = _clean(registry_value), _clean(finder_value)
    if a == b:
        return None
    if a == "" or b == "":
        return "blank"
    if field == "ssn":
        da, db = a.replace("-", ""), b.replace("-", "")
        if is_adjacent_transposition(da, db):
            return "adjacent digits swapped"
        if len(da) == len(db) and sum(x != y for x, y in zip(da, db)) == 1:
            return "one digit changed"
        return "digits changed"
    if field == "date_of_birth":
        pa, pb = parse_mdy(a), parse_mdy(b)
        if pa and pb and pa.year == pb.year and pa.month == pb.day and pa.day == pb.month and pa.month != pa.day:
            return "month and day swapped"
        return "digits changed"
    if field in NAME_FIELDS:
        if a.lower() == b.lower():
            return "case changed"
        if field == "first_name" and is_nickname_pair(a, b):
            return "nickname"
        if levenshtein(a.lower(), b.lower()) <= 2:
            return "typo"
        return "different name" if field == "first_name" else "different value"
    if field in CATEGORY_FIELDS:
        return "different category"
    if field in DIGIT_FIELDS:
        return "digits changed" if len(a) == len(b) else "different value"
    return "different value"
