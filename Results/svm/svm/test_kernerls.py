import pytest
import numpy as np
from Public_Proyects.svm.kernerls import Linear, Poly, RBF

def test_linear_kernel():
    kernel = Linear()
    x = np.array([[1, 2]])
    y = np.array([[3, 4]])
    expected = np.dot(x, y.T)
    assert np.allclose(kernel(x, y), expected)
    assert repr(kernel) == "Linear kernel"

def test_poly_kernel():
    degree = 3
    kernel = Poly(degree=degree)
    x = np.array([[1, 2]])
    y = np.array([[3, 4]])
    expected = np.dot(x, y.T) ** degree
    assert np.allclose(kernel(x, y), expected)
    assert repr(kernel) == "Poly kernel"

def test_rbf_kernel():
    gamma = 0.5
    kernel = RBF(gamma=gamma)
    x = np.array([[1, 0]])
    y = np.array([[0, 1]])
    # dist.cdist squared distance between [1,0] and [0,1] is (1-0)^2 + (0-1)^2 = 2
    # RBF = exp(-0.5 * 2) = exp(-1)
    expected = np.exp(-gamma * 2.0)
    result = kernel(x, y)
    assert np.allclose(result, expected)
    assert repr(kernel) == "RBF kernel"

def test_rbf_input_shapes():
    kernel = RBF()
    x = np.array([1, 2])
    y = np.array([3, 4])
    result = kernel(x, y)
    assert isinstance(result, np.ndarray)
    assert result.ndim == 1

def test_linear_matrix_input():
    kernel = Linear()
    x = np.random.rand(5, 3)
    y = np.random.rand(2, 3)
    result = kernel(x, y)
    assert result.shape == (5, 2)