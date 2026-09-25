"""A diagnosis date for each registry record: a deterministic day within the record's year.

The registry stand-in's records come from a census observer, so the only date the
source supplies is the census year. The diagnosis date is a day drawn uniformly over
that calendar year by a keyed hash of the ``simulant_id``, so it is reproducible with
no random stream to manage, duplicated rows of one simulant share one date (two
reports of the same diagnosis), and the age at diagnosis stays within a year of the
age at the record, which is the age the FCDS age/sex target was matched on. The cost
is that dates heap on the census years (2020, 2030, 2040); that is a limitation of a
census pool, named in §4.2, and the reason a yearly observer is under consideration.
"""

from __future__ import annotations

import calendar

import numpy as np
import pandas as pd

DATE_FORMAT = "%m/%d/%Y"  # the same layout as date_of_birth in the released files


def diagnosis_dates(simulant_ids: pd.Series, years: pd.Series, seed: int) -> pd.Series:
    """One ``MM/DD/YYYY`` string per row, uniform within ``years`` and a pure function of id and seed."""
    if len(simulant_ids) != len(years):
        raise ValueError("simulant_ids and years must align")
    if years.isna().any():
        raise ValueError("every registry record needs a census year to place its diagnosis in")
    ids = simulant_ids.astype(str).to_numpy(dtype=object)
    key = f"dx{int(seed):014d}"[:16]  # pandas wants exactly 16 characters
    frac = pd.util.hash_array(ids, hash_key=key).astype(np.float64) / 2.0**64
    yrs = years.astype(int).to_numpy()
    days_in_year = np.array([366 if calendar.isleap(int(y)) else 365 for y in yrs])
    day = np.minimum(np.floor(frac * days_in_year), days_in_year - 1).astype(int)
    start = pd.to_datetime(pd.Series(yrs, index=simulant_ids.index).astype(str) + "-01-01")
    dates = start + pd.to_timedelta(day, unit="D")
    return dates.dt.strftime(DATE_FORMAT)
