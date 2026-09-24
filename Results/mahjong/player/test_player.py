import pytest
from unittest.mock import MagicMock
from Public_Proyects.mahjong.player import MahjongPlayer

@pytest.fixture
def player():
    np_random = MagicMock()
    return MahjongPlayer(player_id=1, np_random=np_random)

def test_init(player):
    assert player.get_player_id() == 1
    assert player.hand == []
    assert player.pile == []

def test_play_card(player):
    card = MagicMock()
    card.get_str.return_value = "Card1"
    player.hand = [card]
    dealer = MagicMock()
    dealer.table = []

    player.play_card(dealer, card)

    assert len(player.hand) == 0
    assert card in dealer.table

def test_chow(player):
    card_a = MagicMock()
    card_b = MagicMock()
    last_card = MagicMock()
    
    player.hand = [card_a, card_b]
    dealer = MagicMock()
    dealer.table = [last_card]
    
    cards_to_chow = [card_a, card_b, last_card]
    
    player.chow(dealer, cards_to_chow)
    
    assert len(dealer.table) == 0
    assert len(player.hand) == 0
    assert cards_to_chow in player.pile

def test_gong(player):
    card1 = MagicMock()
    card2 = MagicMock()
    player.hand = [card1, card2]
    dealer = MagicMock()
    cards = [card1, card2]
    
    player.gong(dealer, cards)
    
    assert len(player.hand) == 0
    assert cards in player.pile

def test_pong(player):
    card1 = MagicMock()
    card2 = MagicMock()
    player.hand = [card1, card2]
    dealer = MagicMock()
    cards = [card1, card2]
    
    player.pong(dealer, cards)
    
    assert len(player.hand) == 0
    assert cards in player.pile

def test_print_hand(capsys, player):
    card = MagicMock()
    card.get_str.return_value = "TestCard"
    player.hand = [card]
    
    player.print_hand()
    captured = capsys.readouterr()
    assert captured.out.strip() == "['TestCard']"

def test_print_pile(capsys, player):
    card = MagicMock()
    card.get_str.return_value = "PileCard"
    player.pile = [[card]]
    
    player.print_pile()
    captured = capsys.readouterr()
    assert captured.out.strip() == "[['PileCard']]"