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
        return np.zeros(X.shape[0])

def test_setup_input_valid_data():
    estimator = BaseEstimator()
    X = np.array([[1, 2], [3, 4]])
    y = np.array([0, 1])
    estimator._setup_input(X, y)
    assert np.array_equal(estimator.X, X)
    assert np.array_equal(estimator.y, y)
    assert estimator.n_samples == 2
    assert estimator.n_features == 2

def test_setup_input_empty_matrix():
    estimator = BaseEstimator()
    with pytest.raises(ValueError, match="Got an empty matrix."):
        estimator._setup_input(np.array([]))

def test_setup_input_missing_y():
    estimator = BaseEstimator()
    with pytest.raises(ValueError, match="Missed required argument y"):
        estimator._setup_input(np.array([[1]]))

def test_setup_input_empty_y():
    estimator = BaseEstimator()
    with pytest.raises(ValueError, match="The targets array must be no-empty."):
        estimator._setup_input(np.array([[1]]), np.array([]))

def test_setup_input_1d_array():
    estimator = BaseEstimator()
    X = np.array([1, 2, 3])
    y = np.array([1])
    estimator._setup_input(X, y)
    assert estimator.n_samples == 1
    assert estimator.n_features == (3,)

def test_fit_calls_setup():
    estimator = ConcreteEstimator()
    mock_setup = MagicMock(return_value=None)
    # Patching method on instance
    estimator._setup_input = mock_setup
    X = np.array([[1]])
    y = np.array([1])
    estimator.fit(X, y)
    mock_setup.assert_called_once_with(X, y)

def test_predict_without_fit_raises_error():
    estimator = ConcreteEstimator()
    # Initialize X to None to avoid AttributeError during check
    estimator.X = None
    with pytest.raises(ValueError, match="You must call `fit` before `predict`"):
        estimator.predict(np.array([[1]]))

def test_predict_success():
    estimator = ConcreteEstimator()
    X_train = np.array([[1, 2]])
    y_train = np.array([1])
    X_test = np.array([[3, 4]])
    
    estimator.fit(X_train, y_train)
    result = estimator.predict(X_test)
    assert isinstance(result, np.ndarray)
    assert len(result) == 1

def test_predict_no_fit_required():
    estimator = NoYEstimator()
    estimator.fit_required = False
    # Ensure X is not set to avoid AttributeError
    estimator.X = None
    result = estimator.predict(np.array([[1, 2]]))
    assert result is not None

def test_abstract_predict_raises_not_implemented():
    estimator = BaseEstimator()
    with pytest.raises(NotImplementedError):
        estimator._predict(np.array([[1]]))