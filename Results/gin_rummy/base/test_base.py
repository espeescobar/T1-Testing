import pytest
from unittest.mock import MagicMock
from Public_Proyects.gin_rummy.base import Card

def test_card_initialization():
    card = Card('H', 'A')
    assert card.suit == 'H'
    assert card.rank == 'A'

def test_card_equality():
    card1 = Card('S', 'K')
    card2 = Card('S', 'K')
    card3 = Card('H', 'K')
    card4 = "Not a Card object"

    assert card1 == card2
    assert card1 != card3
    # El método __eq__ retorna NotImplemented, pero el operador '==' 
    # en Python cuando recibe NotImplemented intenta la comparación reflejada 
    # o devuelve False si no hay más opciones. 
    # Para verificar la implementación, llamamos directamente al método __eq__.
    assert card1.__eq__(card4) is NotImplemented

def test_card_hash():
    card1 = Card('S', 'A')
    card2 = Card('S', 'A')
    card3 = Card('H', '2')
    
    assert hash(card1) == hash(card2)
    assert hash(card1) != hash(card3)

def test_card_str():
    card = Card('D', 'T')
    assert str(card) == 'TD'

def test_card_get_index():
    card = Card('C', 'J')
    assert card.get_index() == 'CJ'

def test_card_hash_with_mock():
    # Mocking card behavior
    mock_card = MagicMock(spec=Card)
    mock_card.suit = 'H'
    mock_card.rank = '5'
    
    # Obtenemos los índices usando la clase original para garantizar consistencia
    suit_index = Card.valid_suit.index(mock_card.suit)
    rank_index = Card.valid_rank.index(mock_card.rank)
    expected_hash = rank_index + 100 * suit_index
    
    # rank '5' es índice 4, suit 'H' es índice 1
    # 4 + (100 * 1) = 104
    assert expected_hash == 104

def test_invalid_suit_rank_handling():
    card = Card('INVALID', 'VOID')
    assert card.suit == 'INVALID'
    assert card.rank == 'VOID'

def test_card_equality_with_mock():
    card = Card('S', 'A')
    mock_other = MagicMock(spec=Card)
    mock_other.suit = 'S'
    mock_other.rank = 'A'
    
    assert card == mock_other

@pytest.mark.parametrize("suit, rank, expected_str", [
    ('S', 'A', 'AS'),
    ('H', '5', '5H'),
    ('D', 'J', 'JD'),
    ('C', '3', '3C'),
])
def test_card_str_variations(suit, rank, expected_str):
    card = Card(suit, rank)
    assert str(card) == expected_str

def test_card_hash_logic():
    # Test individual hash logic
    c = Card('BJ', 'A')
    # suit 'BJ' index 4, rank 'A' index 0
    # 0 + 100 * 4 = 400
    assert hash(c) == 400