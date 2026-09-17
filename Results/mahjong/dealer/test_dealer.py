import pytest
from unittest.mock import MagicMock, patch
from dealer import MahjongDealer

class MockPlayer:
    def __init__(self):
        self.hand = []

@pytest.fixture
def mock_random():
    rng = MagicMock()
    # Definimos que shuffle no haga nada para evitar errores durante la inicialización
    rng.shuffle.side_effect = lambda x: x
    return rng

@pytest.fixture
def dealer(mock_random):
    # Usamos patch para evitar errores si init_deck depende de imports externos
    with patch('dealer.init_deck', return_value=[f"card_{i}" for i in range(144)]):
        return MahjongDealer(mock_random)

def test_mahjong_dealer_initialization(dealer, mock_random):
    assert len(dealer.deck) == 144
    assert mock_random.shuffle.called
    assert dealer.table == []

def test_shuffle(dealer, mock_random):
    dealer.shuffle()
    # Verifica que shuffle fue llamado al menos dos veces (una en init, otra aquí)
    assert mock_random.shuffle.call_count >= 2

def test_deal_cards(dealer):
    player = MockPlayer()
    num_cards = 5
    
    initial_deck_size = len(dealer.deck)
    dealer.deal_cards(player, num_cards)
    
    assert len(player.hand) == num_cards
    assert len(dealer.deck) == initial_deck_size - num_cards
    # Verificamos que las cartas repartidas sean las del final del deck (stack)
    assert player.hand[0] == f"card_{initial_deck_size - 1}"