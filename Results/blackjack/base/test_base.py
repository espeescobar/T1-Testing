import pytest
from unittest.mock import MagicMock
from Public_Proyects.blackjack.base import Card

def test_card_initialization():
    card = Card('H', 'A')
    assert card.suit == 'H'
    assert card.rank == 'A'

def test_card_equality():
    card1 = Card('S', 'K')
    card2 = Card('S', 'K')
    card3 = Card('H', 'A')
    
    assert card1 == card2
    assert card1 != card3
    assert card1 != "SK"
    # La comparación (card1 == 123) retorna el objeto NotImplemented, 
    # pero en Python, al evaluar "if (card1 == 123) is NotImplemented" el resultado 
    # depende de cómo el operador == maneja el resultado de NotImplemented.
    # Se corrige para verificar explícitamente el valor retornado por el método __eq__
    assert card1.__eq__(123) is NotImplemented

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

def test_card_with_mock():
    # Utilizando MagicMock para simular objetos Card manteniendo la integridad de la clase
    mock_card = MagicMock(spec=Card)
    mock_card.suit = 'BJ'
    mock_card.rank = 'A'
    
    assert mock_card.suit == 'BJ'
    assert mock_card.rank == 'A'

@pytest.mark.parametrize("suit, rank", [
    ('S', 'A'), ('H', '2'), ('D', '3'), ('C', '4'), ('BJ', '5'), ('RJ', 'T')
])
def test_valid_card_creation(suit, rank):
    card = Card(suit, rank)
    assert card.suit == suit
    assert card.rank == rank

def test_hash_calculation_logic():
    # Verificación de la fórmula: rank_index + 100 * suit_index
    # S(0), A(0) -> 0 + 0 = 0
    # H(1), 2(1) -> 1 + 100 = 101
    card1 = Card('S', 'A')
    card2 = Card('H', '2')
    
    assert hash(card1) == 0
    assert hash(card2) == 101