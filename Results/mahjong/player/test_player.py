import pytest
from unittest.mock import MagicMock
from Public_Proyects.mahjong.player import MahjongPlayer

@pytest.fixture
def player():
    return MahjongPlayer(player_id=1, np_random=MagicMock())

def test_play_card(player):
    card_to_play = MagicMock()
    card_stay = MagicMock()
    player.hand = [card_to_play, card_stay]
    
    dealer = MagicMock()
    dealer.table = []
    
    player.play_card(dealer, card_to_play)
    
    assert card_to_play not in player.hand
    assert card_to_play in dealer.table
    assert len(player.hand) == 1

def test_chow(player):
    # El código fuente hace: 
    # 1. last_card = dealer.table.pop(-1)
    # 2. itera sobre cards: si card está en hand y card != last_card, se remueve.
    
    dealer = MagicMock()
    last_card = MagicMock(name="table_card")
    dealer.table = [MagicMock(), last_card] # last_card es el último
    
    c1, c2 = MagicMock(name="h1"), MagicMock(name="h2")
    player.hand = [c1, c2, MagicMock()]
    
    # El set de chow debe incluir el último de la mesa y cartas de la mano
    cards_to_chow = [c1, c2, last_card]
    
    player.chow(dealer, cards_to_chow)
    
    # El último de la mesa debe haber sido removido
    assert last_card not in dealer.table
    # c1 y c2 deberían haber salido de la mano
    assert c1 not in player.hand
    assert c2 not in player.hand
    assert cards_to_chow in player.pile

def test_gong(player):
    c1, c2 = MagicMock(), MagicMock()
    player.hand = [c1, c2, MagicMock()]
    dealer = MagicMock()
    
    cards = [c1, c2]
    player.gong(dealer, cards)
    
    assert c1 not in player.hand
    assert c2 not in player.hand
    assert cards in player.pile

def test_pong(player):
    c1, c2 = MagicMock(), MagicMock()
    player.hand = [c1, c2]
    dealer = MagicMock()
    
    cards = [c1, c2]
    player.pong(dealer, cards)
    
    assert len(player.hand) == 0
    assert cards in player.pile

def test_print_hand(capsys, player):
    mock_card = MagicMock()
    mock_card.get_str.return_value = "5m"
    player.hand = [mock_card]
    
    player.print_hand()
    captured = capsys.readouterr()
    assert "['5m']" in captured.out

def test_print_pile(capsys, player):
    mock_card = MagicMock()
    mock_card.get_str.return_value = "5m"
    player.pile = [[mock_card]]
    
    player.print_pile()
    captured = capsys.readouterr()
    assert "[['5m']]" in captured.out