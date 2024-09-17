import unittest
from parsefire.parser import build_pattern


class TestBuildPattern(unittest.TestCase):

    def test_simple_pattern(self):
        pattern, variables = build_pattern("<int:age>")
        self.assertEqual(len(variables), 1)
        self.assertEqual(variables[0]['name'], 'age')
        self.assertEqual(variables[0]['type'], 'int')

    def test_pattern_with_size(self):
        pattern, variables = build_pattern("<char:initial:1>")
        self.assertEqual(len(variables), 1)
        self.assertEqual(variables[0]['name'], 'initial')
        self.assertEqual(variables[0]['type'], 'char')
        self.assertEqual(variables[0]['size'], '1')

    def test_pattern_with_custom_regex(self):
        pattern, variables = build_pattern(r"<str:name:(\w+)>")
        self.assertEqual(len(variables), 1)
        self.assertEqual(variables[0]['name'], 'name')
        self.assertEqual(variables[0]['type'], 'str')
        self.assertEqual(variables[0]['regex'], r'\w+')

    def test_multiple_tokens(self):
        pattern, variables = build_pattern("<int:age> <str:name>")
        self.assertEqual(len(variables), 2)
        self.assertEqual(variables[0]['name'], 'age')
        self.assertEqual(variables[0]['type'], 'int')
        self.assertEqual(variables[1]['name'], 'name')
        self.assertEqual(variables[1]['type'], 'str')

    def test_escaped_characters(self):
        pattern, variables = build_pattern("<str:text> (escaped)")
        self.assertEqual(len(variables), 1)
        self.assertEqual(variables[0]['name'], 'text')
        self.assertEqual(variables[0]['type'], 'str')


if __name__ == '__main__':
    unittest.main()
