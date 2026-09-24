import pytest
from unittest.mock import MagicMock
from Public_Proyects.blackjack.judger import BlackjackJudger

class TestBlackjackJudger:
    @pytest.fixture
    def judger(self):
        mock_np_random = MagicMock()
        return BlackjackJudger(mock_np_random)

    def test_judge_score_basic(self, judger):
        card_t = MagicMock(rank='T')
        card_5 = MagicMock(rank='5')
        assert judger.judge_score([card_t, card_5]) == 15

    def test_judge_score_ace_adjustment(self, judger):
        card_a = MagicMock(rank='A')
        card_k = MagicMock(rank='K')
        card_5 = MagicMock(rank='5')
        # A(11) + K(10) + 5 = 26 -> adjusts to 1 + 10 + 5 = 16
        assert judger.judge_score([card_a, card_k, card_5]) == 16

    def test_judge_round_alive(self, judger):
        mock_player = MagicMock()
        mock_player.hand = [MagicMock(rank='2'), MagicMock(rank='3')]
        status, score = judger.judge_round(mock_player)
        assert status == 'alive'
        assert score == 5

    def test_judge_round_bust(self, judger):
        mock_player = MagicMock()
        mock_player.hand = [MagicMock(rank='K'), MagicMock(rank='Q'), MagicMock(rank='5')]
        status, score = judger.judge_round(mock_player)
        assert status == 'bust'
        assert score == 25

    def test_judge_game_player_bust(self, judger):
        mock_game = MagicMock()
        mock_pointer = 0
        mock_game.players = [MagicMock(status='bust')]
        mock_game.winner = {}
        
        judger.judge_game(mock_game, mock_pointer)
        assert mock_game.winner['player0'] == -1

    def test_judge_game_dealer_bust_player_alive(self, judger):
        mock_game = MagicMock()
        mock_pointer = 0
        mock_game.players = [MagicMock(status='alive')]
        mock_game.dealer = MagicMock(status='bust')
        mock_game.winner = {}
        
        judger.judge_game(mock_game, mock_pointer)
        assert mock_game.winner['player0'] == 2

    def test_judge_game_player_wins_score(self, judger):
        mock_game = MagicMock()
        mock_pointer = 0
        mock_game.players = [MagicMock(status='alive', score=20)]
        mock_game.dealer = MagicMock(status='alive', score=18)
        mock_game.winner = {}
        
        judger.judge_game(mock_game, mock_pointer)
        assert mock_game.winner['player0'] == 2

    def test_judge_game_dealer_wins_score(self, judger):
        mock_game = MagicMock()
        mock_pointer = 0
        mock_game.players = [MagicMock(status='alive', score=15)]
        mock_game.dealer = MagicMock(status='alive', score=19)
        mock_game.winner = {}
        
        judger.judge_game(mock_game, mock_pointer)
        assert mock_game.winner['player0'] == -1

    def test_judge_game_tie(self, judger):
        mock_game = MagicMock()
        mock_pointer = 0
        mock_game.players = [MagicMock(status='alive', score=18)]
        mock_game.dealer = MagicMock(status='alive', score=18)
        mock_game.winner = {}
        
        judger.judge_game(mock_game, mock_pointer)
        assert mock_game.winner['player0'] == 1