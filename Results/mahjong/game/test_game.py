import pytest
from unittest.mock import MagicMock, patch
from Public_Proyects.mahjong.game import MahjongGame

class TestMahjongGame:

    @pytest.fixture
    def game(self):
        return MahjongGame(allow_step_back=True)

    def test_init_game_branches(self):
        # Probar inicialización completa cubriendo la lógica de deal_cards
        game = MahjongGame(allow_step_back=True)
        mock_dealer = MagicMock()
        mock_player = MagicMock()
        mock_judger = MagicMock()
        mock_round = MagicMock()
        mock_round.current_player = 0
        
        with patch('Public_Proyects.mahjong.game.Dealer', return_value=mock_dealer), \
             patch('Public_Proyects.mahjong.game.Player', return_value=mock_player), \
             patch('Public_Proyects.mahjong.game.Judger', return_value=mock_judger), \
             patch('Public_Proyects.mahjong.game.Round', return_value=mock_round):
            
            game.init_game()
            # Verifica que el dealer haya repartido cartas (13*4 + 1)
            assert mock_dealer.deal_cards.call_count == 5
            assert hasattr(game, 'cur_state')

    def test_step_logic_branch(self, game):
        # Probar el branch 'if self.allow_step_back' con True y False
        game.dealer = MagicMock()
        game.players = []
        game.round = MagicMock()
        game.history = []
        
        # Branch True
        game.step("action")
        assert len(game.history) == 1
        
        # Branch False
        game.allow_step_back = False
        game.step("action")
        assert len(game.history) == 1  # No debe aumentar

    def test_step_back_logic(self, game):
        # Branch: Historial vacío (ya probado), Historial con elementos (rama else)
        game.history = [("d1", "p1", "r1")]
        # Preparar mocks para el unpacking
        mock_d, mock_p, mock_r = MagicMock(), MagicMock(), MagicMock()
        game.history.append((mock_d, mock_p, mock_r))
        
        assert game.step_back() is True
        assert game.dealer == mock_d
        assert game.players == mock_p
        assert game.round == mock_r

    def test_get_legal_actions_logic(self):
        # Branch: valid_act es ['play']
        state1 = {'valid_act': ['play'], 'action_cards': ['a', 'b']}
        assert MahjongGame.get_legal_actions(state1) == ['a', 'b']
        assert state1['valid_act'] == ['a', 'b']
        
        # Branch: valid_act es otra cosa
        state2 = {'valid_act': ['fold'], 'action_cards': ['a', 'b']}
        assert MahjongGame.get_legal_actions(state2) == ['fold']

    def test_is_over_logic(self, game):
        game.judger = MagicMock()
        # Cubrir la asignación de self.winner
        game.judger.judge_game.return_value = (True, 99, None)
        assert game.is_over() is True
        assert game.winner == 99

    def test_getters_and_setters(self, game):
        # Cobertura de métodos simples
        assert game.get_num_actions() == 38
        assert game.get_num_players() == 4
        
        game.round = MagicMock()
        game.round.current_player = 2
        assert game.get_player_id() == 2

    def test_get_state(self, game):
        game.round = MagicMock()
        game.players = []
        game.get_state(1)
        game.round.get_state.assert_called_with([], 1)