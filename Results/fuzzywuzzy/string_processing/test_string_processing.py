import pytest
from Public_Proyects.fuzzywuzzy.string_processing import StringProcessor

def test_replace_non_letters_non_numbers_with_whitespace():
    assert StringProcessor.replace_non_letters_non_numbers_with_whitespace("hello!world") == "hello world"
    assert StringProcessor.replace_non_letters_non_numbers_with_whitespace("test-string_123") == "test string 123"
    assert StringProcessor.replace_non_letters_non_numbers_with_whitespace("   spaces   ") == "   spaces   "
    assert StringProcessor.replace_non_letters_non_numbers_with_whitespace("a@b#c$d") == "a b c d"
    assert StringProcessor.replace_non_letters_non_numbers_with_whitespace("123abc456") == "123abc456"

def test_strip():
    assert StringProcessor.strip("  hello  ") == "hello"
    assert StringProcessor.strip("\n\t hello \r") == "hello"

def test_to_lower_case():
    assert StringProcessor.to_lower_case("HELLO") == "hello"
    assert StringProcessor.to_lower_case("HeLLo") == "hello"
    assert StringProcessor.to_lower_case("123abc") == "123abc"

def test_to_upper_case():
    assert StringProcessor.to_upper_case("hello") == "HELLO"
    assert StringProcessor.to_upper_case("HeLLo") == "HELLO"
    assert StringProcessor.to_upper_case("123abc") == "123ABC"