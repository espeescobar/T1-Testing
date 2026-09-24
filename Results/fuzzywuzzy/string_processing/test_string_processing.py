import pytest
from unittest.mock import MagicMock
from Public_Proyects.fuzzywuzzy.string_processing import StringProcessor

class TestStringProcessor:

    def test_replace_non_letters_non_numbers_with_whitespace(self):
        processor = StringProcessor()
        
        # Test basic alphanumeric replacement
        assert processor.replace_non_letters_non_numbers_with_whitespace("hello!world") == "hello world"
        assert processor.replace_non_letters_non_numbers_with_whitespace("test@123#example") == "test 123 example"
        
        # Test sequences of non-alphanumeric characters
        assert processor.replace_non_letters_non_numbers_with_whitespace("hello!!!world") == "hello   world"
        
        # Test empty string
        assert processor.replace_non_letters_non_numbers_with_whitespace("") == ""
        
        # Test string with only non-alphanumeric
        assert processor.replace_non_letters_non_numbers_with_whitespace("!!!") == "   "

    def test_strip(self):
        assert StringProcessor.strip("  hello  ") == "hello"
        assert StringProcessor.strip(" \t\n hello \t\n ") == "hello"

    def test_to_lower_case(self):
        assert StringProcessor.to_lower_case("HELLO") == "hello"
        assert StringProcessor.to_lower_case("hElLo") == "hello"

    def test_to_upper_case(self):
        assert StringProcessor.to_upper_case("hello") == "HELLO"
        assert StringProcessor.to_upper_case("hElLo") == "HELLO"

    def test_regex_attribute(self):
        # Verify regex is correctly compiled
        assert hasattr(StringProcessor, 'regex')
        assert StringProcessor.regex.pattern == r"(?ui)\W"

    def test_mocking_with_magicmock(self):
        """
        Example test case demonstrating the use of MagicMock as requested.
        """
        mock_processor = MagicMock(spec=StringProcessor)
        mock_processor.to_lower_case.return_value = "mocked_lower"
        
        result = mock_processor.to_lower_case("INPUT")
        
        assert result == "mocked_lower"
        mock_processor.to_lower_case.assert_called_once_with("INPUT")