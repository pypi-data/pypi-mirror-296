import unittest

from jstring import String, StringBuilder, StringBuffer


class StringTest(unittest.TestCase):
    def setUp(self):
        self.s0 = String()
        self.s1 = String("hello")
        self.s2 = String("world")
        self.s3 = String("hello world")
        self.s4 = String(["hello", "world"])
        self.s5 = String.from_char_array(['h', 'e', 'l', 'l', 'o'])
        self.s6 = String.from_code_points([104, 101, 108, 108, 111])
        self.sb1 = String(StringBuilder("hello"))
        self.sb2 = String(StringBuffer("world"))
        self.sb3 = String(StringBuilder().append("hello").append(" world"))
        self.sb4 = String(StringBuffer().append("hello").append(" world"))

    def test_constructor(self):
        self.assertEqual(str(self.s1), "hello")
        self.assertEqual(str(self.s4), "helloworld")
        self.assertEqual(str(self.s5), "hello")
        self.assertEqual(str(self.s6), "hello")

    def test_addition(self):
        self.assertEqual(str(self.s1 + self.s2), "helloworld")
        self.assertEqual(str(self.s1 + " world"), "hello world")

    def test_length(self):
        self.assertEqual(self.s1.length(), 5)

    def test_charAt(self):
        self.assertEqual(self.s1.charAt(0), 'h')
        with self.assertRaises(IndexError):
            self.s1.charAt(5)

    def test_codePointAt(self):
        self.assertEqual(self.s1.codePointAt(0), ord('h'))
        with self.assertRaises(IndexError):
            self.s1.codePointAt(5)

    def test_compareTo(self):
        self.assertEqual(self.s1.compareTo(self.s2), -1)
        self.assertEqual(self.s1.compareTo(self.s3), -1)
        self.assertEqual(self.s3.compareTo(self.s3), 0)

    def test_contains(self):
        self.assertTrue(self.s3.contains("hello"))
        self.assertFalse(self.s3.contains("goodbye"))

    def test_equals(self):
        self.assertTrue(self.s1.equals("hello"))
        self.assertFalse(self.s1.equals("world"))

    def test_equalsIgnoreCase(self):
        self.assertTrue(self.s1.equalsIgnoreCase("HELLO"))

    def test_format(self):
        self.assertEqual(str(String.format("Hello, {}!", "world")), "Hello, world!")

    def test_getBytes(self):
        self.assertEqual(self.s1.getBytes(), b"hello")

    def test_hashCode(self):
        self.assertEqual(self.s1.hashCode(), hash("hello"))

    def test_indexOf(self):
        self.assertEqual(self.s1.indexOf('l'), 2)
        self.assertEqual(self.s1.indexOf('l', 3), 3)

    def test_isEmpty(self):
        self.assertFalse(self.s1.isEmpty())
        self.assertTrue(String().isEmpty())

    def test_lastIndexOf(self):
        self.assertEqual(self.s1.lastIndexOf(ord('l')), 3)

    def test_length(self):
        self.assertEqual(self.s1.length(), 5)

    def test_matches(self):
        self.assertTrue(self.s1.matches("hello"))
        self.assertFalse(self.s1.matches("world"))

    def test_replace(self):
        self.assertEqual(str(self.s1.replace('l', 'L')), "heLLo")

    def test_split(self):
        self.assertEqual([str(s) for s in self.s3.split(" ")], ["hello", "world"])

    def test_substring(self):
        self.assertEqual(str(self.s1.substring(0, 2)), "he")
        self.assertEqual(str(self.s1.substring(2)), "llo")

    def test_toLowerCase(self):
        self.assertEqual(str(self.s1.toLowerCase()), "hello")

    def test_toUpperCase(self):
        self.assertEqual(str(self.s1.toUpperCase()), "HELLO")

    def test_trim(self):
        self.assertEqual(str(String("   hello   ").trim()), "hello")

    def test_sb1_type(self):
        self.assertIsInstance(self.sb1, String)

    def test_sb2_type(self):
        self.assertIsInstance(self.sb2, String)

    def test_sb3_type(self):
        self.assertIsInstance(self.sb3, String)

    def test_sb4_type(self):
        self.assertIsInstance(self.sb4, String)

    def test_sb1_content(self):
        self.assertEqual(self.sb1, "hello")

    def test_sb2_content(self):
        self.assertEqual(self.sb2, "world")

    def test_sb3_content(self):
        self.assertEqual(self.sb3, "hello world")

    def test_sb4_content(self):
        self.assertEqual(self.sb4, "hello world")

if __name__ == "__main__":
    unittest.main()
