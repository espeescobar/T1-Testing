import pytest
import numpy as np
from unittest.mock import MagicMock
from Public_Proyects.svm.base import BaseEstimator

class ConcreteEstimator(BaseEstimator):
    def _predict(self, X=None):
        return np.zeros(X.shape[0])

class NoYEstimator(BaseEstimator):
    y_required = False
    def _predict(self, X=None):
        return np.ones(X.shape[0])

def test_setup_input_valid():
    estimator = ConcreteEstimator()
    X = np.array([[1, 2], [3, 4]])
    y = np.array([0, 1])
    estimator._setup_input(X, y)
    assert estimator.X.shape == (2, 2)
    assert np.array_equal(estimator.y, y)
    assert estimator.n_samples == 2
    assert estimator.n_features == 2

def test_setup_input_list_conversion():
    estimator = ConcreteEstimator()
    estimator._setup_input([[1]], [0])
    assert isinstance(estimator.X, np.ndarray)
    assert isinstance(estimator.y, np.ndarray)

def test_setup_input_empty_matrix_raises():
    estimator = ConcreteEstimator()
    with pytest.raises(ValueError, match="Got an empty matrix."):
        estimator._setup_input(np.array([]), [1])

def test_setup_input_missing_y_raises():
    estimator = ConcreteEstimator()
    with pytest.raises(ValueError, match="Missed required argument y"):
        estimator._setup_input(np.array([[1]]), None)

def test_setup_input_empty_y_raises():
    estimator = ConcreteEstimator()
    with pytest.raises(ValueError, match="The targets array must be no-empty."):
        estimator._setup_input(np.array([[1]]), np.array([]))

def test_setup_input_y_not_required():
    estimator = NoYEstimator()
    estimator._setup_input(np.array([[1, 2]]), y=None)
    assert estimator.y is None

def test_predict_without_fit_raises():
    estimator = ConcreteEstimator()
    # Inicializar X para evitar AttributeError y forzar el camino del else en predict
    estimator.X = None
    with pytest.raises(ValueError, match="You must call `fit` before `predict`"):
        estimator.predict(np.array([[1]]))

def test_predict_success():
    estimator = ConcreteEstimator()
    X_fit = np.array([[1, 2]])
    y_fit = np.array([1])
    estimator.fit(X_fit, y_fit)
    
    X_test = np.array([[3, 4]])
    result = estimator.predict(X_test)
    assert np.array_equal(result, np.array([0]))

def test_not_implemented_predict():
    base = BaseEstimator()
    base.X = np.array([[1]]) 
    with pytest.raises(NotImplementedError):
        base._predict(np.array([[1]]))

def test_fit_calls_setup_input():
    estimator = ConcreteEstimator()
    estimator._setup_input = MagicMock()
    X = np.array([[1]])
    y = np.array([0])
    estimator.fit(X, y)
    estimator._setup_input.assert_called_once_with(X, y)

def test_predict_no_fit_required():
    class NoFitRequiredEstimator(BaseEstimator):
        fit_required = False
        def _predict(self, X=None):
            return np.array([99])
            
    estimator = NoFitRequiredEstimator()
    # Para evitar el AttributeError, inicializamos X como None explícitamente
    estimator.X = None
    res = estimator.predict(np.array([[1]]))
    assert res[0] == 99