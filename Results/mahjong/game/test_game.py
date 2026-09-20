import pytest
from unittest.mock import MagicMock, patch
from Public_Proyects.mahjong.game import MahjongGame

@pytest.fixture
def game():
    return MahjongGame(allow_step_back=True)

def test_init_game(game):
    with patch('Public_Proyects.mahjong.game.Dealer'), \
         patch('Public_Proyects.mahjong.game.Player'), \
         patch('Public_Proyects.mahjong.game.Judger'), \
         patch('Public_Proyects.mahjong.game.Round'):
        
        # Necesitamos mockear Round para que tenga el atributo current_player
        mock_round = MagicMock()
        mock_round.current_player = 0
        game.round = mock_round
        
        state, player_id = game.init_game()
        
        assert hasattr(game, 'dealer')
        assert hasattr(game, 'players')
        assert len(game.players) == 4
        assert hasattr(game, 'history')
        assert game.history == []

def test_step_logic(game):
    # Aseguramos que la historia exista
    game.history = []
    game.dealer = MagicMock()
    game.round = MagicMock()
    game.round.current_player = 0
    game.players = [MagicMock() for _ in range(4)]
    
    # Mockeamos get_state para que no intente ejecutar lógica real
    game.get_state = MagicMock(return_value={'valid_act': ['play']})
    
    state, player_id = game.step("some_action")
    
    assert len(game.history) == 1
    game.round.proceed_round.assert_called_with(game.players, "some_action")

def test_step_back(game):
    game.history = [("d", "p", "r")]
    success = game.step_back()
    
    assert success is True
    assert len(game.history) == 0

def test_step_back_empty_history(game):
    game.history = []
    success = game.step_back()
    assert success is False

def test_get_legal_actions_play():
    state = {'valid_act': ['play'], 'action_cards': ['1m', '2m']}
    actions = MahjongGame.get_legal_actions(state)
    assert actions == ['1m', '2m']

def test_get_legal_actions_other():
    state = {'valid_act': ['call']}
    actions = MahjongGame.get_legal_actions(state)
    assert actions == ['call']

def test_get_num_actions():
    assert MahjongGame.get_num_actions() == 38

def test_is_over(game):
    game.judger = MagicMock()
    # judge_game retorna (win, player, _)
    game.judger.judge_game.return_value = (True, 1, None)
    
    assert game.is_over() is True
    assert game.winner == 1

def test_get_player_id(game):
    game.round = MagicMock()
    game.round.current_player = 2
    assert game.get_player_id() == 2

def test_get_num_players(game):
    assert game.get_num_players() == 4