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
    # Caso base: etiquetas iguales
    p = np.array([1, 1, 1, 1])
    assert f_entropy(p) == 0.0
    
    # Caso: distribución uniforme
    p = np.array([0, 1])
    # log(2) aprox 0.693
    assert f_entropy(p) > 0.0

def test_information_gain():
    y = np.array([0, 0, 1, 1])
    splits = [np.array([0, 0]), np.array([1, 1])]
    gain = information_gain(y, splits)
    assert gain > 0.0

def test_mse_criterion():
    y = np.array([1.0, 2.0, 3.0, 4.0])
    splits = [np.array([1.0, 2.0]), np.array([3.0, 4.0])]
    result = mse_criterion(y, splits)
    assert isinstance(result, float)
    assert result < 0 # El criterio está negado en la implementación

def test_xgb_criterion():
    mock_loss = MagicMock()
    mock_loss.gain.side_effect = [10.0, 10.0, 20.0]  # left, right, initial
    
    y = {"actual": np.array([1]), "y_pred": np.array([0.5])}
    left = {"actual": np.array([1]), "y_pred": np.array([0.2])}
    right = {"actual": np.array([0]), "y_pred": np.array([0.8])}
    
    gain = xgb_criterion(y, left, right, mock_loss)
    # left(10) + right(10) - initial(20) = 0
    assert gain == 0.0

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
    X = np.array([[1], [5]])
    target = {"t": np.array([10, 20])}
    
    # Test con return_X=True
    l_X, r_X, left, right = split_dataset(X, target, 0, 3, return_X=True)
    assert l_X.shape == (1, 1)
    assert left["t"] == 10
    
    # Test con return_X=False
    left_only, right_only = split_dataset(X, target, 0, 3, return_X=False)
    assert "t" in left_only
    assert "t" in right_only