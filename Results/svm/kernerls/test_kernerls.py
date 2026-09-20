import numpy as np
import pytest
from unittest.mock import MagicMock
from Public_Proyects.svm.kernerls import Linear, Poly, RBF

def test_linear_kernel():
    linear = Linear()
    x = np.array([[1, 2], [3, 4]])
    y = np.array([[5, 6], [7, 8]])
    
    expected = np.dot(x, y.T)
    result = linear(x, y)
    
    assert np.array_equal(result, expected)
    assert str(linear) == "Linear kernel"

def test_poly_kernel():
    degree = 3
    poly = Poly(degree=degree)
    x = np.array([[1, 2]])
    y = np.array([[3, 4]])
    
    expected = np.dot(x, y.T) ** degree
    result = poly(x, y)
    
    assert np.array_equal(result, expected)
    assert poly.degree == degree
    assert str(poly) == "Poly kernel"

def test_rbf_kernel_basic():
    gamma = 0.5
    rbf = RBF(gamma=gamma)
    x = np.array([[1, 2]])
    y = np.array([[1, 2]])
    
    result = rbf(x, y)
    
    # Distance is 0, exp(-0) = 1
    assert np.isclose(result[0], 1.0)
    assert rbf.gamma == gamma
    assert str(rbf) == "RBF kernel"

def test_rbf_kernel_dimensions():
    rbf = RBF(gamma=0.1)
    x = np.array([1, 2]) # 1D array should be handled by atleast_2d
    y = np.array([3, 4])
    
    result = rbf(x, y)
    assert isinstance(result, np.ndarray)
    assert result.ndim == 1

def test_rbf_with_mock():
    # Example usage of MagicMock as requested
    mock_dist = MagicMock()
    # Simulating dist.cdist behavior
    mock_dist.return_value = np.array([[2.0]])
    
    import Public_Proyects.svm.kernerls as kernels
    kernels.dist.cdist = mock_dist
    
    rbf = RBF(gamma=0.1)
    x = np.array([[1, 2]])
    y = np.array([[3, 4]])
    
    rbf(x, y)
    
    mock_dist.assert_called_once()
    assert mock_dist.call_args[0][0].shape == (1, 2)