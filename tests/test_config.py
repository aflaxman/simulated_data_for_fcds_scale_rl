from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CFG = yaml.safe_load((ROOT / "config.yaml").read_text())


def test_design_keys_present():
    c = CFG["cohorts"]
    assert c["registry_pool"] == "last_seen"
    assert c["finder_year"] in c["census_years"]
    assert c["census_years"] == sorted(c["census_years"])
    assert c["overlap_500k_target"] + c["overlap_100k_target"] <= c["registry_target"]
    assert c["overlap_finder_finder_target"] == 0


def test_seeds_and_target_table():
    assert set(CFG["seeds"]) >= {"duckdb_sample", "psp_registry", "psp_finder", "diagnosis_date"}


def test_row_noise_is_off():
    """Rows out must equal rows in: no non-response, omission or duplication (decision 2026-10-04)."""
    rn = CFG["noise"]["row_noise"]
    assert set(rn) == {"do_not_respond", "omit_row", "duplicate_with_guardian"}
    assert all(v == 0 for v in rn.values())
    assert (ROOT / CFG["paths"]["age_sex_target"]).exists()


def test_noise_rates_are_the_second_authors_specification():
    n = CFG["noise"]
    assert n["finder"] == {"ssn_missing": 0.20, "ssn_transposed": 0.01, "address_missing": 0.05}
    assert n["registry"] == {"ssn_missing": 0.05, "ssn_transposed": 0.00, "address_missing": 0.01}
