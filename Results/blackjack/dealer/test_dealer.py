import pytest
import numpy as np
from unittest.mock import MagicMock
from Public_Proyects.blackjack.dealer import init_standard_deck, BlackjackDealer

def test_init_standard_deck():
    deck = init_standard_deck()
    assert len(deck) == 52
    # Verificar que sean objetos de tipo Card (asumiendo que Card tiene representación de string o atributos)
    assert all(hasattr(card, 'suit') and hasattr(card, 'rank') for card in deck)

def test_blackjack_dealer_initialization():
    mock_rng = MagicMock(spec=np.random.RandomState)
    dealer = BlackjackDealer(mock_rng, num_decks=1)
    
    assert len(dealer.deck) == 52
    assert dealer.status == 'alive'
    assert dealer.score == 0
    assert dealer.num_decks == 1
    mock_rng.shuffle.assert_called()

def test_blackjack_dealer_multiple_decks():
    mock_rng = MagicMock(spec=np.random.RandomState)
    num_decks = 2
    dealer = BlackjackDealer(mock_rng, num_decks=num_decks)
    assert len(dealer.deck) == 52 * num_decks

def test_blackjack_dealer_infinite_decks():
    mock_rng = MagicMock(spec=np.random.RandomState)
    dealer = BlackjackDealer(mock_rng, num_decks=0)
    assert len(dealer.deck) == 52

def test_shuffle():
    mock_rng = MagicMock(spec=np.random.RandomState)
    dealer = BlackjackDealer(mock_rng, num_decks=1)
    initial_deck = list(dealer.deck)
    
    dealer.shuffle()
    
    assert mock_rng.shuffle.called
    assert len(dealer.deck) == 52

def test_deal_card_finite_deck():
    mock_rng = MagicMock(spec=np.random.RandomState)
    mock_rng.choice.return_value = 0
    
    dealer = BlackjackDealer(mock_rng, num_decks=1)
    mock_player = MagicMock()
    mock_player.hand = []
    
    initial_len = len(dealer.deck)
    dealer.deal_card(mock_player)
    
    assert len(mock_player.hand) == 1
    assert len(dealer.deck) == initial_len - 1
    assert mock_rng.choice.called

def test_deal_card_infinite_deck():
    mock_rng = MagicMock(spec=np.random.RandomState)
    mock_rng.choice.return_value = 0
    
    dealer = BlackjackDealer(mock_rng, num_decks=0)
    mock_player = MagicMock()
    mock_player.hand = []
    
    initial_len = len(dealer.deck)
    dealer.deal_card(mock_player)
    
    assert len(mock_player.hand) == 1
    assert len(dealer.deck) == initial_len  # No debería reducirse en modo infinito