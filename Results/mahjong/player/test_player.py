import pytest
from unittest.mock import MagicMock
from Public_Proyects.mahjong.player import MahjongPlayer

@pytest.fixture
def player():
    np_random = MagicMock()
    return MahjongPlayer(player_id=1, np_random=np_random)

@pytest.fixture
def mock_card():
    card = MagicMock()
    card.get_str.return_value = "TestCard"
    return card

def test_init(player):
    assert player.get_player_id() == 1
    assert player.hand == []
    assert player.pile == []

def test_play_card(player, mock_card):
    dealer = MagicMock()
    dealer.table = []
    player.hand = [mock_card]
    
    player.play_card(dealer, mock_card)
    
    assert len(player.hand) == 0
    assert mock_card in dealer.table

def test_chow(player):
    dealer = MagicMock()
    last_card = MagicMock()
    card1 = MagicMock()
    card2 = MagicMock()
    
    dealer.table = [last_card]
    player.hand = [card1, card2]
    chow_cards = [card1, card2, last_card]
    
    player.chow(dealer, [card1, card2])
    
    assert len(player.hand) == 0
    assert [card1, card2] in player.pile
    assert len(dealer.table) == 0

def test_gong(player):
    dealer = MagicMock()
    card1 = MagicMock()
    card2 = MagicMock()
    
    player.hand = [card1, card2]
    gong_cards = [card1, card2]
    
    player.gong(dealer, gong_cards)
    
    assert len(player.hand) == 0
    assert gong_cards in player.pile

def test_pong(player):
    dealer = MagicMock()
    card1 = MagicMock()
    card2 = MagicMock()
    
    player.hand = [card1, card2]
    pong_cards = [card1, card2]
    
    player.pong(dealer, pong_cards)
    
    assert len(player.hand) == 0
    assert pong_cards in player.pile

def test_print_hand(player, capsys, mock_card):
    player.hand = [mock_card]
    player.print_hand()
    captured = capsys.readouterr()
    assert "['TestCard']" in captured.out

def test_print_pile(player, mock_card):
    player.pile = [[mock_card]]
    player.print_pile()
    # Simple check for print execution
    assert True 