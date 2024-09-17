import unittest
from parsefire.parser import parse_text


class TestParseText(unittest.TestCase):

    def test_parse_text_with_simple_fields(self):
        specs = {
            'fields': [
                "Age: <int:age>",
                "Name: <str:name>"
            ]
        }
        text = "Age: 25\nName: John Doe"
        result = parse_text(specs, text)
        self.assertEqual(result, {'age': 25, 'name': 'John Doe'})

    def test_parse_text_with_nested_sections(self):
        specs = {
            'sections': {
                'person': {
                    'fields': [
                        "Age: <int:age>",
                        "Name: <str:name>"
                    ]
                }
            }
        }
        text = "Age: 25\nName: John Doe"
        result = parse_text(specs, text)
        self.assertEqual(result, {'person': {'age': 25, 'name': 'John Doe'}})

    def test_parse_text_with_table(self):
        specs = {
            'table': "Row: <int:id> <str:name>"
        }
        text = "Row: 1 John\nRow: 2 Jane"
        result = parse_text(specs, text)
        self.assertEqual(result, [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}])

    def test_parse_text_with_custom_regex(self):
        specs = {
            'fields': [
                r"Code: <str:code:([A-Z]{3}-\d{3})>"
            ]
        }
        text = "Code: ABC-123"
        result = parse_text(specs, text)
        self.assertEqual(result, {'code': 'ABC-123'})

    def test_parse_text_with_lines(self):
        specs = {
            'lines': [
                "Line: <line:line>"
            ]
        }
        text = "Line: \nThis is a line\n"
        result = parse_text(specs, text)
        self.assertEqual(result, {'line': 'This is a line'})


if __name__ == '__main__':
    unittest.main()