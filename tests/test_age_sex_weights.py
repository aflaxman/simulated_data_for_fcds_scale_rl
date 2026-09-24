from pathlib import Path

import pandas as pd
import pytest
import yaml

from simulated_data_for_fcds_scale_rl.age_sex_weights import load_age_sex_weights

ROOT = Path(__file__).resolve().parent.parent
CFG = yaml.safe_load((ROOT / "config.yaml").read_text())


def test_configured_weights_table_loads_and_covers_all_ages():
    w = load_age_sex_weights(ROOT / CFG["paths"]["age_sex_weights"])
    assert list(w.columns) == ["age_start", "age_end", "sex", "weight"]
    assert set(w["sex"]) == {"Female", "Male"}
    for _, bins in w.groupby("sex"):
        assert bins["age_start"].iloc[0] == 0
        assert bins["age_end"].iloc[-1] >= 120  # open-ended top bin covers every simulant
    assert (w["weight"] > 0).all()


def test_fcds_table_is_the_configured_source_and_has_18_bins_per_sex():
    assert CFG["paths"]["age_sex_weights"] == "reference/fcds_incidence_by_age_sex.csv"
    w = load_age_sex_weights(ROOT / "reference" / "fcds_incidence_by_age_sex.csv")
    assert w.groupby("sex").size().to_dict() == {"Female": 18, "Male": 18}
    # Rates per 100,000 as committed; a sanity anchor against a silently rescaled file.
    male_75 = w.query("sex == 'Male' and age_start == 75")["weight"].item()
    assert 2700 < male_75 < 2800


def test_gbd_comparator_table_still_loads():
    w = load_age_sex_weights(ROOT / "reference" / "gbd_neoplasm_prevalence_florida.csv")
    assert set(w["sex"]) == {"Female", "Male"}
    assert (w["weight"] > 0).all()


def _write(tmp_path, rows):
    p = tmp_path / "t.csv"
    pd.DataFrame(rows).to_csv(p, index=False)
    return p


def test_lowercase_sex_is_recoded_to_pseudopeople_convention(tmp_path):
    p = _write(tmp_path, [
        dict(age_start=0, age_end=50, sex="male", rate=1.0),
        dict(age_start=50, age_end=999, sex="male", rate=2.0),
        dict(age_start=0, age_end=50, sex="female", rate=1.0),
        dict(age_start=50, age_end=999, sex="female", rate=2.0),
    ])
    assert set(load_age_sex_weights(p)["sex"]) == {"Female", "Male"}


def test_gap_in_age_bins_is_rejected(tmp_path):
    p = _write(tmp_path, [
        dict(age_start=0, age_end=50, sex="Male", rate=1.0),
        dict(age_start=55, age_end=999, sex="Male", rate=2.0),
    ])
    with pytest.raises(ValueError, match="contiguous"):
        load_age_sex_weights(p)


def test_unknown_sex_and_missing_weight_column_are_rejected(tmp_path):
    with pytest.raises(ValueError, match="sex"):
        load_age_sex_weights(_write(tmp_path, [dict(age_start=0, age_end=999, sex="Other", rate=1.0)]))
    with pytest.raises(ValueError, match="weight column"):
        load_age_sex_weights(_write(tmp_path, [dict(age_start=0, age_end=999, sex="Male", count=3)]))
