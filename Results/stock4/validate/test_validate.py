import pytest
from unittest.mock import MagicMock
from Public_Proyects.stock4.validate import (
    Validator, Typed, Integer, Float, String, Positive, NonEmpty,
    PositiveInteger, PositiveFloat, NonEmptyString, validated, enforce
)

# --- Tests for Validators ---

def test_validator_basic():
    v = Validator()
    assert v.check(10) == 10

def test_typed_validators():
    assert Integer.check(5) == 5
    assert Float.check(1.5) == 1.5
    assert String.check("test") == "test"
    
    with pytest.raises(TypeError):
        Integer.check("not an int")
    with pytest.raises(TypeError):
        Float.check(10)
    with pytest.raises(TypeError):
        String.check(123)

def test_positive_validator():
    assert Positive.check(0) == 0
    assert Positive.check(10) == 10
    with pytest.raises(ValueError):
        Positive.check(-1)

def test_nonempty_validator():
    assert NonEmpty.check("abc") == "abc"
    with pytest.raises(ValueError):
        NonEmpty.check("")

def test_composed_validators():
    assert PositiveInteger.check(10) == 10
    with pytest.raises(TypeError):
        PositiveInteger.check(1.5)
    with pytest.raises(ValueError):
        PositiveInteger.check(-5)

    assert NonEmptyString.check("data") == "data"
    with pytest.raises(ValueError):
        NonEmptyString.check("")

# --- Tests for Descriptor mechanics ---

class MockModel:
    attr = Integer()

def test_descriptor_set():
    m = MockModel()
    m.attr = 10
    assert m.attr == 10
    with pytest.raises(TypeError):
        m.attr = "string"

# --- Tests for Decorators ---

@validated
def func_validated(a: Integer, b: Positive):
    return a + b

def test_validated_decorator():
    assert func_validated(1, 2) == 3
    with pytest.raises(TypeError, match="Bad Arguments"):
        func_validated("1", 2)
    with pytest.raises(TypeError, match="Bad Arguments"):
        func_validated(1, -1)

@validated
def func_with_return(a: Integer) -> Positive:
    return a

def test_validated_return():
    assert func_with_return(10) == 10
    with pytest.raises(TypeError, match="Bad return"):
        func_with_return(-1)

@enforce(a=Integer, return_=Positive)
def func_enforce(a):
    return a

def test_enforce_decorator():
    assert func_enforce(10) == 10
    with pytest.raises(TypeError, match="Bad Arguments"):
        func_enforce("string")
    with pytest.raises(TypeError, match="Bad return"):
        func_enforce(-1)

# --- Tests for edge cases and Mocks ---

def test_isvalidator_logic():
    from Public_Proyects.stock4.validate import isvalidator
    assert isvalidator(Integer) is True
    assert isvalidator(str) is False
    
    mock_class = MagicMock()
    mock_class.__name__ = "Mock"
    # Testing logic inside isvalidator via behavior
    assert isvalidator(int) is False

def test_validator_init_subclass():
    class NewVal(Validator):
        pass
    assert "NewVal" in Validator.validators
    assert Validator.validators["NewVal"] == NewVal