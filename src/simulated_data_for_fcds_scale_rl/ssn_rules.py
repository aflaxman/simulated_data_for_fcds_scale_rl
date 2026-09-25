"""Sentinel checks on Social Security numbers, for the data forensics of §3.3 and the acceptance notebook.

The Social Security Administration never issues numbers whose area (first three
digits) is 000, 666 or 900–999, whose group (middle two) is 00, or whose serial
(last four) is 0000; a real file sometimes carries such placeholders, and a
nine-times-repeated digit is the commonest of them.
"""

from __future__ import annotations

import re

_DIGITS = re.compile(r"^\d{9}$")


def digits(ssn: str | None) -> str | None:
    """The nine digits of an SSN written with or without dashes, or None if it is not nine digits."""
    if ssn is None:
        return None
    d = str(ssn).replace("-", "").strip()
    return d if _DIGITS.match(d) else None


def is_repeated_digit(ssn: str | None) -> bool:
    d = digits(ssn)
    return d is not None and len(set(d)) == 1


def is_ssa_issuable(ssn: str | None) -> bool:
    """True when the number could have been issued: valid area, group and serial ranges."""
    d = digits(ssn)
    if d is None:
        return False
    area, group, serial = d[:3], d[3:5], d[5:]
    if area in ("000", "666") or area >= "900":
        return False
    return group != "00" and serial != "0000"
