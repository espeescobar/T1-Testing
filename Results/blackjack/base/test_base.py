import pytest
from unittest.mock import MagicMock
from Public_Proyects.blackjack.base import Card

def test_card_initialization():
    card = Card('S', 'A')
    assert card.suit == 'S'
    assert card.rank == 'A'

def test_card_equality_logic():
    card = Card('S', 'A')
    
    # Coverage: Branch 'if isinstance(other, Card)'
    assert card == Card('S', 'A')
    assert card != Card('H', 'A')
    assert card != Card('S', 'K')
    
    # Coverage: Branch 'else' in __eq__
    assert (card == "AS") is False
    assert card.__eq__(123) is NotImplemented

def test_card_hash_and_exceptions():
    # Coverage: Valid hash calculation
    card = Card('S', 'A')
    assert isinstance(hash(card), int)
    
    # Coverage: ValueError in .index() calls inside __hash__
    invalid_suit = Card('Z', 'A')
    with pytest.raises(ValueError):
        hash(invalid_suit)
        
    invalid_rank = Card('S', '1')
    with pytest.raises(ValueError):
        hash(invalid_rank)

def test_card_str():
    card = Card('C', 'T')
    assert str(card) == 'TC'

def test_card_get_index():
    card = Card('D', '5')
    assert card.get_index() == 'D5'

def test_card_equality_with_mock():
    # Coverage: Mocking with spec=Card allows passing isinstance(other, Card) check
    card = Card('S', 'A')
    
    mock_match = MagicMock(spec=Card)
    mock_match.suit = 'S'
    mock_match.rank = 'A'
    
    mock_mismatch = MagicMock(spec=Card)
    mock_mismatch.suit = 'H'
    mock_mismatch.rank = 'A'
    
    assert card == mock_match
    assert card != mock_mismatch

def test_full_matrix_of_types():
    # Ensuring every single valid path in index/hash logic is touched
    for suit in Card.valid_suit:
        for rank in Card.valid_rank:
            card = Card(suit, rank)
            assert card.get_index() == suit + rank
            assert str(card) == rank + suit
            assert isinstance(hash(card), int)

def test_comparison_with_none_type():
    card = Card('S', 'A')
    # Explicitly testing None branch in equality
    assert card.__eq__(None) is NotImplemented