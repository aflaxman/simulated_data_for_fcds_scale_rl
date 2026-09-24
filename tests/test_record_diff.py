import math

from simulated_data_for_fcds_scale_rl.record_diff import classify, is_adjacent_transposition, levenshtein


def test_equal_and_blank():
    assert classify("first_name", "Mary", "Mary") is None
    assert classify("ssn", None, "123-45-6789") == "blank"
    assert classify("city", "", "tampa") == "blank"
    assert classify("zipcode", float("nan"), "33101") == "blank"


def test_ssn_transposition_vs_other_change():
    assert is_adjacent_transposition("123456789", "123465789")
    assert not is_adjacent_transposition("123456789", "125436789")  # swapped, but not neighbours
    assert classify("ssn", "123-45-6789", "123-46-5789") == "adjacent digits swapped"
    assert classify("ssn", "123-45-6789", "123-45-6788") == "digits changed"


def test_dob_swap_and_typo():
    assert classify("date_of_birth", "03/07/1954", "07/03/1954") == "month and day swapped"
    assert classify("date_of_birth", "03/03/1954", "03/03/1955") == "digits changed"
    assert classify("date_of_birth", "13/40/1954", "03/03/1954") == "digits changed"  # unparseable side


def test_names():
    assert levenshtein("kitten", "sitting") == 3
    assert classify("first_name", "Katherine", "Kathrine") == "typo"
    assert classify("first_name", "William", "Bill") == "nickname or different name"
    assert classify("last_name", "Patel", "Smith") == "different value"
    assert classify("street_name", "caribou ct", "Caribou Ct") == "case changed"


def test_categories_and_digits():
    assert classify("sex", "Male", "Female") == "different category"
    assert classify("zipcode", "32826", "32836") == "digits changed"
    assert classify("street_number", "610", "6100") == "different value"
    assert not math.isnan(0.0)
