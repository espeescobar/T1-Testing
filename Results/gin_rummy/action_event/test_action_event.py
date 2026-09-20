import pytest
from unittest.mock import MagicMock, patch
from Public_Proyects.gin_rummy.action_event import (
    ActionEvent, ScoreNorthPlayerAction, ScoreSouthPlayerAction,
    DrawCardAction, PickUpDiscardAction, DeclareDeadHandAction,
    GinAction, DiscardAction, KnockAction, knock_action_id
)

@pytest.fixture
def mock_card():
    card = MagicMock()
    return card

@patch('Public_Proyects.gin_rummy.action_event.utils')
def test_action_event_equality(mock_utils):
    action1 = ActionEvent(10)
    action2 = ActionEvent(10)
    action3 = ActionEvent(11)
    assert action1 == action2
    assert action1 != action3
    assert action1 != "not an action"

def test_get_num_actions():
    # El código fuente define: knock_action_id = 58
    # get_num_actions retorna knock_action_id + 52 = 58 + 52 = 110
    assert ActionEvent.get_num_actions() == 110

@patch('Public_Proyects.gin_rummy.action_event.utils')
def test_decode_action_simple(mock_utils):
    assert isinstance(ActionEvent.decode_action(0), ScoreNorthPlayerAction)
    assert isinstance(ActionEvent.decode_action(1), ScoreSouthPlayerAction)
    assert isinstance(ActionEvent.decode_action(2), DrawCardAction)
    assert isinstance(ActionEvent.decode_action(3), PickUpDiscardAction)
    assert isinstance(ActionEvent.decode_action(4), DeclareDeadHandAction)
    assert isinstance(ActionEvent.decode_action(5), GinAction)

@patch('Public_Proyects.gin_rummy.action_event.utils')
def test_decode_action_discard(mock_utils):
    mock_utils.get_card.return_value = "CardObject"
    action = ActionEvent.decode_action(6)
    assert isinstance(action, DiscardAction)
    assert action.card == "CardObject"

@patch('Public_Proyects.gin_rummy.action_event.utils')
def test_decode_action_knock(mock_utils):
    mock_utils.get_card.return_value = "CardObject"
    action = ActionEvent.decode_action(58)
    assert isinstance(action, KnockAction)
    assert action.card == "CardObject"

def test_decode_action_invalid():
    with pytest.raises(Exception):
        ActionEvent.decode_action(999)

def test_action_string_representations():
    assert str(ScoreNorthPlayerAction()) == "score N"
    assert str(ScoreSouthPlayerAction()) == "score S"
    assert str(DrawCardAction()) == "draw_card"
    assert str(PickUpDiscardAction()) == "pick_up_discard"
    assert str(DeclareDeadHandAction()) == "declare_dead_hand"
    assert str(GinAction()) == "gin"

@patch('Public_Proyects.gin_rummy.action_event.utils')
def test_discard_action_init(mock_utils, mock_card):
    mock_utils.get_card_id.return_value = 5
    action = DiscardAction(mock_card)
    assert action.action_id == 6 + 5
    assert action.card == mock_card

@patch('Public_Proyects.gin_rummy.action_event.utils')
def test_knock_action_init(mock_utils, mock_card):
    mock_utils.get_card_id.return_value = 10
    action = KnockAction(mock_card)
    assert action.action_id == knock_action_id + 10
    assert action.card == mock_card