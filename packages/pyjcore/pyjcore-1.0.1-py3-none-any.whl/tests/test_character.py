import unittest

from jstring import Character


class TestCharacter(unittest.TestCase):

    def test_charValue(self):
        c = Character('a')
        self.assertEqual(c.charValue(), 'a')

    def test_str(self):
        c = Character('b')
        self.assertEqual(str(c), 'b')

    def test_compareTo(self):
        c1 = Character('a')
        c2 = Character('b')
        self.assertTrue(c1.compareTo(c2) < 0)
        self.assertTrue(c2.compareTo(c1) > 0)
        self.assertTrue(c1.compareTo(Character('a')) == 0)

    def test_hashCode(self):
        c = Character('a')
        self.assertEqual(c.hashCode(), ord('a'))

    def test_equals(self):
        c1 = Character('a')
        c2 = Character('a')
        c3 = Character('b')
        self.assertTrue(c1.equals(c2))
        self.assertFalse(c1.equals(c3))
        self.assertFalse(c1.equals('a'))

    def test_isLetter(self):
        self.assertTrue(Character.isLetter('a'))
        self.assertFalse(Character.isLetter('1'))

    def test_isDigit(self):
        self.assertTrue(Character.isDigit('1'))
        self.assertFalse(Character.isDigit('a'))

    def test_isWhitespace(self):
        self.assertTrue(Character.isWhitespace(' '))
        self.assertFalse(Character.isWhitespace('a'))

    def test_isLowerCase(self):
        self.assertTrue(Character.isLowerCase('a'))
        self.assertFalse(Character.isLowerCase('A'))

    def test_isUpperCase(self):
        self.assertTrue(Character.isUpperCase('A'))
        self.assertFalse(Character.isUpperCase('a'))

    def test_isTitleCase(self):
        self.assertTrue(Character.isTitleCase('A'))
        self.assertFalse(Character.isTitleCase('a'))

    def test_toLowerCase(self):
        self.assertEqual(Character.toLowerCase('A'), 'a')

    def test_toUpperCase(self):
        self.assertEqual(Character.toUpperCase('a'), 'A')

    def test_codePointAt(self):
        self.assertEqual(Character.codePointAt('abc', 1), ord('b'))

    def test_codePointBefore(self):
        self.assertEqual(Character.codePointBefore('abc', 2), ord('b'))

    def test_charCount(self):
        self.assertEqual(Character.charCount(0x10000), 2)
        self.assertEqual(Character.charCount(0xFFFF), 1)

    def test_digit(self):
        self.assertEqual(Character.digit('A', 16), 10)
        self.assertEqual(Character.digit('1', 10), 1)

    def test_forDigit(self):
        self.assertEqual(Character.forDigit(10, 16), 'a')  # 10 in base 16 is 'a'
        self.assertEqual(Character.forDigit(1, 10), '1')  # 1 in base 10 is '1'
        self.assertEqual(Character.forDigit(36, 37), '\0')  # Invalid digit/radix returns '\0'

    def test_isSurrogate(self):
        self.assertTrue(Character.isSurrogate('\uD800'))
        self.assertFalse(Character.isSurrogate('a'))

    def test_highSurrogate(self):
        self.assertEqual(Character.highSurrogate(0x10400), '\uD801')

    def test_lowSurrogate(self):
        self.assertEqual(Character.lowSurrogate(0x10400), '\uDC00')

    def test_Subset(self):
        subset = Character.Subset('example')
        self.assertEqual(subset.name, 'example')

    def test_UnicodeBlock(self):
        block = Character.UnicodeBlock('exampleBlock')
        self.assertEqual(block.name, 'exampleBlock')

    def test_UnicodeScript(self):
        script = Character.UnicodeScript('exampleScript')
        self.assertEqual(script.name, 'exampleScript')

if __name__ == '__main__':
    unittest.main()


