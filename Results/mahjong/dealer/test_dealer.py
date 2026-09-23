import pytest
from unittest.mock import MagicMock, patch
from Public_Proyects.mahjong.dealer import MahjongDealer

class TestMahjongDealer:

    @pytest.fixture
    def mock_np_random(self):
        return MagicMock()

    def test_init_and_internal_methods(self, mock_np_random):
        """
        Tests the constructor and explicitly exercises the internal calls.
        """
        with patch('Public_Proyects.mahjong.dealer.init_deck', return_value=['c1', 'c2']) as mock_init:
            dealer = MahjongDealer(mock_np_random)
            
            assert dealer.np_random == mock_np_random
            assert dealer.table == []
            assert dealer.deck == ['c1', 'c2']
            mock_init.assert_called_once()
            # Branch: Verify shuffle is called during __init__
            mock_np_random.shuffle.assert_called_with(['c1', 'c2'])

    def test_shuffle_method_branch(self, mock_np_random):
        """
        Covers the shuffle method branch explicitly.
        """
        with patch('Public_Proyects.mahjong.dealer.init_deck', return_value=['a']):
            dealer = MahjongDealer(mock_np_random)
            dealer.shuffle()
            # Branch: Verify shuffle logic is executed
            assert mock_np_random.shuffle.call_count == 2

    def test_deal_cards_loop_branches(self, mock_np_random):
        """
        Covers implicit branches in the for-loop structure:
        - Branch: loop does not execute (range(0))
        - Branch: loop executes one or more times
        """
        with patch('Public_Proyects.mahjong.dealer.init_deck', return_value=['c1', 'c2']):
            dealer = MahjongDealer(mock_np_random)
            mock_player = MagicMock()
            mock_player.hand = []

            # Branch: num = 0 (Loop body never entered)
            dealer.deal_cards(mock_player, 0)
            assert len(mock_player.hand) == 0

            # Branch: num > 0 (Loop body entered)
            dealer.deal_cards(mock_player, 1)
            assert len(mock_player.hand) == 1
            assert len(dealer.deck) == 1

    def test_deal_cards_exception_and_partial_execution(self, mock_np_random):
        """
        Covers the exception branch when the deck is depleted mid-loop.
        """
        with patch('Public_Proyects.mahjong.dealer.init_deck', return_value=['c1']):
            dealer = MahjongDealer(mock_np_random)
            mock_player = MagicMock()
            mock_player.hand = []
            
            # Requesting more cards than available triggers IndexError inside the loop
            with pytest.raises(IndexError):
                dealer.deal_cards(mock_player, 2)
            
            # Verify the partial state resulting from the failed operation
            assert len(mock_player.hand) == 1
            assert len(dealer.deck) == 0

    def test_deal_cards_boundary_exact_exhaustion(self, mock_np_random):
        """
        Covers the boundary branch where the deck becomes exactly empty.
        """
        with patch('Public_Proyects.mahjong.dealer.init_deck', return_value=['a', 'b']):
            dealer = MahjongDealer(mock_np_random)
            mock_player = MagicMock()
            mock_player.hand = []
            
            # Exhaust the deck
            dealer.deal_cards(mock_player, 2)
            assert len(dealer.deck) == 0
            assert len(mock_player.hand) == 2

    def test_init_with_empty_deck_branch(self, mock_np_random):
        """
        Covers branch for empty initial deck during instantiation.
        """
        with patch('Public_Proyects.mahjong.dealer.init_deck', return_value=[]):
            dealer = MahjongDealer(mock_np_random)
            assert dealer.deck == []
            # Verify shuffle branch is still taken even with empty list
            assert mock_np_random.shuffle.called

    def test_deal_cards_preservation(self, mock_np_random):
        """
        Ensures existing player hand state is maintained when appending.
        """
        with patch('Public_Proyects.mahjong.dealer.init_deck', return_value=['c1']):
            dealer = MahjongDealer(mock_np_random)
            mock_player = MagicMock()
            mock_player.hand = ['existing']
            
            dealer.deal_cards(mock_player, 1)
            assert 'existing' in mock_player.hand
            assert 'c1' in mock_player.hand
            assert len(mock_player.hand) == 2