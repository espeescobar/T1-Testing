import pytest
from unittest.mock import MagicMock
from Public_Proyects.stock4.tableformat import (
    print_table,
    TableFormatter,
    TextTableFormatter,
    CSVTableFormatter,
    HTMLTableFormatter,
    ColumnFormatMixin,
    UpperHeadersMixin,
    create_formatter
)

def test_print_table_invalid_formatter():
    with pytest.raises(RuntimeError, match='Expected a TableFormatter'):
        print_table([], [], None)

def test_print_table_execution():
    mock_formatter = MagicMock(spec=TableFormatter)
    records = [MagicMock(a=1, b=2)]
    fields = ['a', 'b']
    
    print_table(records, fields, mock_formatter)
    
    mock_formatter.headings.assert_called_once_with(fields)
    mock_formatter.row.assert_called_once_with([1, 2])

def test_text_table_formatter(capsys):
    formatter = TextTableFormatter()
    formatter.headings(['Name', 'Price'])
    formatter.row(['AAPL', 100])
    
    captured = capsys.readouterr()
    assert '      Name      Price' in captured.out
    assert 'AAPL        100' in captured.out

def test_csv_table_formatter(capsys):
    formatter = CSVTableFormatter()
    formatter.headings(['Name', 'Price'])
    formatter.row(['AAPL', 100])
    
    captured = capsys.readouterr()
    assert 'Name,Price' in captured.out
    assert 'AAPL,100' in captured.out

def test_html_table_formatter(capsys):
    formatter = HTMLTableFormatter()
    formatter.headings(['Name'])
    formatter.row(['AAPL'])
    
    captured = capsys.readouterr()
    assert '<tr> <th>Name</th> </tr>' in captured.out
    assert '<tr> <td>AAPL</td> </tr>' in captured.out

def test_column_format_mixin():
    # Para que super() funcione, la clase debe heredar de una clase que tenga el método
    class BaseMock(TableFormatter):
        def headings(self, headers): pass
        def row(self, rowdata): pass

    class TestFormatter(ColumnFormatMixin, BaseMock):
        pass

    formatter = TestFormatter()
    formatter.formats = ['%.2f', '%s']
    # Usamos un mock para verificar que el método row finalmente llama al padre
    formatter.row = MagicMock()
    
    # Inyectamos el comportamiento del mixin llamando manualmente o creando una instancia real
    ColumnFormatMixin.row(formatter, [1.234, 'test'])
    
    formatter.row.assert_called_with(['1.23', 'test'])

def test_upper_headers_mixin():
    class BaseMock(TableFormatter):
        def headings(self, headers): pass
        def row(self, rowdata): pass

    class TestFormatter(UpperHeadersMixin, BaseMock):
        pass

    formatter = TestFormatter()
    formatter.headings = MagicMock()
    
    UpperHeadersMixin.headings(formatter, ['name', 'price'])
    
    formatter.headings.assert_called_with(['NAME', 'PRICE'])

def test_create_formatter_invalid():
    with pytest.raises(RuntimeError, match='Unknown format'):
        create_formatter('invalid')

@pytest.mark.parametrize("name", ['text', 'csv', 'html'])
def test_create_formatter_types(name):
    formatter = create_formatter(name)
    assert isinstance(formatter, TableFormatter)

def test_create_formatter_with_mixins():
    formatter = create_formatter('text', column_formats=['%s'], upper_headers=True)
    assert isinstance(formatter, TextTableFormatter)
    assert hasattr(formatter, 'formats')
    assert formatter.formats == ['%s']
    assert isinstance(formatter, ColumnFormatMixin)
    assert isinstance(formatter, UpperHeadersMixin)