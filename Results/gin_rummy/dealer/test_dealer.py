import pytest
from unittest.mock import MagicMock, patch
from Public_Proyects.gin_rummy.dealer import GinRummyDealer

class TestGinRummyDealer:

    @pytest.fixture
    def mock_np_random(self):
        mock = MagicMock()
        # Ensure shuffle does nothing to the list in-place
        mock.shuffle = MagicMock(side_effect=lambda x: x)
        return mock

    @pytest.fixture
    def dealer(self, mock_np_random):
        with patch('utils.get_deck', return_value=['C1', 'C2', 'C3', 'C4', 'C5', 'C6']):
            return GinRummyDealer(mock_np_random)

    def test_init(self, mock_np_random):
        cards = ['C1', 'C2', 'C3']
        with patch('utils.get_deck', return_value=list(cards)):
            dealer = GinRummyDealer(mock_np_random)
            
            assert dealer.np_random == mock_np_random
            assert dealer.discard_pile == []
            assert len(dealer.stock_pile) == 3
            mock_np_random.shuffle.assert_called_once()

    def test_deal_cards(self, dealer):
        # Mock player
        mock_player = MagicMock()
        mock_player.hand = []
        
        # Initial stock size is 6
        num_cards_to_deal = 3
        dealer.deal_cards(mock_player, num_cards_to_deal)
        
        # Verify cards moved to player
        assert len(mock_player.hand) == 3
        assert len(dealer.stock_pile) == 3
        
        # Verify player method called
        mock_player.did_populate_hand.assert_called_once()

    def test_deal_cards_empty_stock_raises_error(self, dealer):
        mock_player = MagicMock()
        mock_player.hand = []
        
        # Deal all remaining cards
        dealer.deal_cards(mock_player, 6)
        assert len(dealer.stock_pile) == 0
        
        # Trying to deal more should raise IndexError from pop()
        with pytest.raises(IndexError):
            dealer.deal_cards(mock_player, 1)

    def test_deal_cards_interaction(self, dealer):
        mock_player = MagicMock()
        mock_player.hand = []
        
        dealer.deal_cards(mock_player, 1)
        
        assert len(mock_player.hand) == 1
        assert mock_player.did_populate_hand.called