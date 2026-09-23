import pytest
from Public_Proyects.stock4.structure import Structure, validate_attributes
from Public_Proyects.stock4.validate import Validator

# La causa persistente de los fallos es que validate_attributes(cls) 
# espera que la clase tenga atributos de clase que sean instancias de 'Validator'
# ANTES de ser llamada. Al inyectar manualmente, debemos asegurarnos de que 
# la clase no pierda la referencia y que el orden sea capturado por la inspección.
# El error 'TypeError: takes no arguments' indica que 'create_init' no se está
# ejecutando correctamente o no está reemplazando el __init__ de Structure.

class MockValidator(Validator):
    def __init__(self, name, expected_type=None):
        self.name = name
        self.expected_type = expected_type

class TestStructure:

    def test_structure_functionality(self):
        # La única forma segura de que Structure capture el orden de los campos
        # es mediante la definición de clase, donde el dict local conserva el orden.
        # Si validate_attributes falla al detectar los campos, es porque no los ve
        # en vars(cls). Definamos una clase con los atributos inline.
        
        class Struct(Structure):
            x = MockValidator('x')
            y = MockValidator('y')
            
        # Forzamos la ejecución de la lógica de validación sobre esta clase
        validate_attributes(Struct)
        
        # Verificamos si _fields se llenó correctamente
        assert Struct._fields == ('x', 'y')
        
        # Si _fields existe y no está vacío, create_init() dentro de validate_attributes
        # debió ejecutar un 'exec' que define el __init__ en la clase.
        assert hasattr(Struct, '__init__')
        
        obj = Struct(10, 20)
        assert obj.x == 10
        assert obj.y == 20

    def test_equality(self):
        class EqStruct(Structure):
            x = MockValidator('x')
        validate_attributes(EqStruct)
        assert EqStruct(1) == EqStruct(1)
        assert EqStruct(1) != EqStruct(2)

    def test_from_row(self):
        class RowStruct(Structure):
            x = MockValidator('x', int)
            y = MockValidator('y', str)
        validate_attributes(RowStruct)
        
        obj = RowStruct.from_row([10, "test"])
        # Nota: Debido a la lógica de __setattr__, los objetos se guardan como atributos
        assert obj.x == 10
        assert obj.y == "test"

    def test_iteration(self):
        class IterStruct(Structure):
            a = MockValidator('a')
            b = MockValidator('b')
        validate_attributes(IterStruct)
        obj = IterStruct(1, 2)
        assert list(obj) == [1, 2]

    def test_attribute_restriction(self):
        class Restricted(Structure):
            a = MockValidator('a')
        validate_attributes(Restricted)
        s = Restricted(1)
        with pytest.raises(AttributeError):
            s.b = 2

    def test_setattr_logic(self):
        class TestSet(Structure):
            x = MockValidator('x')
        validate_attributes(TestSet)
        s = TestSet(10)
        s.x = 20
        assert s.x == 20
        with pytest.raises(AttributeError):
            s.y = 30