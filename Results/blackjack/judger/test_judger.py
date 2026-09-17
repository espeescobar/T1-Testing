import pytest
from unittest.mock import MagicMock
from Public_Proyects.blackjack.judger import BlackjackJudger

@pytest.fixture
def judger():
    return BlackjackJudger(np_random=None)

def test_judge_score_simple():
    judger = BlackjackJudger(None)
    card1 = MagicMock(rank='2')
    card2 = MagicMock(rank='T')
    assert judger.judge_score([card1, card2]) == 12

def test_judge_score_with_ace_adjustment():
    judger = BlackjackJudger(None)
    card1 = MagicMock(rank='A')
    card2 = MagicMock(rank='A')
    card3 = MagicMock(rank='9')
    # 11+11+9 = 31 -> adjusted to 1+1+9 = 11
    assert judger.judge_score([card1, card2, card3]) == 21

def test_judge_round_alive():
    judger = BlackjackJudger(None)
    player = MagicMock()
    player.hand = [MagicMock(rank='5'), MagicMock(rank='5')]
    status, score = judger.judge_round(player)
    assert status == "alive"
    assert score == 10

def test_judge_round_bust():
    judger = BlackjackJudger(None)
    player = MagicMock()
    player.hand = [MagicMock(rank='K'), MagicMock(rank='K'), MagicMock(rank='5')]
    status, score = judger.judge_round(player)
    assert status == "bust"
    assert score == 25

def test_judge_game_player_bust():
    judger = BlackjackJudger(None)
    game = MagicMock()
    game.players = [MagicMock(status='bust')]
    game.winner = {}
    judger.judge_game(game, 0)
    assert game.winner['player0'] == -1

def test_judge_game_dealer_bust_player_not_bust():
    judger = BlackjackJudger(None)
    game = MagicMock()
    game.players = [MagicMock(status='alive')]
    game.dealer = MagicMock(status='bust')
    game.winner = {}
    judger.judge_game(game, 0)
    assert game.winner['player0'] == 2

def test_judge_game_player_win():
    judger = BlackjackJudger(None)
    game = MagicMock()
    player = MagicMock(status='alive', score=20)
    dealer = MagicMock(status='alive', score=18)
    game.players = [player]
    game.dealer = dealer
    game.winner = {}
    judger.judge_game(game, 0)
    assert game.winner['player0'] == 2

def test_judge_game_player_lose():
    judger = BlackjackJudger(None)
    game = MagicMock()
    player = MagicMock(status='alive', score=15)
    dealer = MagicMock(status='alive', score=19)
    game.players = [player]
    game.dealer = dealer
    game.winner = {}
    judger.judge_game(game, 0)
    assert game.winner['player0'] == -1

def test_judge_game_tie():
    judger = BlackjackJudger(None)
    game = MagicMock()
    player = MagicMock(status='alive', score=18)
    dealer = MagicMock(status='alive', score=18)
    game.players = [player]
    game.dealer = dealer
    game.winner = {}
    judger.judge_game(game, 0)
    assert game.winner['player0'] == 1