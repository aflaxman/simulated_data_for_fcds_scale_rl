import pandas as pd
import pytest

from simulated_data_for_fcds_scale_rl.diagnosis_date import diagnosis_dates


def _frame(n=5000):
    ids = pd.Series([f"{i % 7}_{i}" for i in range(n)])
    years = pd.Series([2020, 2030, 2040][i % 3] for i in range(n))
    return ids, years


def test_dates_fall_in_the_record_year_and_use_the_dob_layout():
    ids, years = _frame()
    d = diagnosis_dates(ids, years, seed=1)
    parsed = pd.to_datetime(d, format="%m/%d/%Y")
    assert (parsed.dt.year.to_numpy() == years.to_numpy()).all()
    assert d.str.match(r"^\d{2}/\d{2}/\d{4}$").all()


def test_deterministic_and_seed_sensitive():
    ids, years = _frame()
    a, b, c = (diagnosis_dates(ids, years, seed=s) for s in (1, 1, 2))
    assert a.equals(b)
    assert (a != c).mean() > 0.9


def test_roughly_uniform_over_the_year():
    ids, years = _frame(20000)
    months = pd.to_datetime(diagnosis_dates(ids, years, seed=3), format="%m/%d/%Y").dt.month.value_counts(normalize=True)
    assert len(months) == 12 and months.min() > 0.06 and months.max() < 0.11


def test_duplicate_rows_of_one_simulant_share_a_date():
    ids = pd.Series(["a_1", "a_1", "b_2"])
    years = pd.Series([2030, 2030, 2020])
    d = diagnosis_dates(ids, years, seed=9)
    assert d.iloc[0] == d.iloc[1] and d.iloc[2].endswith("2020")


def test_missing_year_is_rejected():
    with pytest.raises(ValueError):
        diagnosis_dates(pd.Series(["x"]), pd.Series([float("nan")]), seed=1)
