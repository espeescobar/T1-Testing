import pytest
from unittest.mock import MagicMock
from Public_Proyects.blackjack.judger import BlackjackJudger

class TestBlackjackJudger:
    @pytest.fixture
    def judger(self):
        mock_np_random = MagicMock()
        return BlackjackJudger(mock_np_random)

    def test_judge_score_basic(self, judger):
        card1 = MagicMock(rank="2")
        card2 = MagicMock(rank="3")
        assert judger.judge_score([card1, card2]) == 5

    def test_judge_score_ace_adjustment(self, judger):
        card1 = MagicMock(rank="A")
        card2 = MagicMock(rank="K")
        card3 = MagicMock(rank="2")
        # 11 + 10 + 2 = 23 -> 13
        assert judger.judge_score([card1, card2, card3]) == 13

    def test_judge_score_multiple_aces(self, judger):
        cards = [MagicMock(rank="A"), MagicMock(rank="A"), MagicMock(rank="9")]
        # 11 + 11 + 9 = 31 -> 21 -> 11
        assert judger.judge_score(cards) == 11

    def test_judge_round_alive(self, judger):
        player = MagicMock()
        player.hand = [MagicMock(rank="T")]
        status, score = judger.judge_round(player)
        assert status == "alive"
        assert score == 10

    def test_judge_round_bust(self, judger):
        player = MagicMock()
        player.hand = [MagicMock(rank="K"), MagicMock(rank="K"), MagicMock(rank="2")]
        status, score = judger.judge_round(player)
        assert status == "bust"
        assert score == 22

    def test_judge_game_player_bust(self, judger):
        game = MagicMock()
        game_pointer = 0
        game.players = {0: MagicMock(status='bust')}
        game.winner = {}
        judger.judge_game(game, game_pointer)
        assert game.winner['player0'] == -1

    def test_judge_game_dealer_bust_player_alive(self, judger):
        game = MagicMock()
        game_pointer = 0
        game.players = {0: MagicMock(status='alive')}
        game.dealer = MagicMock(status='bust')
        game.winner = {}
        judger.judge_game(game, game_pointer)
        assert game.winner['player0'] == 2

    def test_judge_game_win_by_score(self, judger):
        game = MagicMock()
        game_pointer = 0
        game.players = {0: MagicMock(status='alive', score=20)}
        game.dealer = MagicMock(status='alive', score=18)
        game.winner = {}
        judger.judge_game(game, game_pointer)
        assert game.winner['player0'] == 2

    def test_judge_game_lose_by_score(self, judger):
        game = MagicMock()
        game_pointer = 0
        game.players = {0: MagicMock(status='alive', score=17)}
        game.dealer = MagicMock(status='alive', score=19)
        game.winner = {}
        judger.judge_game(game, game_pointer)
        assert game.winner['player0'] == -1

    def test_judge_game_tie(self, judger):
        game = MagicMock()
        game_pointer = 0
        game.players = {0: MagicMock(status='alive', score=19)}
        game.dealer = MagicMock(status='alive', score=19)
        game.winner = {}
        judger.judge_game(game, game_pointer)
        assert game.winner['player0'] == 1