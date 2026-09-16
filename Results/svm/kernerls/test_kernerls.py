import pytest
import numpy as np
from Public_Proyects.svm.kernerls import Linear, Poly, RBF

def test_linear_kernel():
    kernel = Linear()
    x = np.array([[1, 2]])
    y = np.array([[3, 4]])
    expected = np.dot(x, y.T)
    assert np.allclose(kernel(x, y), expected)
    assert str(kernel) == "Linear kernel"

def test_poly_kernel():
    degree = 3
    kernel = Poly(degree=degree)
    x = np.array([[1, 2]])
    y = np.array([[3, 4]])
    expected = np.dot(x, y.T) ** degree
    assert np.allclose(kernel(x, y), expected)
    assert str(kernel) == "Poly kernel"

def test_rbf_kernel():
    gamma = 0.5
    kernel = RBF(gamma=gamma)
    x = np.array([[1, 2]])
    y = np.array([[3, 4]])
    
    # RBF formula: exp(-gamma * ||x-y||^2)
    dist_sq = np.sum((x - y) ** 2)
    expected = np.exp(-gamma * dist_sq)
    
    result = kernel(x, y)
    assert np.allclose(result, expected)
    assert result.shape == (1,)
    assert str(kernel) == "RBF kernel"

def test_rbf_multiple_inputs():
    kernel = RBF(gamma=0.1)
    x = np.array([[1, 0], [0, 1]])
    y = np.array([[1, 0]])
    result = kernel(x, y)
    assert result.shape == (2,)

def test_kernel_repr():
    assert repr(Linear()) == "Linear kernel"
    assert repr(Poly(2)) == "Poly kernel"
    assert repr(RBF(0.1)) == "RBF kernel"