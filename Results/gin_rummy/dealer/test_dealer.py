import pytest
from unittest.mock import MagicMock, patch
from Public_Proyects.gin_rummy.dealer import GinRummyDealer

class TestGinRummyDealer:

    @pytest.fixture
    def mock_np_random(self):
        mock = MagicMock()
        # Ensure shuffle does nothing to the list in place
        mock.shuffle.side_effect = lambda x: x
        return mock

    @pytest.fixture
    def deck_content(self):
        return ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']

    @pytest.fixture
    def dealer(self, mock_np_random, deck_content):
        with patch('utils.get_deck', return_value=list(deck_content)):
            return GinRummyDealer(mock_np_random)

    def test_init_initializes_piles_correctly(self, mock_np_random):
        test_deck = ['A', 'B', 'C']
        with patch('utils.get_deck', return_value=list(test_deck)):
            dealer = GinRummyDealer(mock_np_random)
            
            assert dealer.discard_pile == []
            assert len(dealer.shuffled_deck) == 3
            assert len(dealer.stock_pile) == 3
            mock_np_random.shuffle.assert_called_once()

    def test_deal_cards_updates_player_hand_and_stock(self, dealer):
        mock_player = MagicMock()
        mock_player.hand = []
        
        num_cards = 3
        dealer.deal_cards(mock_player, num_cards)
        
        assert len(mock_player.hand) == 3
        assert len(dealer.stock_pile) == 3
        mock_player.did_populate_hand.assert_called_once()

    def test_deal_cards_removes_from_stock_pile(self, dealer, deck_content):
        mock_player = MagicMock()
        mock_player.hand = []
        
        # El método pop() en Python extrae el último elemento de la lista.
        # Si el deck es ['C1', 'C2', 'C3', 'C4', 'C5', 'C6'],
        # al pedir 2 cartas, pop() sacará 'C6' y luego 'C5'.
        # Por lo tanto, el último elemento añadido a la mano será 'C5'.
        
        initial_stock_size = len(dealer.stock_pile)
        dealer.deal_cards(mock_player, 2)
        
        assert len(dealer.stock_pile) == initial_stock_size - 2
        assert mock_player.hand == ['C6', 'C5']
        assert mock_player.hand[-1] == 'C5'

    def test_deal_multiple_times(self, dealer):
        mock_player = MagicMock()
        mock_player.hand = []
        
        dealer.deal_cards(mock_player, 1)
        dealer.deal_cards(mock_player, 1)
        
        assert len(mock_player.hand) == 2
        assert len(dealer.stock_pile) == 4
        assert mock_player.did_populate_hand.call_count == 2