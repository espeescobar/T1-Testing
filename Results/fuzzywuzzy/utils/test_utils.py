import pytest
import sys
from unittest.mock import patch, MagicMock
from Public_Proyects.fuzzywuzzy.utils import (
    validate_string,
    check_for_equivalence,
    check_for_none,
    check_empty_string,
    asciionly,
    asciidammit,
    make_type_consistent,
    full_process,
    intr,
    PY3,
    unicode
)

# --- Decorator Tests ---

def test_decorators():
    @check_for_equivalence
    def func_eq(a, b): return 1
    assert func_eq("a", "a") == 100
    assert func_eq("a", "b") == 1

    @check_for_none
    def func_none(a, b): return 1
    assert func_none(None, "b") == 0
    assert func_none("a", None) == 0
    assert func_none("a", "b") == 1

    @check_empty_string
    def func_empty(a, b): return 1
    assert func_empty("", "b") == 0
    assert func_empty("a", "") == 0
    assert func_empty("a", "b") == 1

# --- Unicode/ASCII Logic ---

def test_asciionly_branches():
    if PY3:
        assert asciionly("abc") == "abc"
    else:
        # For Python 2 compatibility in test environment
        with patch('Public_Proyects.fuzzywuzzy.utils.PY3', False):
            mock_s = MagicMock()
            asciionly(mock_s)
            assert mock_s.translate.called

def test_asciidammit_branches():
    # Branch: type is str
    assert asciidammit("abc") == "abc"
    
    # Branch: type is unicode
    # Using the module's unicode alias
    u_val = unicode("abc")
    with patch('Public_Proyects.fuzzywuzzy.utils.type', return_value=unicode):
        assert asciidammit(u_val) == "abc"
        
    # Branch: Else (recursive)
    with patch('Public_Proyects.fuzzywuzzy.utils.unicode', side_effect=lambda x: str(x)):
        assert asciidammit(123) == "123"

# --- Type Consistency ---

def test_make_type_consistent_branches():
    # Branch: Both str
    assert make_type_consistent("a", "b") == ("a", "b")
    
    # Branch: Both unicode
    u1, u2 = unicode("a"), unicode("b")
    # We bypass isinstance check via mock to verify the elif branch
    with patch('Public_Proyects.fuzzywuzzy.utils.isinstance', side_effect=lambda obj, t: t is unicode or obj is u1):
        assert make_type_consistent(u1, u2) == (u1, u2)
        
    # Branch: Else (mixed)
    r1, r2 = make_type_consistent(1, "a")
    assert r1 == "1" and r2 == "a"

# --- Full Process & Utils ---

@patch('Public_Proyects.fuzzywuzzy.utils.StringProcessor')
def test_full_process_logic(mock_sp):
    mock_sp.replace_non_letters_non_numbers_with_whitespace.return_value = "a"
    mock_sp.to_lower_case.return_value = "a"
    mock_sp.strip.return_value = "a"
    
    # Force ascii path
    with patch('Public_Proyects.fuzzywuzzy.utils.asciidammit', return_value="a") as mock_ascii:
        assert full_process("Café", force_ascii=True) == "a"
        mock_ascii.assert_called_with("Café")
        
    # No force ascii path
    assert full_process("Café", force_ascii=False) == "a"

def test_validate_string_logic():
    # True path
    assert validate_string("abc") is True
    # False path (empty)
    assert validate_string("") is False
    # TypeError path
    assert validate_string(None) is False
    assert validate_string(123) is False

def test_intr():
    assert intr(1.4) == 1
    assert intr(1.6) == 2
    assert intr(1.5) == 2 