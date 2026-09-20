import pytest
from unittest.mock import patch
from Public_Proyects.fuzzywuzzy.StringMatcher import StringMatcher

def test_string_matcher_initialization():
    matcher = StringMatcher(seq1="test", seq2="text")
    assert matcher._str1 == "test"
    assert matcher._str2 == "text"

def test_set_methods_reset_cache():
    matcher = StringMatcher("a", "b")
    matcher._ratio = 0.5
    matcher.set_seq1("c")
    assert matcher._ratio is None
    
    matcher._ratio = 0.8
    matcher.set_seq2("d")
    assert matcher._ratio is None
    
    matcher._ratio = 0.9
    matcher.set_seqs("e", "f")
    assert matcher._ratio is None

def test_get_opcodes_caching():
    with patch('Public_Proyects.fuzzywuzzy.StringMatcher.opcodes', return_value=[('equal', 0, 1, 0, 1)]) as mock_opcodes:
        matcher = StringMatcher("a", "a")
        res1 = matcher.get_opcodes()
        res2 = matcher.get_opcodes()
        assert res1 == [('equal', 0, 1, 0, 1)]
        assert mock_opcodes.call_count == 1

def test_get_editops_from_opcodes():
    matcher = StringMatcher("abc", "adc")
    matcher._opcodes = [('equal', 0, 1, 0, 1)]
    
    with patch('Public_Proyects.fuzzywuzzy.StringMatcher.editops') as mock_editops:
        mock_editops.return_value = [('replace', 1, 1)]
        result = matcher.get_editops()
        assert result == [('replace', 1, 1)]
        mock_editops.assert_called_once()

def test_ratio_and_quick_ratio():
    # Patch the ratio function globally used within StringMatcher
    with patch('Public_Proyects.fuzzywuzzy.StringMatcher.ratio', return_value=0.5):
        matcher = StringMatcher("test", "test")
        assert matcher.ratio() == 0.5
        assert matcher.quick_ratio() == 0.5

def test_real_quick_ratio():
    # El error 0.0 ocurre porque los strings pueden estar vacíos o inicializados incorrectamente en el mock
    # Verificamos la lógica matemática instanciando con valores directos
    matcher = StringMatcher(seq1="abc", seq2="ab")
    # 2.0 * min(3, 2) / (3 + 2) = 2.0 * 2 / 5 = 0.8
    assert matcher.real_quick_ratio() == pytest.approx(0.8)

def test_distance():
    with patch('Public_Proyects.fuzzywuzzy.StringMatcher.distance', return_value=3):
        matcher = StringMatcher("kitten", "sitting")
        assert matcher.distance() == 3

def test_isjunk_warning():
    with pytest.warns(UserWarning, match="isjunk not NOT implemented"):
        StringMatcher(isjunk=lambda x: True)

def test_caching_logic_branches():
    matcher = StringMatcher("test", "test")
    # Inyectamos el valor de control directamente
    matcher._distance = 42
    
    # Si patchamos, nos aseguramos de que el método no sea ejecutado por la lógica interna
    with patch('Public_Proyects.fuzzywuzzy.StringMatcher.distance') as mock_dist:
        result = matcher.distance()
        assert result == 42
        mock_dist.assert_not_called()

def test_get_matching_blocks():
    matcher = StringMatcher("abc", "abc")
    # mockeamos opcodes para que get_matching_blocks no intente procesar la cadena original
    with patch('Public_Proyects.fuzzywuzzy.StringMatcher.opcodes', return_value=[]):
        with patch('Public_Proyects.fuzzywuzzy.StringMatcher.matching_blocks', return_value=[(0, 0, 3)]):
            assert matcher.get_matching_blocks() == [(0, 0, 3)]