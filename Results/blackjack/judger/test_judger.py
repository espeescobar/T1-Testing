import pytest
from unittest.mock import MagicMock
from Public_Proyects.blackjack.judger import BlackjackJudger

class TestBlackjackJudger:
    @pytest.fixture
    def judger(self):
        return BlackjackJudger(MagicMock())

    def test_judge_round_branches(self, judger):
        # Rama if (score <= 21)
        player_alive = MagicMock()
        player_alive.hand = [MagicMock(rank="T")]
        status, score = judger.judge_round(player_alive)
        assert status == "alive"
        assert score == 10

        # Rama else (score > 21)
        player_bust = MagicMock()
        player_bust.hand = [MagicMock(rank="T"), MagicMock(rank="T"), MagicMock(rank="2")]
        status, score = judger.judge_round(player_bust)
        assert status == "bust"
        assert score == 22

    def test_judge_game_branches(self, judger):
        # 1. Rama if: player bust
        game = MagicMock()
        game.players = {0: MagicMock(status='bust')}
        game.winner = {}
        judger.judge_game(game, 0)
        assert game.winner['player0'] == -1

        # 2. Rama elif: dealer bust (player not bust)
        game.players = {0: MagicMock(status='alive')}
        game.dealer = MagicMock(status='bust')
        game.winner = {}
        judger.judge_game(game, 0)
        assert game.winner['player0'] == 2

        # 3. Rama else: both not bust
        # 3a. Sub-rama: player > dealer
        game.players = {0: MagicMock(status='alive', score=20)}
        game.dealer = MagicMock(status='alive', score=10)
        game.winner = {}
        judger.judge_game(game, 0)
        assert game.winner['player0'] == 2

        # 3b. Sub-rama: player < dealer
        game.players = {0: MagicMock(status='alive', score=10)}
        game.dealer = MagicMock(status='alive', score=20)
        game.winner = {}
        judger.judge_game(game, 0)
        assert game.winner['player0'] == -1

        # 3c. Sub-rama: else (tie)
        game.players = {0: MagicMock(status='alive', score=15)}
        game.dealer = MagicMock(status='alive', score=15)
        game.winner = {}
        judger.judge_game(game, 0)
        assert game.winner['player0'] == 1

    def test_judge_score_branches(self, judger):
        # Bucle for vacio
        assert judger.judge_score([]) == 0
        
        # Bucle for, caso normal sin Ases
        assert judger.judge_score([MagicMock(rank="2"), MagicMock(rank="3")]) == 5
        
        # As con valor inicial 11
        assert judger.judge_score([MagicMock(rank="A")]) == 11
        
        # Bucle while: condición score > 21
        # [A, A] -> 11 + 11 = 22. Entra al while -> 12
        assert judger.judge_score([MagicMock(rank="A"), MagicMock(rank="A")]) == 12
        
        # Bucle while: condición count_a > 0
        # [A, A, A, A] -> 44 -> 34 -> 24 -> 14
        assert judger.judge_score([MagicMock(rank="A"), MagicMock(rank="A"), MagicMock(rank="A"), MagicMock(rank="A")]) == 14
        
        # Caso borde: Reducción exacta a 21
        # [A, A, 9] -> 11 + 11 + 9 = 31 -> 21
        assert judger.judge_score([MagicMock(rank="A"), MagicMock(rank="A"), MagicMock(rank="9")]) == 21

    def test_init_and_errors(self, judger):
        mock_rand = MagicMock()
        j = BlackjackJudger(mock_rand)
        assert j.np_random == mock_rand
        
        # Validación de estructura de datos
        assert j.rank2score['A'] == 11
        
        # Error en input (KeyError al acceder a ranking inexistente)
        with pytest.raises(KeyError):
            j.judge_score([MagicMock(rank="Z")])