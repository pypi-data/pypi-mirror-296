import unittest
from parsefire.parser import parse_text


class TestParseText(unittest.TestCase):

    def test_parse_text_with_domain(self):
        specs = {
            'domain': r"Inside:(.*?)(?=Outside|$)",
            'fields': [
                "Age: <int:age>",
                "Name: <str:name>"
            ]
        }
        text = (
            "Inside:\n"
            "Age: 25\n"
            "Name: John Doe\n"
            "Outside:\n"
            "Age: 30\n"
            "Name: Jane Doe"
        )
        result = parse_text(specs, text)
        self.assertEqual(result, {'age': 25, 'name': 'John Doe'})

    def test_parse_text_with_domains(self):
        specs = {
            'domains': r"Inside:(.*?)(?=Outside|$)",
            'fields': [
                "Age: <int:age>",
                "Name: <str:name>"
            ]
        }
        text = (
            "Inside:\n"
            "Age: 25\n"
            "Name: John Doe\n"
            "Outside:\n"
            "Age: 36\n"
            "Name: Jack Doe"
            "Inside:\n"
            "Age: 30\n"
            "Name: Jane Doe"
        )
        result = parse_text(specs, text)
        self.assertEqual(result, {'age': 25, 'name': 'John Doe'})

    def test_parse_table_with_domains(self):
        specs = {
            'domains': r"Inside:(.*?)(?=Outside|$)",
            'table': [
                "Age: <int:age>",
                "Name: <str:name>"
            ]
        }
        text = (
            "Inside:\n"
            "Age: 25\n"
            "Name: John Doe\n"
            "Outside:\n"
            "Age: 36\n"
            "Name: Jack Doe"
            "Inside:\n"
            "Age: 30\n"
            "Name: Jane Doe"
        )
        result = parse_text(specs, text)
        self.assertEqual(result, [{'age': 25, 'name': 'John Doe'}, {'age': 30, 'name': 'Jane Doe'}])


if __name__ == '__main__':
    unittest.main()
