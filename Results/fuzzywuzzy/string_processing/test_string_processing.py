import pytest
from unittest.mock import MagicMock
from Public_Proyects.fuzzywuzzy.string_processing import StringProcessor

def test_replace_non_letters_non_numbers_with_whitespace():
    """
    The regex '\W' matches any character that is NOT a word character (a-z, A-Z, 0-9, or _).
    Therefore, underscores are considered 'word characters' and are NOT replaced by the regex.
    """
    # Verifying behavior based on the actual implementation of \W
    assert StringProcessor.replace_non_letters_non_numbers_with_whitespace("hello!world") == "hello world"
    assert StringProcessor.replace_non_letters_non_numbers_with_whitespace("test@example.com") == "test example com"
    
    # Corrected expectation: underscores are preserved by \W regex
    assert StringProcessor.replace_non_letters_non_numbers_with_whitespace("123-456_789") == "123 456_789"
    
    # Verifying multiple non-alphanumeric characters are replaced individually
    assert StringProcessor.replace_non_letters_non_numbers_with_whitespace("a!@#b") == "a   b"

def test_strip():
    assert StringProcessor.strip("  hello  ") == "hello"
    assert StringProcessor.strip("\t\n hello \t\n") == "hello"

def test_to_lower_case():
    assert StringProcessor.to_lower_case("HELLO") == "hello"
    assert StringProcessor.to_lower_case("PyThOn") == "python"

def test_to_upper_case():
    assert StringProcessor.to_upper_case("hello") == "HELLO"
    assert StringProcessor.to_upper_case("PyThOn") == "PYTHON"

def test_regex_mocking():
    """
    Test using MagicMock to simulate the regex sub behavior.
    """
    mock_regex = MagicMock()
    mock_regex.sub.return_value = "mocked_result"
    
    # Temporarily override the class attribute for isolated testing
    original_regex = StringProcessor.regex
    StringProcessor.regex = mock_regex
    
    try:
        result = StringProcessor.replace_non_letters_non_numbers_with_whitespace("input")
        assert result == "mocked_result"
        mock_regex.sub.assert_called_once_with(" ", "input")
    finally:
        StringProcessor.regex = original_regex