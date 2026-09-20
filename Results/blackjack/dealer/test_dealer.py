import pytest
import numpy as np
from unittest.mock import MagicMock
from Public_Proyects.blackjack.dealer import init_standard_deck, BlackjackDealer

def test_init_standard_deck():
    deck = init_standard_deck()
    assert len(deck) == 52
    # Verificamos que contenga objetos (asumiendo que Card tiene representación)
    assert hasattr(deck[0], 'suit')
    assert hasattr(deck[0], 'rank')

def test_blackjack_dealer_initialization():
    mock_random = MagicMock(spec=np.random.RandomState)
    dealer = BlackjackDealer(mock_random, num_decks=1)
    
    assert len(dealer.deck) == 52
    assert dealer.status == 'alive'
    assert dealer.score == 0
    mock_random.shuffle.assert_called_once()

def test_blackjack_dealer_multiple_decks():
    mock_random = MagicMock(spec=np.random.RandomState)
    num_decks = 2
    dealer = BlackjackDealer(mock_random, num_decks=num_decks)
    
    assert len(dealer.deck) == 52 * num_decks

def test_shuffle():
    mock_random = MagicMock(spec=np.random.RandomState)
    dealer = BlackjackDealer(mock_random, num_decks=1)
    dealer.shuffle()
    
    assert mock_random.shuffle.called
    assert len(dealer.deck) == 52

def test_deal_card_finite_deck():
    mock_random = MagicMock(spec=np.random.RandomState)
    # Simulamos que elige el índice 0
    mock_random.choice.return_value = 0
    
    dealer = BlackjackDealer(mock_random, num_decks=1)
    player = MagicMock()
    player.hand = []
    
    initial_len = len(dealer.deck)
    dealer.deal_card(player)
    
    assert len(player.hand) == 1
    assert len(dealer.deck) == initial_len - 1

def test_deal_card_infinite_deck():
    mock_random = MagicMock(spec=np.random.RandomState)
    mock_random.choice.return_value = 0
    
    # num_decks = 0 implica infinito según la lógica del código
    dealer = BlackjackDealer(mock_random, num_decks=0)
    player = MagicMock()
    player.hand = []
    
    initial_len = len(dealer.deck)
    dealer.deal_card(player)
    
    assert len(player.hand) == 1
    assert len(dealer.deck) == initial_len

def test_deal_card_adds_correct_object():
    mock_random = MagicMock(spec=np.random.RandomState)
    mock_random.choice.return_value = 5
    
    dealer = BlackjackDealer(mock_random, num_decks=1)
    target_card = dealer.deck[5]
    
    player = MagicMock()
    player.hand = []
    
    dealer.deal_card(player)
    
    assert player.hand[0] == target_card