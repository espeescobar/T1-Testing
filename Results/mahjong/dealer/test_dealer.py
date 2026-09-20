import pytest
from unittest.mock import MagicMock, patch
from Public_Proyects.mahjong.dealer import MahjongDealer

class TestMahjongDealer:

    @pytest.fixture
    def mock_np_random(self):
        return MagicMock()

    @pytest.fixture
    def dealer(self, mock_np_random):
        with patch('Public_Proyects.mahjong.dealer.init_deck') as mock_init:
            # Creamos una lista de mocks numerados para identificar las cartas
            mock_cards = [MagicMock(name=f"card_{i}") for i in range(10)]
            mock_init.return_value = list(mock_cards)
            return MahjongDealer(mock_np_random)

    def test_init(self, mock_np_random):
        with patch('Public_Proyects.mahjong.dealer.init_deck') as mock_init:
            mock_deck = [MagicMock()]
            mock_init.return_value = mock_deck
            
            dealer = MahjongDealer(mock_np_random)
            
            assert dealer.np_random == mock_np_random
            assert dealer.deck == mock_deck
            assert dealer.table == []
            mock_np_random.shuffle.assert_called_once_with(mock_deck)

    def test_shuffle(self, dealer, mock_np_random):
        dealer.shuffle()
        mock_np_random.shuffle.assert_called_with(dealer.deck)

    def test_deal_cards(self, dealer):
        # Configuración del jugador mock con lista real para 'hand'
        mock_player = MagicMock()
        mock_player.hand = []
        
        # Guardamos referencias a las cartas antes de repartir
        # Como el método usa pop(), las cartas repartidas son las que estaban al final
        initial_deck = list(dealer.deck)
        num_cards_to_deal = 3
        expected_cards = initial_deck[-num_cards_to_deal:]
        
        dealer.deal_cards(mock_player, num_cards_to_deal)
        
        # Verificamos longitud
        assert len(mock_player.hand) == num_cards_to_deal
        assert len(dealer.deck) == len(initial_deck) - num_cards_to_deal
        
        # Verificamos que las cartas en la mano sean las que se retiraron del final del deck
        # El orden en hand será [última, penúltima, antepenúltima] debido al pop()
        assert mock_player.hand == expected_cards[::-1]
        
    def test_deal_cards_empty_deck_behavior(self, dealer):
        # Vaciamos el deck
        dealer.deck = []
        mock_player = MagicMock()
        mock_player.hand = []
        
        # Intentar repartir de un deck vacío debe lanzar IndexError por el pop()
        with pytest.raises(IndexError):
            dealer.deal_cards(mock_player, 1)

    def test_integration_with_multiple_cards(self, dealer):
        mock_player = MagicMock()
        mock_player.hand = []
        
        # Repartir 5 cartas
        dealer.deal_cards(mock_player, 5)
        
        assert len(mock_player.hand) == 5