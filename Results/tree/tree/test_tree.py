import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from Public_Proyects.tree.tree import Tree

@pytest.fixture
def sample_data():
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
    y = np.array([0, 0, 1, 1, 1])
    return X, y

def test_tree_initialization():
    tree = Tree(regression=True, criterion=sum, n_classes=2)
    assert tree.regression is True
    assert tree.criterion == sum
    assert tree.is_terminal is True

def test_find_splits():
    tree = Tree()
    X = np.array([1, 2, 3, 4])
    splits = tree._find_splits(X)
    assert 1.5 in splits
    assert 2.5 in splits
    assert 3.5 in splits
    assert len(splits) == 3

def test_is_terminal():
    tree = Tree()
    assert tree.is_terminal is True
    tree.left_child = Tree()
    assert tree.is_terminal is True
    tree.right_child = Tree()
    assert tree.is_terminal is False

def test_calculate_leaf_value_regression(sample_data):
    _, y = sample_data
    tree = Tree(regression=True)
    targets = {"y": y}
    tree._calculate_leaf_value(targets)
    assert tree.outcome == np.mean(y)

def test_calculate_leaf_value_classification(sample_data):
    _, y = sample_data
    tree = Tree(regression=False, n_classes=2)
    targets = {"y": y}
    tree._calculate_leaf_value(targets)
    # y = [0, 0, 1, 1, 1], prob of class 1 is 3/5 = 0.6
    expected = np.array([2/5, 3/5])
    np.testing.assert_array_almost_equal(tree.outcome, expected)

def test_predict_row_terminal():
    tree = Tree()
    tree.outcome = 0.5
    assert tree.predict_row(np.array([1])) == 0.5

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
    
    assert tree.predict_row(np.array([4.0])) == 1.0
    assert tree.predict_row(np.array([6.0])) == 2.0

def test_train_creates_nodes(sample_data):
    X, y = sample_data
    tree = Tree(regression=False, criterion=lambda y, splits: 0.1)
    tree.train(X, y, max_depth=2, min_samples_split=2)
    
    assert tree.column_index is not None
    assert tree.left_child is not None
    assert tree.right_child is not None

def test_train_with_loss_gradient_boosting():
    X = np.array([[1], [2]])
    y = np.array([0, 1])
    target = {"actual": y, "y_pred": np.array([0.5, 0.5])}
    
    mock_loss = MagicMock()
    mock_loss.approximate.return_value = 0.99
    
    tree = Tree(regression=True)
    tree.loss = mock_loss
    tree._calculate_leaf_value(target)
    
    assert tree.outcome == 0.99
    mock_loss.approximate.assert_called_once()