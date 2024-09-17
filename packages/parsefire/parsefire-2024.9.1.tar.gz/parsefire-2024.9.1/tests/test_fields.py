import unittest
from parsefire.parser import parse_fields, Int, String, Char, Slug, Float, Line


class TestParseFields(unittest.TestCase):

    def test_parse_int_field(self):
        spec = "Age: <int:age>"
        text = "Age: 25"
        result = parse_fields(spec, text)
        self.assertEqual(result, {'age': 25})

    def test_parse_string_field(self):
        spec = "Name: <str:name>"
        text = "Name: John Doe"
        result = parse_fields(spec, text)
        self.assertEqual(result, {'name': 'John Doe'})

    def test_parse_char_field(self):
        spec = "Initial: <char:initial>"
        text = "Initial: J"
        result = parse_fields(spec, text)
        self.assertEqual(result, {'initial': 'J'})

    def test_parse_slug_field(self):
        spec = "Slug: <slug:slug>"
        text = "Slug: my-slug_123"
        result = parse_fields(spec, text)
        self.assertEqual(result, {'slug': 'my-slug_123'})

    def test_parse_float_field(self):
        spec = "Value: <float:value>"
        text = "Value: 123.45"
        result = parse_fields(spec, text)
        self.assertEqual(result, {'value': 123.45})

    def test_parse_line_field(self):
        spec = "Line: <line:line>"
        text = "Line: \nThis is a line\n"
        result = parse_fields(spec, text)
        self.assertEqual(result, {'line': 'This is a line'})

    def test_parse_multiple_fields(self):
        spec = "Age: <int:age> Name: <str:name>"
        text = "Age: 25 Name: John Doe"
        result = parse_fields(spec, text)
        self.assertEqual(result, {'age': 25, 'name': 'John Doe'})

    def test_parse_with_custom_regex(self):
        spec = r"Code: <str:code:([A-Z]{3}-\d{3})>"
        text = "Code: ABC-123"
        result = parse_fields(spec, text)
        self.assertEqual(result, {'code': 'ABC-123'})

    def test_parse_table(self):
        spec = "Row: <int:id> <str:name>"
        text = "Row: 1 John\nRow: 2 Jane"
        result = parse_fields(spec, text, table=True)
        self.assertEqual(result, [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}])


if __name__ == '__main__':
    unittest.main()
