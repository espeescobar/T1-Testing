import pytest
from unittest.mock import MagicMock, patch
from Public_Proyects.fuzzywuzzy.StringMatcher import StringMatcher

class TestStringMatcher:

    @pytest.fixture
    def matcher(self):
        return StringMatcher(seq1="apple", seq2="pear")

    def test_init_sets_sequences(self):
        matcher = StringMatcher(seq1="test1", seq2="test2")
        assert matcher._str1 == "test1"
        assert matcher._str2 == "test2"

    def test_init_warns_on_isjunk(self):
        with pytest.warns(UserWarning, match="isjunk not NOT implemented"):
            StringMatcher(isjunk=lambda x: True)

    def test_set_seqs_resets_cache(self, matcher):
        matcher._ratio = 0.5
        matcher.set_seqs("a", "b")
        assert matcher._ratio is None
        assert matcher._str1 == "a"
        assert matcher._str2 == "b"

    def test_set_seq1_resets_cache(self, matcher):
        matcher._distance = 5
        matcher.set_seq1("new")
        assert matcher._distance is None
        assert matcher._str1 == "new"

    def test_set_seq2_resets_cache(self, matcher):
        matcher._editops = [('replace', 0, 0)]
        matcher.set_seq2("new")
        assert matcher._editops is None
        assert matcher._str2 == "new"

    @patch('Public_Proyects.fuzzywuzzy.StringMatcher.opcodes')
    def test_get_opcodes_calls_levenshtein(self, mock_opcodes):
        matcher = StringMatcher(seq1="abc", seq2="abd")
        matcher.get_opcodes()
        mock_opcodes.assert_called_once_with("abc", "abd")

    @patch('Public_Proyects.fuzzywuzzy.StringMatcher.editops')
    def test_get_editops_calls_levenshtein(self, mock_editops):
        matcher = StringMatcher(seq1="abc", seq2="abd")
        matcher.get_editops()
        mock_editops.assert_called_once_with("abc", "abd")

    @patch('Public_Proyects.fuzzywuzzy.StringMatcher.matching_blocks')
    def test_get_matching_blocks(self, mock_matching):
        matcher = StringMatcher(seq1="abc", seq2="abd")
        matcher.get_matching_blocks()
        assert mock_matching.called

    def test_ratio(self, matcher):
        val = matcher.ratio()
        assert isinstance(val, float)
        assert matcher._ratio == val

    def test_quick_ratio(self, matcher):
        assert matcher.quick_ratio() == matcher.ratio()

    def test_real_quick_ratio(self):
        # 2.0 * min(3, 3) / (3 + 3) = 2.0 * 3 / 6 = 1.0
        matcher = StringMatcher(seq1="abc", seq2="abc")
        assert matcher.real_quick_ratio() == 1.0
        # 2.0 * min(2, 4) / (2 + 4) = 4 / 6 = 0.666...
        matcher.set_seqs("ab", "abcd")
        assert matcher.real_quick_ratio() == pytest.approx(0.6666666666666666)

    def test_distance(self, matcher):
        dist = matcher.distance()
        assert isinstance(dist, int)
        assert matcher._distance == dist

    def test_caching_mechanism(self):
        # Verify that calling a method multiple times returns cached result
        matcher = StringMatcher(seq1="hello", seq2="hello")
        with patch('Public_Proyects.fuzzywuzzy.StringMatcher.ratio', return_value=1.0) as mock_ratio:
            matcher.ratio()
            matcher.ratio()
            assert mock_ratio.call_count == 1