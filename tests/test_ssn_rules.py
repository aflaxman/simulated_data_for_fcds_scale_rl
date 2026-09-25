from simulated_data_for_fcds_scale_rl.ssn_rules import digits, is_repeated_digit, is_ssa_issuable


def test_digits_and_formats():
    assert digits("123-45-6789") == "123456789"
    assert digits("123456789") == "123456789"
    assert digits("12-345-6789") == "123456789"
    assert digits("1234-5678") is None and digits(None) is None and digits("") is None


def test_repeated_digit_sentinel():
    assert is_repeated_digit("111-11-1111")
    assert not is_repeated_digit("111-11-1112")


def test_ssa_issuance_rules():
    assert is_ssa_issuable("123-45-6789")
    assert not is_ssa_issuable("000-45-6789")
    assert not is_ssa_issuable("666-45-6789")
    assert not is_ssa_issuable("900-45-6789") and not is_ssa_issuable("999-45-6789")
    assert not is_ssa_issuable("123-00-6789")
    assert not is_ssa_issuable("123-45-0000")
    assert not is_ssa_issuable("12-345-678")
