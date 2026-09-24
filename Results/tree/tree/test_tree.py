import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from Public_Proyects.tree.tree import Tree

@pytest.fixture
def sample_data():
    X = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0]])
    y = np.array([0, 0, 1, 1])
    return X, {"y": y, "actual": y, "y_pred": y}

def test_tree_initialization():
    tree = Tree(regression=True, n_classes=2)
    assert tree.regression is True
    assert tree.n_classes == 2
    assert tree.is_terminal is True

def test_find_splits():
    tree = Tree()
    X = np.array([1.0, 3.0, 5.0])
    splits = tree._find_splits(X)
    assert 2.0 in splits
    assert 4.0 in splits
    assert len(splits) == 2

def test_calculate_leaf_value_regression():
    tree = Tree(regression=True)
    targets = {"y": np.array([1.0, 2.0, 3.0])}
    tree._calculate_leaf_value(targets)
    assert tree.outcome == 2.0

def test_predict_row_terminal():
    tree = Tree()
    tree.outcome = 0.5
    assert tree.predict_row([1, 2]) == 0.5

@patch("Public_Proyects.tree.tree.xgb_criterion")
@patch("Public_Proyects.tree.tree.split_dataset")
def test_train_gradient_boosting(mock_split_dataset, mock_xgb, sample_data):
    """
    Se corrige el manejo de side_effect para split_dataset.
    El error original ocurría porque al llamar a split_dataset con return_X=False,
    se esperaba que el mock devolviera 2 elementos, pero el mock estaba configurado 
    para devolver siempre 4, causando el ValueError.
    """
    X, target = sample_data
    mock_loss = MagicMock()
    mock_loss.approximate.return_value = 0.5
    
    tree = Tree(regression=True)
    tree.loss = mock_loss
    mock_xgb.return_value = 0.5
    
    # Definimos una función que decide qué retornar basado en los argumentos recibidos
    def side_effect_func(X_in, target_in, col, val, return_X=True):
        if not return_X:
            return (np.array([1]), np.array([3]))
        else:
            return (np.array([[1]]), np.array([[3]]), {"y": np.array([0])}, {"y": np.array([1])})
    
    mock_split_dataset.side_effect = side_effect_func
    
    tree.train(X, target, max_depth=1, min_samples_split=0)
    
    assert tree.loss == mock_loss
    assert tree.impurity == 0.5

def test_predict_flow():
    tree = Tree()
    tree.column_index = 0
    tree.threshold = 5.0
    
    left = Tree()
    left.outcome = 0.0
    right = Tree()
    right.outcome = 1.0
    
    tree.left_child = left
    tree.right_child = right
    
    X = np.array([[2.0, 0.0], [8.0, 0.0]])
    predictions = tree.predict(X)
    
    np.testing.assert_array_equal(predictions, np.array([0.0, 1.0]))

def test_is_terminal_property():
    tree = Tree()
    assert tree.is_terminal is True
    tree.left_child = MagicMock()
    tree.right_child = MagicMock()
    assert tree.is_terminal is False

def test_calculate_leaf_value_classification():
    tree = Tree(regression=False, n_classes=2)
    targets = {"y": np.array([0, 1, 0])}
    tree._calculate_leaf_value(targets)
    np.testing.assert_array_almost_equal(tree.outcome, np.array([2/3, 1/3]))