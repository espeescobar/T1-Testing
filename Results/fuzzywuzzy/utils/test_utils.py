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

def test_validate_string():
    assert validate_string("test") is True
    assert validate_string("a") is True
    assert validate_string("") is False
    assert validate_string(None) is False
    assert validate_string(123) is False

def test_check_for_equivalence():
    @check_for_equivalence
    def dummy_func(a, b):
        return 50
    
    assert dummy_func("test", "test") == 100
    assert dummy_func("test1", "test2") == 50

def test_check_for_none():
    @check_for_none
    def dummy_func(a, b):
        return 50
    
    assert dummy_func(None, "test") == 0
    assert dummy_func("test", None) == 0
    assert dummy_func("test", "test") == 50

def test_check_empty_string():
    @check_empty_string
    def dummy_func(a, b):
        return 50
    
    assert dummy_func("", "test") == 0
    assert dummy_func("test", "") == 0
    assert dummy_func("a", "b") == 50

def test_asciionly():
    s = "hello" + chr(128)
    assert asciionly(s) == "hello"

def test_asciidammit():
    # En Python 3, unicode es str. 
    # El test verifica el comportamiento sin necesidad de mockear si no es estrictamente necesario 
    # o usando un mock que no rompa el isinstance.
    assert asciidammit("ascii") == "ascii"
    assert asciidammit(123) == "123"

@patch('Public_Proyects.fuzzywuzzy.utils.unicode', str)
def test_make_type_consistent():
    # Caso 1: Ambos son str (se ejecuta el primer if)
    s1, s2 = make_type_consistent("a", "b")
    assert isinstance(s1, str) and isinstance(s2, str)
    
    # Caso 2: Mixto (ejecuta el else y llama a unicode())
    # Como patchamos 'unicode' como 'str', el isinstance(s1, unicode) funciona correctamente.
    r1, r2 = make_type_consistent(1, "b")
    assert r1 == "1"
    assert r2 == "b"

@patch('Public_Proyects.fuzzywuzzy.utils.StringProcessor')
def test_full_process(mock_sp):
    mock_sp.replace_non_letters_non_numbers_with_whitespace.return_value = " raw "
    mock_sp.to_lower_case.return_value = " raw "
    mock_sp.strip.return_value = "raw"
    
    result = full_process("Raw String", force_ascii=False)
    
    assert result == "raw"
    mock_sp.replace_non_letters_non_numbers_with_whitespace.assert_called_once()
    mock_sp.to_lower_case.assert_called_once()
    mock_sp.strip.assert_called_once()

def test_intr():
    assert intr(1.4) == 1
    assert intr(1.6) == 2
    assert intr(2.5) == 2  
    assert intr(-1.5) == -2