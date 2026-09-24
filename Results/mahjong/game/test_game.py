import pytest
from unittest.mock import MagicMock, patch
from Public_Proyects.mahjong.game import MahjongGame

@pytest.fixture
def game():
    return MahjongGame(allow_step_back=True)

def test_init_game(game):
    # Necesitamos mockear el retorno de get_state dentro de Round porque init_game lo llama
    mock_round_instance = MagicMock()
    mock_round_instance.current_player = 0
    mock_round_instance.get_state.return_value = {"state": "data"}
    
    with patch('Public_Proyects.mahjong.game.Dealer'), \
         patch('Public_Proyects.mahjong.game.Player'), \
         patch('Public_Proyects.mahjong.game.Judger'), \
         patch('Public_Proyects.mahjong.game.Round', return_value=mock_round_instance):
        
        state, player_id = game.init_game()
        
        assert hasattr(game, 'dealer')
        assert hasattr(game, 'players')
        assert hasattr(game, 'history')
        assert len(game.players) == 4
        assert state == {"state": "data"}
        assert isinstance(state, dict)

def test_step_logic(game):
    # Inicializar estado base
    game.round = MagicMock()
    game.round.current_player = 0
    game.history = []
    game.dealer = MagicMock()
    game.players = []
    
    # Mockear get_state para que devuelva un dict y evite el error de isinstance
    game.get_state = MagicMock(return_value={'valid_act': ['play']})
    
    initial_history_len = len(game.history)
    state, player_id = game.step('action_test')
    
    assert len(game.history) == initial_history_len + 1
    game.round.proceed_round.assert_called_once()
    assert state == {'valid_act': ['play']}

def test_step_back_functionality(game):
    game.history = []
    mock_dealer = MagicMock()
    mock_players = MagicMock()
    mock_round = MagicMock()
    game.history.append((mock_dealer, mock_players, mock_round))
    
    success = game.step_back()
    
    assert success is True
    assert game.dealer == mock_dealer
    assert game.players == mock_players
    assert game.round == mock_round
    assert len(game.history) == 0

def test_step_back_empty_history(game):
    game.history = []  # Aseguramos que existe y está vacía
    assert game.step_back() is False

def test_get_legal_actions_play_case():
    state = {'valid_act': ['play'], 'action_cards': ['1m', '2m']}
    actions = MahjongGame.get_legal_actions(state)
    assert actions == ['1m', '2m']
    assert state['valid_act'] == ['1m', '2m']

def test_get_legal_actions_other_case():
    state = {'valid_act': ['call']}
    actions = MahjongGame.get_legal_actions(state)
    assert actions == ['call']

def test_get_num_actions():
    assert MahjongGame.get_num_actions() == 38

def test_get_player_id(game):
    game.round = MagicMock()
    game.round.current_player = 2
    assert game.get_player_id() == 2

def test_is_over(game):
    game.judger = MagicMock()
    game.judger.judge_game.return_value = (True, 1, None)
    
    assert game.is_over() is True
    assert game.winner == 1

def test_get_state(game):
    game.round = MagicMock()
    game.players = []
    expected_state = {'test': 'data'}
    game.round.get_state.return_value = expected_state
    
    assert game.get_state(0) == expected_state
    game.round.get_state.assert_called_with(game.players, 0)