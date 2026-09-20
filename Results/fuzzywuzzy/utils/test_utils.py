import pytest
from unittest.mock import MagicMock, patch
from Public_Proyects.fuzzywuzzy.utils import (
    validate_string,
    check_for_equivalence,
    check_for_none,
    check_empty_string,
    asciionly,
    asciidammit,
    make_type_consistent,
    full_process,
    intr
)

# Test validate_string
def test_validate_string():
    assert validate_string("abc") is True
    assert validate_string(" ") is True
    assert validate_string("") is False
    assert validate_string(None) is False
    assert validate_string(123) is False

# Test decorators
def test_check_for_equivalence():
    @check_for_equivalence
    def mock_func(a, b): return 0
    assert mock_func("a", "a") == 100
    assert mock_func("a", "b") == 0

def test_check_for_none():
    decorated = check_for_none(lambda a, b: 1)
    assert decorated(None, "b") == 0
    assert decorated("a", None) == 0
    assert decorated("a", "b") == 1

def test_check_empty_string():
    decorated = check_empty_string(lambda a, b: 1)
    assert decorated("", "b") == 0
    assert decorated("a", "") == 0
    assert decorated("a", "b") == 1

# Test string processing
def test_asciionly():
    # 'á' (U+00E1) is outside 0-127 range
    assert asciionly("abcá") == "abc"
    assert asciionly("123") == "123"

def test_asciidammit():
    assert asciidammit("abc") == "abc"
    # Testing branch where input is not str or unicode
    assert asciidammit(123) == "123"

def test_make_type_consistent():
    # Testing strings
    assert make_type_consistent("a", "b") == ("a", "b")
    # Testing mismatch
    s1, s2 = make_type_consistent("a", 1)
    assert isinstance(s1, str)
    assert isinstance(s2, str)

@patch('Public_Proyects.fuzzywuzzy.utils.StringProcessor')
def test_full_process(mock_sp):
    # Configure mock object behavior
    mock_sp.replace_non_letters_non_numbers_with_whitespace.return_value = "clean"
    mock_sp.to_lower_case.return_value = "clean"
    mock_sp.strip.return_value = "clean"
    
    result = full_process("Test String", force_ascii=False)
    assert result == "clean"
    mock_sp.strip.assert_called_once()

def test_intr():
    assert intr(1.4) == 1
    assert intr(1.5) == 2
    assert intr(1.6) == 2
    assert intr(-1.5) == -2