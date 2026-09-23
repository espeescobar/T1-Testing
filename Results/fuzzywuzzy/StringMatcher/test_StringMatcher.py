import pytest
from unittest.mock import patch, MagicMock
from Public_Proyects.fuzzywuzzy.StringMatcher import StringMatcher

class TestStringMatcher:

    def test_init_with_isjunk_warning(self):
        with pytest.warns(UserWarning, match="isjunk not NOT implemented"):
            StringMatcher(isjunk=lambda x: True)

    def test_init_sets_sequences(self):
        matcher = StringMatcher(seq1="foo", seq2="bar")
        assert matcher._str1 == "foo"
        assert matcher._str2 == "bar"

    def test_set_seqs_resets_cache(self):
        matcher = StringMatcher(seq1="a", seq2="b")
        matcher._ratio = 0.5
        matcher.set_seqs("c", "d")
        assert matcher._ratio is None
        assert matcher._str1 == "c"
        assert matcher._str2 == "d"

    def test_set_seq1_resets_cache(self):
        matcher = StringMatcher(seq1="a", seq2="b")
        matcher._distance = 1
        matcher.set_seq1("z")
        assert matcher._distance is None
        assert matcher._str1 == "z"

    def test_set_seq2_resets_cache(self):
        matcher = StringMatcher(seq1="a", seq2="b")
        matcher._editops = []
        matcher.set_seq2("z")
        assert matcher._editops is None
        assert matcher._str2 == "z"

    def test_get_opcodes_logic_branches(self):
        # Rama: self._opcodes es None (inicial)
        matcher = StringMatcher(seq1="a", seq2="b")
        with patch('Public_Proyects.fuzzywuzzy.StringMatcher.opcodes') as mock_op:
            matcher.get_opcodes()
            assert mock_op.called
            # Verifica que no se llamó con editops si no existían
            mock_op.assert_called_with("a", "b")
        
        # Rama: self._opcodes ya está definido (cache hit)
        matcher._opcodes = [('equal', 0, 1, 0, 1)]
        assert matcher.get_opcodes() == [('equal', 0, 1, 0, 1)]

    def test_get_editops_logic_branches(self):
        # Rama: self._editops es None, pero existe self._opcodes
        matcher = StringMatcher(seq1="a", seq2="b")
        matcher._opcodes = [('equal', 0, 1, 0, 1)]
        with patch('Public_Proyects.fuzzywuzzy.StringMatcher.editops') as mock_eo:
            matcher.get_editops()
            mock_eo.assert_called_with(matcher._opcodes, "a", "b")

    def test_get_matching_blocks_logic(self):
        matcher = StringMatcher(seq1="a", seq2="a")
        # Forzar que get_opcodes sea llamado internamente
        with patch('Public_Proyects.fuzzywuzzy.StringMatcher.get_opcodes') as mock_ops:
            mock_ops.return_value = [('equal', 0, 1, 0, 1)]
            with patch('Public_Proyects.fuzzywuzzy.StringMatcher.matching_blocks') as mock_mb:
                matcher.get_matching_blocks()
                assert mock_mb.called
                assert mock_mb.call_args[0][0] == mock_ops.return_value

    def test_ratio_branches(self):
        matcher = StringMatcher(seq1="a", seq2="b")
        with patch('Public_Proyects.fuzzywuzzy.StringMatcher.ratio') as mock_r:
            matcher.ratio() # First call
            matcher.ratio() # Second call (cached)
            assert mock_r.call_count == 1

    def test_quick_ratio_branches(self):
        matcher = StringMatcher(seq1="a", seq2="b")
        with patch('Public_Proyects.fuzzywuzzy.StringMatcher.ratio') as mock_r:
            matcher.quick_ratio()
            matcher.quick_ratio()
            assert mock_r.call_count == 1

    def test_real_quick_ratio_math(self):
        # Caso: (2 * min(len1, len2)) / (len1 + len2)
        matcher = StringMatcher(seq1="abc", seq2="ab")
        # 2 * 2 / 5 = 0.8
        assert matcher.real_quick_ratio() == 0.8
        
        # Caso: División por cero (strings vacíos)
        matcher = StringMatcher(seq1="", seq2="")
        with pytest.raises(ZeroDivisionError):
            matcher.real_quick_ratio()

    def test_distance_branches(self):
        matcher = StringMatcher(seq1="a", seq2="b")
        with patch('Public_Proyects.fuzzywuzzy.StringMatcher.distance') as mock_d:
            matcher.distance()
            matcher.distance()
            assert mock_d.call_count == 1