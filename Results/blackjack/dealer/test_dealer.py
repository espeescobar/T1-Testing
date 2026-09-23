import pytest
import numpy as np
from unittest.mock import MagicMock
from Public_Proyects.blackjack.dealer import init_standard_deck, BlackjackDealer
from blackjack import Card

def test_init_standard_deck():
    deck = init_standard_deck()
    assert len(deck) == 52
    assert all(isinstance(card, Card) for card in deck)
    suits = {card.suit for card in deck}
    assert suits == {'S', 'H', 'D', 'C'}

@pytest.mark.parametrize("num_decks, expected_size", [
    (1, 52),
    (0, 52),
    (3, 156),
    (5, 260)
])
def test_blackjack_dealer_initialization_variations(num_decks, expected_size):
    mock_rng = MagicMock()
    dealer = BlackjackDealer(mock_rng, num_decks=num_decks)
    assert len(dealer.deck) == expected_size
    assert dealer.status == 'alive'
    assert dealer.score == 0
    assert dealer.hand == []

def test_shuffle():
    mock_rng = MagicMock()
    dealer = BlackjackDealer(mock_rng, num_decks=1)
    # Verificamos que np.array y shuffle se invocan correctamente
    dealer.shuffle()
    assert mock_rng.shuffle.called
    assert isinstance(dealer.deck, list)

def test_deal_card_finite_deck_branch():
    # Cubre la rama: if self.num_decks != 0
    mock_rng = MagicMock()
    mock_rng.choice.return_value = 0
    mock_player = MagicMock()
    mock_player.hand = []
    
    dealer = BlackjackDealer(mock_rng, num_decks=2)
    initial_len = len(dealer.deck)
    dealer.deal_card(mock_player)
    
    assert len(dealer.deck) == initial_len - 1
    assert len(mock_player.hand) == 1

def test_deal_card_infinite_deck_branch():
    # Cubre la rama else implícita: num_decks == 0
    mock_rng = MagicMock()
    mock_rng.choice.return_value = 0
    mock_player = MagicMock()
    mock_player.hand = []
    
    dealer = BlackjackDealer(mock_rng, num_decks=0)
    initial_len = len(dealer.deck)
    dealer.deal_card(mock_player)
    
    assert len(dealer.deck) == initial_len
    assert len(mock_player.hand) == 1

def test_blackjack_dealer_branch_logic_for_decks():
    # Cubre la rama if self.num_decks not in [0, 1]
    mock_rng = MagicMock()
    # Caso num_decks = 1 (no entra en el if)
    dealer_one = BlackjackDealer(mock_rng, num_decks=1)
    assert len(dealer_one.deck) == 52
    
    # Caso num_decks = 0 (no entra en el if)
    dealer_zero = BlackjackDealer(mock_rng, num_decks=0)
    assert len(dealer_zero.deck) == 52

    # Caso num_decks > 1 (entra en el if)
    dealer_multi = BlackjackDealer(mock_rng, num_decks=4)
    assert len(dealer_multi.deck) == 52 * 4

def test_deal_card_index_boundary():
    # Prueba de borde: elegir el último índice posible
    mock_rng = MagicMock()
    num_cards = 52
    mock_rng.choice.return_value = num_cards - 1
    mock_player = MagicMock()
    mock_player.hand = []
    
    dealer = BlackjackDealer(mock_rng, num_decks=1)
    last_card = dealer.deck[-1]
    dealer.deal_card(mock_player)
    
    assert mock_player.hand[0] == last_card
    assert len(dealer.deck) == num_cards - 1