import pytest
from unittest.mock import MagicMock
from Public_Proyects.blackjack.base import Card

def test_card_initialization():
    card = Card('S', 'A')
    assert card.suit == 'S'
    assert card.rank == 'A'

def test_card_equality():
    card1 = Card('H', 'K')
    card2 = Card('H', 'K')
    card3 = Card('D', 'A')
    
    assert card1 == card2
    assert card1 != card3
    assert card1 != "KH"  # Comparación con tipo distinto

def test_card_str_representation():
    card = Card('C', 'T')
    assert str(card) == 'TC'

def test_card_get_index():
    card = Card('D', '7')
    assert card.get_index() == 'D7'

def test_card_hash():
    card1 = Card('S', 'A')
    card2 = Card('S', 'A')
    card3 = Card('H', '2')
    
    assert hash(card1) == hash(card2)
    assert hash(card1) != hash(card3)

def test_card_hash_calculation():
    # S index 0, A index 0 -> 0 + 100*0 = 0
    card_sa = Card('S', 'A')
    # H index 1, 2 index 1 -> 1 + 100*1 = 101
    card_h2 = Card('H', '2')
    
    assert hash(card_sa) == 0
    assert hash(card_h2) == 101

def test_card_with_mock():
    # Ejemplo de uso de MagicMock según requerimiento
    mock_card = MagicMock(spec=Card)
    mock_card.suit = 'BJ'
    mock_card.rank = 'A'
    
    # Verificamos que el mock se comporta como esperamos en el contexto de la clase
    assert mock_card.suit == 'BJ'
    assert mock_card.rank == 'A'

def test_invalid_suit_in_hash_raises_error():
    # Intentar hashear una carta con suit inválido debería lanzar ValueError
    card = Card('INVALID', 'A')
    with pytest.raises(ValueError):
        hash(card)

def test_invalid_rank_in_hash_raises_error():
    card = Card('S', 'INVALID')
    with pytest.raises(ValueError):
        hash(card)