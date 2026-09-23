import pytest
import numpy as np
from unittest.mock import patch
from Public_Proyects.svm.base import BaseEstimator

class ConcreteEstimator(BaseEstimator):
    def _predict(self, X=None):
        return np.zeros(len(X))

class NoYRequiredEstimator(BaseEstimator):
    y_required = False
    def _predict(self, X=None):
        return np.ones(len(X))

class NoFitRequiredEstimator(BaseEstimator):
    fit_required = False
    def _predict(self, X=None):
        return np.array([2.0])

# --- Pruebas de cobertura de ramas (setup_input) ---

def test_setup_input_1d_array():
    estimator = BaseEstimator()
    X = np.array([1, 2, 3])
    y = np.array([0, 0, 0])
    estimator._setup_input(X, y)
    assert estimator.n_samples == 1
    assert estimator.n_features == (3,)

def test_setup_input_multidimensional_array():
    estimator = BaseEstimator()
    X = np.array([[1, 2], [3, 4]])
    y = np.array([0, 1])
    estimator._setup_input(X, y)
    assert estimator.n_samples == 2
    assert estimator.n_features == 2

def test_setup_input_y_conversion():
    estimator = BaseEstimator()
    X = np.array([[1]])
    y = [1]
    estimator._setup_input(X, y)
    assert isinstance(estimator.y, np.ndarray)

# --- Pruebas de cobertura de ramas (predict) ---

def test_predict_fit_not_required():
    estimator = NoFitRequiredEstimator()
    # Inicializar X a None explícitamente para evitar AttributeError al evaluar self.X
    estimator.X = None
    result = estimator.predict(np.array([[1]]))
    assert result[0] == 2.0

def test_predict_X_is_none_error():
    estimator = ConcreteEstimator()
    estimator.X = None
    with pytest.raises(ValueError, match="You must call `fit` before `predict`"):
        estimator.predict(np.array([[1]]))

def test_predict_X_conversion_triggered():
    estimator = ConcreteEstimator()
    estimator.fit(np.array([[1]]), np.array([1]))
    
    # Verificamos que si pasamos una lista, se invoca la conversión a np.ndarray
    # Usamos patch sobre 'Public_Proyects.svm.base.np.array' para interceptar la conversión dentro del método
    with patch('Public_Proyects.svm.base.np.array', wraps=np.array) as mock_np:
        estimator.predict([[1]])
        mock_np.assert_called()

# --- Pruebas de cobertura general ---

def test_fit_method():
    estimator = ConcreteEstimator()
    X = np.array([[1]])
    y = np.array([1])
    estimator.fit(X, y)
    assert np.array_equal(estimator.X, X)
    assert np.array_equal(estimator.y, y)

def test_abstract_predict_raises():
    estimator = BaseEstimator()
    # Para llamar a _predict directamente y probar la excepción sin pasar por la validación de fit
    with pytest.raises(NotImplementedError):
        estimator._predict()

def test_errors_cases():
    estimator = BaseEstimator()
    
    with pytest.raises(ValueError, match="Got an empty matrix."):
        estimator._setup_input(np.array([]))
        
    with pytest.raises(ValueError, match="Missed required argument y"):
        estimator._setup_input(np.array([[1]]), None)
        
    with pytest.raises(ValueError, match="The targets array must be no-empty."):
        estimator._setup_input(np.array([[1]]), np.array([]))