import pytest
from Public_Proyects.stock4.validate import (
    Validator, Typed, Integer, Float, String, Positive, NonEmpty, 
    PositiveInteger, PositiveFloat, NonEmptyString, 
    validated, enforce, isvalidator
)

# --- Pruebas para incrementar Branch Coverage ---

def test_validator_descriptor_set_name_coverage():
    # Cubre __set_name__ explícitamente
    v = Validator()
    v.__set_name__(None, "foo")
    assert v.name == "foo"

def test_typed_check_type_error_branch():
    # Cubre el if de isinstance en Typed
    with pytest.raises(TypeError):
        Typed.check(1)

def test_positive_value_error_branch():
    # Cubre el if value < 0 en Positive
    with pytest.raises(ValueError, match="must be >= 0"):
        Positive.check(-1)

def test_nonempty_value_error_branch():
    # Cubre el if len(value) == 0 en NonEmpty
    with pytest.raises(ValueError, match="must be non-empty"):
        NonEmpty.check("")

def test_validated_exception_wrapping():
    # Cubre el 'raise TypeError(...) from None' en la validación de retorno
    @validated
    def func() -> Positive:
        return -1
    with pytest.raises(TypeError) as exc:
        func()
    assert "Bad return" in str(exc.value)

def test_enforce_exception_wrapping():
    # Cubre el 'raise TypeError(...) from None' en enforce return
    @enforce(return_=Positive)
    def func():
        return -1
    with pytest.raises(TypeError) as exc:
        func()
    assert "Bad return" in str(exc.value)

def test_validator_init_subclass_coverage():
    # Verifica que __init_subclass__ registra la clase
    class MockValidator(Validator):
        pass
    assert Validator.validators["MockValidator"] is MockValidator

def test_isvalidator_logic_branch():
    # Cubre el 'isinstance(item, type) and issubclass(item, Validator)'
    # Caso donde es tipo pero no subclase
    assert isvalidator(int) is False
    # Caso donde es una subclase de Validator (clase, no instancia)
    assert isvalidator(Validator) is True

def test_validated_complex_annotations():
    # Cubre el filtrado de anotaciones (solo Validator)
    @validated
    def func(x: Integer, y: int): # 'int' debe ser ignorado
        return x + y
    assert func(1, 2) == 3

def test_enforce_binding_error():
    # Cubre TypeError si bind falla (ej. argumentos faltantes)
    @enforce(x=Integer)
    def func(x):
        return x
    with pytest.raises(TypeError):
        func() # Falta x

def test_validated_binding_error():
    # Cubre TypeError si bind falla en validated
    @validated
    def func(x: Integer):
        return x
    with pytest.raises(TypeError):
        func() # Falta x

def test_enforce_loop_exception_handling():
    # Cubre el bloque try/except dentro del loop de enforce
    @enforce(x=Positive)
    def func(x):
        return x
    # Provoca error en el validador
    with pytest.raises(TypeError) as exc:
        func(-5)
    assert "Bad Arguments" in str(exc.value)
    assert "x:" in str(exc.value)