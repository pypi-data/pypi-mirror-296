import unittest
from parsefire.parser import Int, String, Char, Slug, Float, Line


class TestConverters(unittest.TestCase):

    def test_int_converter(self):
        self.assertEqual(Int.to_python(" 123 "), 123)
        self.assertEqual(Int.to_python("-123"), -123)
        self.assertEqual(Int.to_python("+123"), 123)
        self.assertRegex(" 123 ", Int.regex("test"))
        self.assertRegex("-123", Int.regex("test"))
        self.assertRegex("+123", Int.regex("test"))

    def test_string_converter(self):
        self.assertEqual(String.to_python("  hello  "), "hello")
        self.assertEqual(String.to_python("world"), "world")
        self.assertRegex("hello", String.regex("test"))
        self.assertRegex("world", String.regex("test"))

    def test_char_converter(self):
        self.assertEqual(Char.to_python("a"), "a")
        self.assertEqual(Char.to_python("z"), "z")
        self.assertRegex("a", Char.regex("test"))
        self.assertRegex("z", Char.regex("test"))

    def test_slug_converter(self):
        self.assertEqual(Slug.to_python("  my-slug_123  "), "my-slug_123")
        self.assertEqual(Slug.to_python("another/slug \n"), "another/slug")
        self.assertRegex("my-slug_123", Slug.regex("test"))
        self.assertRegex("another/slug", Slug.regex("test"))

    def test_float_converter(self):
        self.assertEqual(Float.to_python(" 123.45 "), 123.45)
        self.assertEqual(Float.to_python("-123.45"), -123.45)
        self.assertEqual(Float.to_python("+123.45"), 123.45)
        self.assertEqual(Float.to_python("+123.45E+5"), 123.45e5)
        self.assertEqual(Float.to_python("+123.45E5"), 123.45e5)
        self.assertEqual(Float.to_python("+123.45e+5"), 123.45e5)
        self.assertEqual(Float.to_python("+123.45e5"), 123.45e5)
        self.assertEqual(Float.to_python("+123.45E-5"), 123.45e-5)
        self.assertEqual(Float.to_python("+123.45e-5"), 123.45e-5)
        self.assertRegex(" 123.45 ", Float.regex("test"))
        self.assertRegex("-123.45", Float.regex("test"))
        self.assertRegex("+123.45", Float.regex("test"))

    def test_line_converter(self):
        self.assertEqual(Line.to_python("This is a line"), "This is a line")
        self.assertRegex("This is a line", Line.regex("test"))


if __name__ == '__main__':
    unittest.main()