import pytest
import numpy as np
from Public_Proyects.svm.base import BaseEstimator

class ConcreteEstimator(BaseEstimator):
    def _predict(self, X=None):
        return np.zeros(X.shape[0])

def test_setup_input_valid_data():
    estimator = ConcreteEstimator()
    X = np.array([[1, 2], [3, 4]])
    y = np.array([0, 1])
    estimator._setup_input(X, y)
    assert estimator.X.shape == (2, 2)
    assert np.array_equal(estimator.y, y)
    assert estimator.n_samples == 2
    assert estimator.n_features == 2

def test_setup_input_conversion():
    estimator = ConcreteEstimator()
    X = [[1, 2], [3, 4]]
    y = [0, 1]
    estimator._setup_input(X, y)
    assert isinstance(estimator.X, np.ndarray)
    assert isinstance(estimator.y, np.ndarray)

def test_setup_input_empty_matrix_raises_error():
    estimator = ConcreteEstimator()
    with pytest.raises(ValueError, match="Got an empty matrix."):
        estimator._setup_input(np.array([]))

def test_setup_input_missing_y_raises_error():
    estimator = ConcreteEstimator()
    with pytest.raises(ValueError, match="Missed required argument y"):
        estimator._setup_input(np.array([[1, 2]]))

def test_setup_input_empty_y_raises_error():
    estimator = ConcreteEstimator()
    with pytest.raises(ValueError, match="The targets array must be no-empty."):
        estimator._setup_input(np.array([[1, 2]]), np.array([]))

def test_predict_without_fit_raises_error():
    estimator = ConcreteEstimator()
    with pytest.raises(ValueError, match="You must call `fit` before `predict`"):
        estimator.predict(np.array([[1, 2]]))

def test_predict_success():
    estimator = ConcreteEstimator()
    X = np.array([[1, 2], [3, 4]])
    y = np.array([0, 1])
    estimator.fit(X, y)
    result = estimator.predict(X)
    assert len(result) == 2
    assert np.all(result == 0)

def test_y_not_required_behavior():
    class NoYEstimator(BaseEstimator):
        y_required = False
        def _predict(self, X=None): return X

    estimator = NoYEstimator()
    X = np.array([[1, 2]])
    estimator.fit(X)
    assert estimator.y is None
    assert np.array_equal(estimator.predict(X), X)