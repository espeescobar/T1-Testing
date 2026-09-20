import pytest
from unittest.mock import MagicMock
from Public_Proyects.stock4.validate import (
    Validator, Typed, Integer, Float, String, Positive, 
    NonEmpty, PositiveInteger, PositiveFloat, NonEmptyString,
    validated, enforce, isvalidator
)

class TestValidators:
    def test_integer_validator(self):
        val = Integer()
        val.check(10)
        with pytest.raises(TypeError):
            val.check("not an int")

    def test_float_validator(self):
        val = Float()
        val.check(10.5)
        with pytest.raises(TypeError):
            val.check(10)

    def test_string_validator(self):
        val = String()
        val.check("hello")
        with pytest.raises(TypeError):
            val.check(123)

    def test_positive_validator(self):
        val = Positive()
        val.check(5)
        with pytest.raises(ValueError):
            val.check(-1)

    def test_non_empty_validator(self):
        val = NonEmpty()
        val.check("abc")
        with pytest.raises(ValueError):
            val.check("")

    def test_composite_validators(self):
        pos_int = PositiveInteger()
        pos_int.check(10)
        with pytest.raises(ValueError):
            pos_int.check(-5)
        with pytest.raises(TypeError):
            pos_int.check(1.5)

        non_empty_str = NonEmptyString()
        non_empty_str.check("data")
        with pytest.raises(ValueError):
            non_empty_str.check("")

    def test_descriptor_behavior(self):
        class Container:
            x = Integer()
        
        c = Container()
        c.x = 10
        assert c.x == 10
        with pytest.raises(TypeError):
            c.x = "fail"

class TestDecorators:
    def test_isvalidator(self):
        assert isvalidator(Integer) is True
        assert isvalidator(str) is False
        assert isvalidator(object()) is False

    def test_validated_decorator(self):
        @validated
        def func(a: Integer, b: Positive) -> Float:
            return float(a + b)

        assert func(10, 5) == 15.0
        with pytest.raises(TypeError, match="Bad Arguments"):
            func("x", 5)
        with pytest.raises(TypeError, match="Bad return"):
            @validated
            def bad_ret(a: Integer) -> Positive:
                return -1
            bad_ret(10)

    def test_enforce_decorator(self):
        @enforce(a=Integer, b=Positive, return_=Float)
        def func(a, b):
            return float(a + b)

        assert func(10, 5) == 15.0
        with pytest.raises(TypeError, match="Bad Arguments"):
            func(1.5, 5)
        with pytest.raises(TypeError, match="Bad return"):
            @enforce(return_=Positive)
            def bad_ret():
                return -1
            bad_ret()

    def test_mocking_validator(self):
        mock_val = MagicMock()
        mock_val.check.return_value = True
        
        @enforce(val=mock_val)
        def func(val):
            return val
        
        func(100)
        mock_val.check.assert_called_with(100)

    def test_validator_subclass_registration(self):
        assert "Integer" in Validator.validators
        assert "Positive" in Validator.validators
        assert "NonEmpty" in Validator.validators