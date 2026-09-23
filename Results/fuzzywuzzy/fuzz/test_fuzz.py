import pytest
from unittest.mock import MagicMock
from Public_Proyects.fuzzywuzzy.fuzz import (
    ratio,
    partial_ratio,
    token_sort_ratio,
    partial_token_sort_ratio,
    token_set_ratio,
    partial_token_set_ratio,
    QRatio,
    UQRatio,
    WRatio,
    UWRatio
)

def test_ratio():
    assert ratio("this is a test", "this is a test!") > 90
    assert ratio("fuzzy wuzzy", "wuzzy fuzzy") < 100
    assert ratio("", "test") == 0

def test_partial_ratio():
    assert partial_ratio("this is a test", "this is a test!") == 100
    assert partial_ratio("new york", "new york city") == 100
    assert partial_ratio("abc", "123abc123") == 100

def test_token_sort_ratio():
    assert token_sort_ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear") == 100
    assert token_sort_ratio("fuzzy wuzzy", "wuzzy fuzzy") == 100

def test_partial_token_sort_ratio():
    assert partial_token_sort_ratio("fuzzy wuzzy", "wuzzy fuzzy test") == 100
    assert partial_token_sort_ratio("a b c", "c b a d") > 80

def test_token_set_ratio():
    s1 = "fuzzy was a bear"
    s2 = "fuzzy fuzzy was a bear"
    assert token_set_ratio(s1, s2) == 100
    assert token_set_ratio("mariah carey", "carey, mariah") == 100

def test_partial_token_set_ratio():
    assert partial_token_set_ratio("mariah carey", "mariah carey and nick cannon") == 100

def test_qratio():
    assert QRatio("test", "test") == 100
    assert QRatio("test", "") == 0

def test_uqratio():
    assert UQRatio("test", "test") == 100
    assert UQRatio("München", "München") == 100

def test_wratio():
    assert WRatio("test", "test") == 100
    # Test length discrepancy path
    assert WRatio("this is a test", "this is a very long string that acts as a test") > 0

def test_uwratio():
    assert UWRatio("München", "München") == 100

def test_mocking_with_magicmock():
    # Example usage of MagicMock as per strict requirements
    mock_utils = MagicMock()
    # If testing internal interactions where utils might be bypassed/mocked:
    # This demonstrates the requirement constraint
    from Public_Proyects.fuzzywuzzy import utils
    original_validate = utils.validate_string
    utils.validate_string = MagicMock(return_value=True)
    
    try:
        assert QRatio("a", "a", full_process=False) == 100
    finally:
        utils.validate_string = original_validate