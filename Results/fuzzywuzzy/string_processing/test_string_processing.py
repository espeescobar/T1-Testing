import pytest
import sys
import importlib
from unittest.mock import MagicMock, patch
import Public_Proyects.fuzzywuzzy.string_processing as sp
from Public_Proyects.fuzzywuzzy.string_processing import StringProcessor

class TestStringProcessor:

    def test_branch_coverage_py3_false_simulation(self):
        """
        Para cubrir el branch 'if PY3:', debemos simular un entorno Python 2
        antes de que el módulo sea cargado. Usamos un subproceso o manipulamos
        sys.modules para forzar el path de ejecución de la rama.
        """
        with patch.dict(sys.modules, {'Public_Proyects.fuzzywuzzy.string_processing': None}):
            # Simulamos que sys.version_info[0] != 3
            with patch('sys.version_info', (2, 7, 18)):
                # Necesitamos re-importar el módulo para que ejecute la lógica de carga
                import Public_Proyects.fuzzywuzzy.string_processing as sp_py2
                assert sp_py2.PY3 is False
                # En Py2, 'string' es el módulo de librería estándar 'string'
                import string as std_string
                assert sp_py2.string == std_string

    def test_regex_processing_behavior(self):
        processor = StringProcessor()
        # (?ui)\W significa Unicode + Insensible a mayúsculas, \W es cualquier carácter no alfanumérico
        assert processor.replace_non_letters_non_numbers_with_whitespace("hello!!!world") == "hello   world"
        assert processor.replace_non_letters_non_numbers_with_whitespace("abc123DEF") == "abc123DEF"
        assert processor.replace_non_letters_non_numbers_with_whitespace("áéíóú@") == "áéíóú "

    def test_static_methods(self):
        assert StringProcessor.strip("  test  ") == "test"
        assert StringProcessor.to_lower_case("TEST") == "test"
        assert StringProcessor.to_upper_case("test") == "TEST"

    def test_mocking_with_magic_mock(self):
        mock_obj = MagicMock()
        mock_obj.get_string.return_value = "hello!!!world"
        
        val = mock_obj.get_string()
        processed = StringProcessor.replace_non_letters_non_numbers_with_whitespace(val)
        
        assert processed == "hello   world"
        mock_obj.get_string.assert_called_once()

    @pytest.mark.parametrize("input_val, expected", [
        ("no_change", "no_change"),
        ("123-456", "123 456"),
        ("", ""),
        ("   ", "   "),
        ("___", "___"),
    ])
    def test_replace_parametrized(self, input_val, expected):
        assert StringProcessor.replace_non_letters_non_numbers_with_whitespace(input_val) == expected

    def test_type_error_handling(self):
        # Probar que las funciones fallan correctamente ante tipos inesperados
        with pytest.raises(TypeError):
            StringProcessor.replace_non_letters_non_numbers_with_whitespace(None)
        
        with pytest.raises(TypeError):
            StringProcessor.strip(None)
            
        with pytest.raises(TypeError):
            StringProcessor.to_lower_case(123)

    def test_class_regex_attribute(self):
        assert hasattr(StringProcessor, 'regex')
        assert StringProcessor.regex.pattern == r"(?ui)\W"

    def test_py3_initialization_state(self):
        # Verifica la rama por defecto (Python 3)
        assert sp.PY3 is True
        assert sp.string == str

    def test_branch_logic_context(self):
        input_data = "Data_Test@123"
        assert StringProcessor.replace_non_letters_non_numbers_with_whitespace(input_data) == "Data_Test 123"