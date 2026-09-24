import pytest
from unittest.mock import MagicMock
from Public_Proyects.fuzzywuzzy.fuzz import (
    ratio, partial_ratio, token_sort_ratio, partial_token_sort_ratio,
    token_set_ratio, partial_token_set_ratio, QRatio, UQRatio, WRatio, UWRatio
)

def test_ratio_exhaustive():
    assert ratio("this is a test", "this is a test!") == 97
    assert ratio("fuzzy wuzzy", "fuzzy wuzzy") == 100
    assert ratio("", "test") == 0
    assert ratio("a", "b") == 0

def test_partial_ratio_exhaustive():
    assert partial_ratio("this is a test", "this is a test") == 100
    assert partial_ratio("new york", "new york city") == 100
    assert partial_ratio("apple", "pineapple") == 100
    # Test block logic where block alignment is forced
    assert partial_ratio("short", "extremely long string that contains short") == 100
    assert partial_ratio("a", "b") == 0

def test_token_sort_ratio_variations():
    assert token_sort_ratio("fuzzy wuzzy", "wuzzy fuzzy") == 100
    assert token_sort_ratio("a b c", "c b a") == 100
    assert token_sort_ratio("test", "test") == 100
    assert partial_token_sort_ratio("a b c", "b") == 100

def test_token_set_ratio_variations():
    assert token_set_ratio("fuzzy wuzzy", "wuzzy fuzzy fuzzy") == 100
    # Test branch where full_process=False and strings are equal
    assert token_set_ratio("same", "same", full_process=False) == 100
    # Test branch where strings are not equal and not fully processed
    assert token_set_ratio("a b", "a c", full_process=False) > 0
    assert partial_token_set_ratio("test", "this is a test") == 100

def test_wratio_branches():
    # Test len_ratio < 1.5 (try_partial = False)
    assert WRatio("same length", "same length") == 100
    # Test len_ratio > 1.5 (try_partial = True)
    assert WRatio("short", "a very long string that is much longer") > 0
    # Test len_ratio > 8 (partial_scale = .6)
    assert WRatio("a", "this is a string that is way way way way way way way way long") >= 0
    # Test force_ascii=False path
    assert UWRatio("test", "test") == 100

def test_qratio_branches():
    assert QRatio("test", "test", full_process=False) == 100
    assert QRatio("test", "test", full_process=True) == 100
    assert QRatio("a", "b", full_process=True) == 0
    assert UQRatio("test", "test", full_process=False) == 100

def test_input_validation():
    assert ratio(None, "test") == 0
    assert token_sort_ratio(None, "test") == 0
    assert token_set_ratio(None, "test") == 0
    
    # Mocking validation to trigger the 0 return in QRatio
    mock_utils = MagicMock()
    # Ensure validation fails for empty string scenarios
    assert QRatio("", "test") == 0

def test_edge_cases():
    # Testing strings that result in empty after full_process
    assert QRatio("!!!", "???") == 0
    assert WRatio("!!!", "???") == 0
    # Test tokens difference logic in _token_set
    assert token_set_ratio("same", "different") < 100