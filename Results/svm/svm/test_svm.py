import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from Public_Proyects.svm.svm import SVM

@pytest.fixture
def sample_data():
    X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
    y = np.array([1, 1, -1, -1])
    return X, y

@pytest.fixture
def svm_model():
    return SVM(C=1.0, tol=1e-3, max_iter=10)

def test_svm_initialization():
    model = SVM(C=2.0, tol=1e-4, max_iter=50)
    assert model.C == 2.0
    assert model.tol == 1e-4
    assert model.max_iter == 50
    assert model.b == 0
    assert model.alpha is None

def test_svm_fit(svm_model, sample_data):
    X, y = sample_data
    svm_model.fit(X, y)
    assert svm_model.alpha is not None
    assert len(svm_model.alpha) == len(y)
    assert svm_model.K.shape == (len(y), len(y))

def test_clip():
    model = SVM(C=1.0)
    assert model.clip(1.5, 1.0, 0.0) == 1.0
    assert model.clip(-0.5, 1.0, 0.0) == 0.0
    assert model.clip(0.5, 1.0, 0.0) == 0.5

def test_find_bounds():
    model = SVM(C=1.0)
    model.alpha = np.array([0.5, 0.5])
    model.y = np.array([1, -1])
    
    # y[i] != y[j]
    L, H = model._find_bounds(0, 1)
    assert L == 0
    assert H == 1.0
    
    # y[i] == y[j]
    model.y = np.array([1, 1])
    L, H = model._find_bounds(0, 1)
    assert L == 0
    assert H == 1.0

def test_predict(svm_model, sample_data):
    X, y = sample_data
    svm_model.fit(X, y)
    predictions = svm_model._predict(X)
    assert isinstance(predictions, np.ndarray)
    assert len(predictions) == len(y)
    assert all(val in [-1.0, 1.0] for val in predictions)

def test_random_index(svm_model):
    svm_model.n_samples = 5
    idx = svm_model.random_index(0)
    assert idx != 0
    assert 0 <= idx < 5

def test_train_convergence(svm_model, sample_data):
    X, y = sample_data
    svm_model.fit(X, y)
    # Verificar que el entrenamiento se detiene o termina
    assert svm_model.alpha is not None
    assert hasattr(svm_model, 'sv_idx')

def test_predict_row_logic(svm_model, sample_data):
    X, y = sample_data
    svm_model.fit(X, y)
    # Mocking kernel output to ensure deterministic prediction test
    svm_model.kernel = MagicMock(return_value=np.array([1.0]))
    svm_model.sv_idx = np.array([0])
    svm_model.alpha = np.array([0.1, 0, 0, 0])
    svm_model.y = np.array([1, 0, 0, 0])
    
    res = svm_model._predict_row(np.array([1, 1]))
    assert isinstance(res, np.float64)

@patch('Public_Proyects.svm.svm.Linear')
def test_default_kernel(mock_linear):
    SVM()
    mock_linear.assert_called_once()