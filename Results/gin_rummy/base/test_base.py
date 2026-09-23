import pytest
from unittest.mock import MagicMock
from Public_Proyects.gin_rummy.base import Card

def test_card_initialization():
    card = Card('S', 'A')
    assert card.suit == 'S'
    assert card.rank == 'A'

def test_card_equality_branches():
    # Cobertura de rama: isinstance(other, Card) es True
    card1 = Card('H', 'K')
    card2 = Card('H', 'K')
    card3 = Card('H', 'Q')
    card4 = Card('D', 'K')
    
    # Evalúa el "and" en la rama True
    assert card1 == card2
    assert (card1 == card3) is False
    assert (card1 == card4) is False
    
    # Cobertura de rama: isinstance(other, Card) es False
    assert card1.__eq__("Not a card") is NotImplemented

def test_card_hash_and_index_branches():
    # Cobertura de camino normal para __hash__
    card = Card('H', '2')
    # Rank index 1 (for '2'), Suit index 1 (for 'H')
    assert hash(card) == 101
    
    # Cobertura de excepciones (invalid suit/rank) para cubrir ramas de .index()
    # Estas líneas cubren el caso donde .index() falla al no encontrar el elemento
    with pytest.raises(ValueError):
        invalid_card = Card('X', 'A')
        hash(invalid_card)
        
    with pytest.raises(ValueError):
        invalid_card = Card('S', '1')
        hash(invalid_card)

def test_card_str():
    card = Card('C', 'T')
    assert str(card) == 'TC'

def test_card_get_index():
    card = Card('D', '5')
    assert card.get_index() == 'D5'

def test_card_equality_with_mock():
    # Usando MagicMock para forzar ramas de isinstance en __eq__
    card = Card('S', 'A')
    
    # Caso: Objeto que es instancia de Card (mockeado)
    mock_card = MagicMock(spec=Card)
    mock_card.rank = 'A'
    mock_card.suit = 'S'
    assert card == mock_card
    
    # Caso: Objeto distinto de Card para la rama else
    mock_other = MagicMock()
    assert card.__eq__(mock_other) is NotImplemented

def test_card_hash_complex_mock():
    # Mock para cubrir la lógica de __hash__ sin usar datos reales de la clase
    # Forzamos los índices para cubrir la lógica de cálculo
    mock_card = MagicMock(spec=Card)
    mock_card.suit = 'RJ'
    mock_card.rank = 'K'
    
    # Inyectar comportamiento esperado mediante el acceso a las constantes de clase
    # RJ index 5, K index 12. Hash = 12 + 100 * 5 = 512
    assert Card.__hash__(mock_card) == 512

@pytest.mark.parametrize("suit", ['S', 'H', 'D', 'C', 'BJ', 'RJ'])
@pytest.mark.parametrize("rank", ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K'])
def test_card_all_valid_combinations(suit, rank):
    # Test exhaustivo de todas las combinaciones posibles
    card = Card(suit, rank)
    assert card.suit == suit
    assert card.rank == rank
    assert str(card) == rank + suit
    assert card.get_index() == suit + rank
    assert hash(card) >= 0

def test_card_equality_identity():
    # Caso de borde: comparar la misma instancia
    card = Card('S', 'A')
    assert card == card