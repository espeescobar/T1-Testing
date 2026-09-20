import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from Public_Proyects.svm.svm import SVM

@pytest.fixture
def sample_data():
    X = np.array([[1, 2], [2, 3], [3, 3], [2, 1]])
    y = np.array([1, 1, -1, -1])
    return X, y

@pytest.fixture
def svm_model():
    return SVM(C=1.0, max_iter=10)

def test_svm_initialization():
    kernel = MagicMock()
    svm = SVM(C=0.5, kernel=kernel, tol=1e-4, max_iter=50)
    assert svm.C == 0.5
    assert svm.kernel == kernel
    assert svm.tol == 1e-4
    assert svm.max_iter == 50
    assert svm.b == 0

def test_fit_sets_attributes(svm_model, sample_data):
    X, y = sample_data
    svm_model.fit(X, y)
    assert svm_model.alpha is not None
    assert svm_model.K.shape == (4, 4)
    assert len(svm_model.alpha) == 4

def test_clip():
    svm = SVM()
    assert svm.clip(0.5, 1.0, 0.0) == 0.5
    assert svm.clip(1.5, 1.0, 0.0) == 1.0
    assert svm.clip(-0.5, 1.0, 0.0) == 0.0

def test_find_bounds():
    svm = SVM(C=1.0)
    svm.y = np.array([1, -1])
    svm.alpha = np.array([0.2, 0.2])
    
    # Different labels
    L, H = svm._find_bounds(0, 1)
    assert L == 0
    assert H == 1.0
    
    # Same labels
    svm.y = np.array([1, 1])
    L, H = svm._find_bounds(0, 1)
    assert L == 0
    assert H == 0.4

def test_predict(svm_model, sample_data):
    X, y = sample_data
    svm_model.fit(X, y)
    predictions = svm_model._predict(X)
    assert isinstance(predictions, np.ndarray)
    assert len(predictions) == len(y)
    assert set(np.unique(predictions)).issubset({-1.0, 0.0, 1.0})

def test_random_index():
    svm = SVM()
    svm.n_samples = 5
    with patch('numpy.random.randint', return_value=1) as mock_rand:
        # If z=0, random index should be 1
        idx = svm.random_index(0)
        assert idx == 1
        mock_rand.assert_called_with(0, 5)

def test_error_calculation(svm_model, sample_data):
    X, y = sample_data
    svm_model.fit(X, y)
    # Ensure error returns a float
    error = svm_model._error(0)
    assert isinstance(error, (float, np.float64))

def test_train_convergence(svm_model, sample_data):
    X, y = sample_data
    # Force max_iter to be small to test loop
    svm_model.max_iter = 1
    svm_model.fit(X, y)
    assert svm_model.alpha is not None