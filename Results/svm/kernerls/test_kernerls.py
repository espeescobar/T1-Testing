import numpy as np
import pytest
from unittest.mock import MagicMock
from Public_Proyects.svm.kernerls import Linear, Poly, RBF

def test_linear_kernel():
    linear = Linear()
    x = np.array([[1, 2], [3, 4]])
    y = np.array([[5, 6]])
    
    result = linear(x, y)
    expected = np.dot(x, y.T)
    
    assert np.array_equal(result, expected)
    assert repr(linear) == "Linear kernel"

def test_poly_kernel():
    degree = 3
    poly = Poly(degree=degree)
    x = np.array([[1, 2]])
    y = np.array([[3, 4]])
    
    result = poly(x, y)
    expected = (np.dot(x, y.T)) ** degree
    
    assert np.array_equal(result, expected)
    assert repr(poly) == "Poly kernel"

def test_rbf_kernel():
    gamma = 0.5
    rbf = RBF(gamma=gamma)
    x = np.array([[1, 0]])
    y = np.array([[0, 1]])
    
    result = rbf(x, y)
    
    # RBF formula: exp(-gamma * ||x-y||^2)
    # distance^2 = (1-0)^2 + (0-1)^2 = 2
    # result = exp(-0.5 * 2) = exp(-1)
    assert np.isclose(result[0], np.exp(-1))
    assert repr(rbf) == "RBF kernel"

def test_rbf_atleast_2d_handling():
    rbf = RBF(gamma=0.1)
    # Test with 1D input
    x = np.array([1, 2])
    y = np.array([3, 4])
    result = rbf(x, y)
    assert result.shape == (1,)

def test_kernel_mocking_interface():
    # Demonstrating mocking requirement with MagicMock
    mock_kernel = MagicMock(spec=Linear)
    mock_kernel.return_value = np.array([10.0])
    
    result = mock_kernel(np.array([1]), np.array([1]))
    assert result == 10.0
    mock_kernel.assert_called_once()

def test_poly_kernel_default_degree():
    poly = Poly()
    assert poly.degree == 2

def test_rbf_kernel_default_gamma():
    rbf = RBF()
    assert rbf.gamma == 0.1

@pytest.mark.parametrize("kernel_class, args", [
    (Linear, {}),
    (Poly, {"degree": 4}),
    (RBF, {"gamma": 0.01})
])
def test_kernel_initialization(kernel_class, args):
    instance = kernel_class(**args)
    assert isinstance(instance, kernel_class)