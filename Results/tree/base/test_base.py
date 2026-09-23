import pytest
import numpy as np
from unittest.mock import MagicMock
from Public_Proyects.tree.base import (
    f_entropy,
    information_gain,
    mse_criterion,
    xgb_criterion,
    get_split_mask,
    split,
    split_dataset
)

def test_f_entropy():
    # Caso para distribución uniforme
    p = np.array([0, 1, 0, 1])
    entropy = f_entropy(p)
    assert isinstance(entropy, float)
    assert entropy >= 0

    # Caso con un solo elemento (debe ser 0)
    p_single = np.array([0, 0, 0])
    assert f_entropy(p_single) == 0.0

def test_information_gain():
    y = np.array([0, 1, 0, 1])
    split1 = np.array([0, 0])
    split2 = np.array([1, 1])
    gain = information_gain(y, [split1, split2])
    assert gain > 0

def test_mse_criterion():
    y = np.array([1, 2, 3, 4, 5])
    split1 = np.array([1, 2])
    split2 = np.array([3, 4, 5])
    mse = mse_criterion(y, [split1, split2])
    assert isinstance(mse, float)

def test_xgb_criterion():
    mock_loss = MagicMock()
    mock_loss.gain.side_effect = [10.0, 10.0, 5.0]  # left, right, initial
    
    y = {"actual": np.array([1]), "y_pred": np.array([0.5])}
    left = {"actual": np.array([1]), "y_pred": np.array([0.5])}
    right = {"actual": np.array([0]), "y_pred": np.array([0.5])}
    
    gain = xgb_criterion(y, left, right, mock_loss)
    assert gain == 15.0
    assert mock_loss.gain.call_count == 3

def test_get_split_mask():
    X = np.array([[1, 2], [3, 4], [5, 6]])
    column = 0
    value = 3
    left, right = get_split_mask(X, column, value)
    
    assert np.array_equal(left, [True, False, False])
    assert np.array_equal(right, [False, True, True])

def test_split():
    X = np.array([1, 2, 3, 4, 5])
    y = np.array([10, 20, 30, 40, 50])
    value = 3
    left_y, right_y = split(X, y, value)
    
    assert np.array_equal(left_y, [10, 20])
    assert np.array_equal(right_y, [30, 40, 50])

def test_split_dataset_with_X():
    X = np.array([[1], [2], [3]])
    target = {"y": np.array([10, 20, 30])}
    column = 0
    value = 2
    
    left_X, right_X, left_t, right_t = split_dataset(X, target, column, value, return_X=True)
    
    assert len(left_X) == 1
    assert len(right_X) == 2
    assert np.array_equal(left_t["y"], [10])
    assert np.array_equal(right_t["y"], [20, 30])

def test_split_dataset_without_X():
    X = np.array([[1], [2], [3]])
    target = {"y": np.array([10, 20, 30])}
    column = 0
    value = 2
    
    left_t, right_t = split_dataset(X, target, column, value, return_X=False)
    
    assert "y" in left_t
    assert "y" in right_t
    assert np.array_equal(left_t["y"], [10])