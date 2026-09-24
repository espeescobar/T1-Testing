import pytest
from unittest.mock import MagicMock
from Public_Proyects.gin_rummy.base import Card

def test_card_initialization():
    card = Card('S', 'A')
    assert card.suit == 'S'
    assert card.rank == 'A'

def test_card_equality():
    card1 = Card('H', '5')
    card2 = Card('H', '5')
    card3 = Card('D', '5')
    
    assert card1 == card2
    assert card1 != card3
    assert card1 != "5H"  # Testing against unrelated type

def test_card_hash():
    card1 = Card('S', 'A')
    card2 = Card('S', 'A')
    card3 = Card('H', '2')
    
    assert hash(card1) == hash(card2)
    assert hash(card1) != hash(card3)

def test_card_str():
    card = Card('C', 'T')
    assert str(card) == 'TC'

def test_card_get_index():
    card = Card('D', 'J')
    assert card.get_index() == 'DJ'

def test_card_hash_calculation():
    # Validating the specific logic: rank_index + 100 * suit_index
    # suit 'S' is index 0, rank 'A' is index 0 -> 0 + 100*0 = 0
    # suit 'H' is index 1, rank '2' is index 1 -> 1 + 100*1 = 101
    card1 = Card('S', 'A')
    card2 = Card('H', '2')
    
    assert hash(card1) == 0
    assert hash(card2) == 101

def test_mocked_card_behavior():
    # Using MagicMock for scenarios where we might need to simulate card objects
    mock_card = MagicMock(spec=Card)
    mock_card.suit = 'BJ'
    mock_card.rank = 'A'
    
    # Verify mock properties
    assert mock_card.suit == 'BJ'
    assert mock_card.rank == 'A'

@pytest.mark.parametrize("suit, rank", [
    ('S', 'A'),
    ('H', '2'),
    ('D', '3'),
    ('C', '4'),
    ('BJ', '5'),
    ('RJ', 'K')
])
def test_valid_card_combinations(suit, rank):
    card = Card(suit, rank)
    assert card.suit in Card.valid_suit
    assert card.rank in Card.valid_rank