import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from Public_Proyects.tree.tree import Tree

@pytest.fixture
def sample_data():
    X = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0]])
    y = np.array([0, 0, 1, 1])
    target = {"y": y}
    return X, target

def test_tree_initialization():
    tree = Tree(regression=True, n_classes=2)
    assert tree.regression is True
    assert tree.n_classes == 2
    assert tree.is_terminal is True

def test_find_splits():
    tree = Tree()
    X = np.array([1.0, 2.0, 3.0])
    splits = tree._find_splits(X)
    assert 1.5 in splits
    assert 2.5 in splits
    assert len(splits) == 2

def test_is_terminal_property():
    tree = Tree()
    assert tree.is_terminal is True
    tree.left_child = Tree()
    tree.right_child = Tree()
    assert tree.is_terminal is False

def test_calculate_leaf_value_regression():
    tree = Tree(regression=True)
    targets = {"y": np.array([1.0, 2.0, 3.0])}
    tree._calculate_leaf_value(targets)
    assert tree.outcome == 2.0

def test_calculate_leaf_value_classification():
    tree = Tree(regression=False, n_classes=2)
    targets = {"y": np.array([0, 1, 1])}
    tree._calculate_leaf_value(targets)
    expected = np.array([1/3, 2/3])
    np.testing.assert_array_almost_equal(tree.outcome, expected)

def test_predict_row_terminal():
    tree = Tree()
    tree.outcome = 0.5
    assert tree.predict_row([1, 2]) == 0.5

def test_predict_row_recursive():
    tree = Tree()
    tree.column_index = 0
    tree.threshold = 5.0
    
    left = Tree()
    left.outcome = 1.0
    
    right = Tree()
    right.outcome = 2.0
    
    tree.left_child = left
    tree.right_child = right
    
    assert tree.predict_row([2.0, 0.0]) == 1.0
    assert tree.predict_row([6.0, 0.0]) == 2.0

@patch("Public_Proyects.tree.tree.split")
def test_find_best_split(mock_split, sample_data):
    X, target = sample_data
    # Mocking the criterion function to avoid TypeError
    mock_criterion = MagicMock(return_value=0.5)
    tree = Tree(criterion=mock_criterion)
    
    col, val, gain = tree._find_best_split(X, target, n_features=1)
    
    assert col is not None
    assert val is not None
    assert gain == 0.5
    assert mock_criterion.called

def test_train_recursion_limit(sample_data):
    X, target = sample_data
    # Use a dummy criterion to avoid TypeError
    tree = Tree(regression=False, criterion=lambda y, splits: 0.1)
    tree.train(X, target, min_samples_split=10, max_depth=1)
    assert tree.is_terminal is True
    assert tree.outcome is not None

def test_predict_integration(sample_data):
    X, target = sample_data
    # Providing a dummy criterion for the random forest logic
    # Gain must be > 0 for regression if we follow the code constraints
    tree = Tree(regression=True, criterion=lambda y, splits: 1.0)
    tree.train(X, target, min_samples_split=1, max_depth=2)
    predictions = tree.predict(X)
    assert isinstance(predictions, np.ndarray)
    assert len(predictions) == X.shape[0]

def test_gradient_boosting_loss_path():
    tree = Tree(regression=True)
    mock_loss = MagicMock()
    mock_loss.approximate.return_value = 0.99
    tree.loss = mock_loss
    
    targets = {"actual": np.array([1]), "y_pred": np.array([0])}
    tree._calculate_leaf_value(targets)
    
    mock_loss.approximate.assert_called_once()
    assert tree.outcome == 0.99