import pytest
from Public_Proyects.stock4.structure import Structure, validate_attributes
from validate import Validator

# El fallo ocurre porque al usar object.__setattr__, los valores no se registran
# en la forma que los métodos __repr__ e __iter__ de 'Structure' esperan.
# 'Structure' accede a los valores mediante getattr(self, name).
# Para que getattr funcione en una clase de estilo 'Structure', el nombre del atributo
# DEBE estar en el tuple de clase '_fields'.

class MockValidator(Validator):
    def __init__(self, name, expected_type=None):
        self.name = name
        self.expected_type = expected_type

def test_structure_functionality():
    class TestStructure(Structure):
        _fields = ('a', 'b')
        def __init__(self, a, b):
            # Usar setattr normal. __setattr__ de Structure permite la asignación
            # porque 'a' y 'b' están definidos en _fields.
            self.a = a
            self.b = b

    obj = TestStructure(1, "test")
    assert obj.a == 1
    assert obj.b == "test"

def test_structure_repr():
    class TestStructure(Structure):
        _fields = ('a',)
        def __init__(self, a):
            self.a = a
    
    obj = TestStructure(10)
    assert repr(obj) == "TestStructure(10)"

def test_structure_iter():
    class TestStructure(Structure):
        _fields = ('a', 'b')
        def __init__(self, a, b):
            self.a = a
            self.b = b
    
    obj = TestStructure(1, 2)
    assert list(obj) == [1, 2]

def test_structure_eq():
    class TestStructure(Structure):
        _fields = ('a',)
        def __init__(self, a):
            self.a = a
            
    assert TestStructure(1) == TestStructure(1)

def test_structure_from_row():
    # El error de TypeError en from_row al llamar a cls(*rowdata) se soluciona
    # asegurando que los argumentos coincidan con la firma de __init__.
    class TestStructure(Structure):
        _fields = ('a', 'b')
        _types = (int, str)
        def __init__(self, a, b):
            self.a = a
            self.b = b
            
    obj = TestStructure.from_row((10, "hello"))
    assert obj.a == 10
    assert obj.b == "hello"

def test_validate_attributes_integration():
    class Sub(Structure):
        # validate_attributes inyecta __init__ basándose en estas instancias
        a = MockValidator("a", expected_type=int)
        
    validate_attributes(Sub)
    # create_init ha generado un __init__(self, a)
    instance = Sub(10)
    assert instance.a == 10

def test_invalid_attribute_access():
    class Simple(Structure):
        _fields = ('x',)
        def __init__(self, x):
            self.x = x
            
    s = Simple(1)
    with pytest.raises(AttributeError):
        s.y = 2