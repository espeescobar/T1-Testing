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
def svm_instance():
    return SVM(C=1.0, tol=1e-3, max_iter=10)

def test_svm_initialization():
    svm = SVM(C=0.5, tol=0.01, max_iter=50)
    assert svm.C == 0.5
    assert svm.tol == 0.01
    assert svm.max_iter == 50
    assert svm.b == 0

def test_fit_sets_attributes(svm_instance, sample_data):
    X, y = sample_data
    svm_instance.fit(X, y)
    assert svm_instance.K.shape == (4, 4)
    assert svm_instance.alpha is not None
    assert len(svm_instance.alpha) == 4

def test_clip():
    svm = SVM()
    assert svm.clip(1.5, 1.0, 0.0) == 1.0
    assert svm.clip(-0.5, 1.0, 0.0) == 0.0
    assert svm.clip(0.5, 1.0, 0.0) == 0.5

def test_find_bounds_different_labels():
    svm = SVM(C=1.0)
    # Usamos valores exactos representables en binario para evitar errores de precisión de punto flotante
    svm.alpha = np.array([0.25, 0.75])
    svm.y = np.array([1, -1])
    L, H = svm._find_bounds(0, 1)
    # L = max(0, 0.75 - 0.25) = 0.5
    # H = min(1, 1 - 0.25 + 0.75) = 1.5 -> min(1, 1.5) = 1
    assert L == pytest.approx(0.5)
    assert H == pytest.approx(1.0)

def test_find_bounds_same_labels():
    svm = SVM(C=1.0)
    svm.alpha = np.array([0.2, 0.3])
    svm.y = np.array([1, 1])
    L, H = svm._find_bounds(0, 1)
    # L = max(0, 0.2 + 0.3 - 1) = 0
    # H = min(1, 0.2 + 0.3) = 0.5
    assert L == pytest.approx(0.0)
    assert H == pytest.approx(0.5)

def test_predict(svm_instance, sample_data):
    X, y = sample_data
    svm_instance.fit(X, y)
    predictions = svm_instance._predict(X)
    assert predictions.shape == (4,)
    assert all(p in [-1.0, 1.0, 0.0] for p in predictions)

def test_random_index(svm_instance):
    svm_instance.n_samples = 5
    idx = svm_instance.random_index(0)
    assert idx != 0
    assert 0 <= idx < 5

def test_train_convergence(svm_instance, sample_data):
    X, y = sample_data
    # Usamos patch para asegurar que el entrenamiento no dependa de la aleatoriedad excesiva del random_index
    with patch.object(svm_instance, 'random_index', return_value=1):
        svm_instance.fit(X, y)
        assert svm_instance.alpha is not None

def test_predict_row(svm_instance, sample_data):
    X, y = sample_data
    svm_instance.fit(X, y)
    svm_instance.kernel = MagicMock(return_value=np.array([1.0]))
    svm_instance.sv_idx = [0]
    result = svm_instance._predict_row(X[0])
    assert isinstance(result, (float, np.float64, np.ndarray))