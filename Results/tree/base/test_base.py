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
    # Test with balanced distribution
    p = np.array([0, 0, 1, 1])
    entropy = f_entropy(p)
    assert entropy >= 0.693  # ln(2)

    # Test with single class
    p_single = np.array([0, 0, 0])
    assert f_entropy(p_single) == 0.0

def test_information_gain():
    y = np.array([0, 0, 1, 1])
    splits = [np.array([0, 0]), np.array([1, 1])]
    gain = information_gain(y, splits)
    assert gain > 0

def test_mse_criterion():
    y = np.array([1.0, 2.0, 3.0])
    splits = [np.array([1.0]), np.array([2.0, 3.0])]
    criterion = mse_criterion(y, splits)
    assert criterion <= 0

def test_xgb_criterion():
    mock_loss = MagicMock()
    mock_loss.gain.side_effect = [10.0, 20.0, 5.0]  # left, right, initial
    
    y = {"actual": np.array([1]), "y_pred": np.array([0])}
    left = {"actual": np.array([1]), "y_pred": np.array([0])}
    right = {"actual": np.array([1]), "y_pred": np.array([0])}
    
    gain = xgb_criterion(y, left, right, mock_loss)
    # 10 + 20 - 5 = 25
    assert gain == 25.0

def test_get_split_mask():
    X = np.array([[1, 2], [3, 4], [5, 6]])
    left, right = get_split_mask(X, 0, 3)
    assert np.array_equal(left, [True, False, False])
    assert np.array_equal(right, [False, True, True])

def test_split():
    X = np.array([1, 2, 3, 4, 5])
    y = np.array([10, 20, 30, 40, 50])
    left, right = split(X, y, 3)
    assert np.array_equal(left, [10, 20])
    assert np.array_equal(right, [30, 40, 50])

def test_split_dataset():
    X = np.array([[1], [2], [3]])
    target = {"y": np.array([10, 20, 30])}
    
    left_X, right_X, left, right = split_dataset(X, target, 0, 2, return_X=True)
    
    assert left_X.shape == (1, 1)
    assert right_X.shape == (2, 1)
    assert np.array_equal(left["y"], [10])
    assert np.array_equal(right["y"], [20, 30])

def test_split_dataset_no_X():
    X = np.array([[1], [2]])
    target = {"y": np.array([10, 20])}
    
    left, right = split_dataset(X, target, 0, 2, return_X=False)
    assert "y" in left
    assert "y" in right
    assert left["y"].size == 1