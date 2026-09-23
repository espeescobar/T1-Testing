import pytest
from unittest.mock import MagicMock, patch
from Public_Proyects.gin_rummy.dealer import GinRummyDealer

class TestGinRummyDealer:

    @pytest.fixture
    def mock_np_random(self):
        return MagicMock()

    def test_init_state(self, mock_np_random):
        with patch('Public_Proyects.gin_rummy.dealer.utils') as mock_utils:
            mock_deck = ["C1", "C2"]
            mock_utils.get_deck.return_value = list(mock_deck)
            
            dealer = GinRummyDealer(mock_np_random)
            
            assert dealer.discard_pile == []
            assert len(dealer.stock_pile) == 2
            assert dealer.shuffled_deck is not dealer.stock_pile 
            mock_np_random.shuffle.assert_called_once_with(dealer.shuffled_deck)

    @pytest.mark.parametrize("num_cards", [0, 1, 3])
    def test_deal_cards_loop_variations(self, mock_np_random, num_cards):
        """
        Covers the range(num) loop logic.
        """
        with patch('Public_Proyects.gin_rummy.dealer.utils') as mock_utils:
            mock_utils.get_deck.return_value = ["C1", "C2", "C3"]
            dealer = GinRummyDealer(mock_np_random)
            
            player = MagicMock()
            player.hand = []
            
            dealer.deal_cards(player, num_cards)
            
            assert len(player.hand) == num_cards
            assert player.did_populate_hand.called is True

    def test_deal_cards_pop_logic(self, mock_np_random):
        with patch('Public_Proyects.gin_rummy.dealer.utils') as mock_utils:
            mock_utils.get_deck.return_value = ["Bottom", "Top"]
            dealer = GinRummyDealer(mock_np_random)
            player = MagicMock()
            player.hand = []
            
            dealer.deal_cards(player, 1)
            
            assert player.hand == ["Top"]
            assert dealer.stock_pile == ["Bottom"]

    def test_deal_cards_exception_branch(self, mock_np_random):
        """
        Covers the branch where the loop runs for more items than exist in the stock_pile.
        """
        with patch('Public_Proyects.gin_rummy.dealer.utils') as mock_utils:
            mock_utils.get_deck.return_value = ["C1"]
            dealer = GinRummyDealer(mock_np_random)
            player = MagicMock()
            # Initialize hand as a real list to track state during iteration
            player.hand = []
            
            # Attempt to deal 2 cards when only 1 is available
            with pytest.raises(IndexError):
                dealer.deal_cards(player, 2)
            
            # After IndexError, the loop terminates immediately upon the second iteration.
            # Only one card should have been appended before the crash.
            assert len(player.hand) == 1
            assert len(dealer.stock_pile) == 0

    def test_did_populate_hand_called_always(self, mock_np_random):
        """
        Ensures that did_populate_hand is called even if range(num) is empty (0).
        """
        with patch('Public_Proyects.gin_rummy.dealer.utils') as mock_utils:
            mock_utils.get_deck.return_value = []
            dealer = GinRummyDealer(mock_np_random)
            player = MagicMock()
            
            dealer.deal_cards(player, 0)
            
            player.did_populate_hand.assert_called_once()