import pytest
from unittest.mock import MagicMock, patch
from Public_Proyects.mahjong.dealer import MahjongDealer

class TestMahjongDealer:

    @pytest.fixture
    def mock_np_random(self):
        return MagicMock()

    @pytest.fixture
    def dealer(self, mock_np_random):
        # Utilizamos patch como gestor de contexto dentro del fixture
        # para evitar el error de inyección de argumentos de pytest
        with patch('Public_Proyects.mahjong.dealer.init_deck') as mock_init:
            mock_init.return_value = ["card1", "card2", "card3", "card4", "card5"]
            dealer_instance = MahjongDealer(mock_np_random)
            # Retornamos la instancia configurada
            return dealer_instance

    def test_init(self, mock_np_random, dealer):
        assert dealer.np_random == mock_np_random
        assert dealer.table == []
        assert len(dealer.deck) == 5
        # Verifica que shuffle fue llamado al inicializar
        assert dealer.np_random.shuffle.called

    def test_shuffle(self, dealer):
        initial_deck = list(dealer.deck)
        dealer.shuffle()
        # Se llamó una vez en __init__ y otra en test_shuffle
        assert dealer.np_random.shuffle.call_count == 2
        assert dealer.deck == initial_deck

    def test_deal_cards(self, dealer):
        mock_player = MagicMock()
        mock_player.hand = []
        
        num_cards = 3
        dealer.deal_cards(mock_player, num_cards)
        
        assert len(mock_player.hand) == num_cards
        assert len(dealer.deck) == 2
        # El pop toma del final: "card5", luego "card4", luego "card3"
        assert mock_player.hand == ["card5", "card4", "card3"]

    def test_deal_cards_empty_deck(self, dealer):
        dealer.deck = []
        mock_player = MagicMock()
        mock_player.hand = []
        
        with pytest.raises(IndexError):
            dealer.deal_cards(mock_player, 1)

    def test_init_calls_init_deck(self, mock_np_random):
        with patch('Public_Proyects.mahjong.dealer.init_deck') as mock_init:
            mock_init.return_value = ["c1"]
            MahjongDealer(mock_np_random)
            mock_init.assert_called_once()