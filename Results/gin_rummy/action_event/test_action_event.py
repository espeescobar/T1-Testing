import pytest
from unittest.mock import MagicMock, patch
from Public_Proyects.gin_rummy.action_event import (
    ActionEvent, ScoreNorthPlayerAction, ScoreSouthPlayerAction,
    DrawCardAction, PickUpDiscardAction, DeclareDeadHandAction,
    GinAction, DiscardAction, KnockAction, knock_action_id,
    discard_action_id, score_player_0_action_id, score_player_1_action_id
)

@pytest.fixture
def mock_card():
    return MagicMock()

def test_action_event_init():
    action = ActionEvent(99)
    assert action.action_id == 99

def test_action_event_equality():
    action = ActionEvent(10)
    # Branch: isinstance is True, result is True
    assert action == ActionEvent(10)
    # Branch: isinstance is True, result is False
    assert action != ActionEvent(11)
    # Branch: isinstance is False
    assert action != "not an action"

def test_get_num_actions():
    assert ActionEvent.get_num_actions() == 110

@patch("Public_Proyects.gin_rummy.action_event.utils")
@pytest.mark.parametrize("action_id, expected_cls", [
    (score_player_0_action_id, ScoreNorthPlayerAction),
    (score_player_1_action_id, ScoreSouthPlayerAction),
    (2, DrawCardAction),
    (3, PickUpDiscardAction),
    (4, DeclareDeadHandAction),
    (5, GinAction),
])
def test_decode_action_basic(mock_utils, action_id, expected_cls):
    # Tests specific if/elif branches
    action = ActionEvent.decode_action(action_id)
    assert isinstance(action, expected_cls)

@patch("Public_Proyects.gin_rummy.action_event.utils")
def test_decode_action_ranges(mock_utils):
    mock_card = MagicMock()
    mock_utils.get_card.return_value = mock_card
    
    # Coverage: DiscardAction branch range
    action_d = ActionEvent.decode_action(discard_action_id + 5)
    assert isinstance(action_d, DiscardAction)
    
    # Coverage: KnockAction branch range
    action_k = ActionEvent.decode_action(knock_action_id + 5)
    assert isinstance(action_k, KnockAction)

def test_decode_action_else_branch():
    # Coverage: Final else branch raising exception
    with pytest.raises(Exception) as exc:
        ActionEvent.decode_action(1000)
    assert "unknown action_id=1000" in str(exc.value)

@patch("Public_Proyects.gin_rummy.action_event.utils")
def test_subclasses_init_and_str(mock_utils, mock_card):
    mock_utils.get_card_id.return_value = 1
    
    # Test specific subclasses and their __str__ methods
    objs = [
        (ScoreNorthPlayerAction(), "score N"),
        (ScoreSouthPlayerAction(), "score S"),
        (DrawCardAction(), "draw_card"),
        (PickUpDiscardAction(), "pick_up_discard"),
        (DeclareDeadHandAction(), "declare_dead_hand"),
        (GinAction(), "gin"),
        (DiscardAction(mock_card), "discard "),
        (KnockAction(mock_card), "knock ")
    ]
    
    for obj, expected_str_part in objs:
        assert str(obj).startswith(expected_str_part)
        
    # Verify utility calls in subclass constructors
    mock_utils.get_card_id.assert_called()

def test_eq_branch_coverage_supplementary():
    action = ActionEvent(1)
    # Ensure all paths in __eq__ are covered
    assert (action == None) is False