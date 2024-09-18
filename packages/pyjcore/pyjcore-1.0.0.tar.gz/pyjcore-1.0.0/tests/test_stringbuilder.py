import unittest

from jstring import StringBuilder


class TestStringBuilder(unittest.TestCase):

    def test_initialization(self):
        sb = StringBuilder("Hello")
        self.assertEqual(str(sb), "Hello")
        self.assertEqual(sb.capacity(), 16)

        sb = StringBuilder(10)
        self.assertEqual(sb.capacity(), 10)
        self.assertEqual(str(sb), "")

        sb = StringBuilder()
        self.assertEqual(sb.capacity(), 16)
        self.assertEqual(str(sb), "")

    def test_append(self):
        sb = StringBuilder("Hello")
        sb.append(" World")
        self.assertEqual(str(sb), "Hello World")

        sb.append(123)
        self.assertEqual(str(sb), "Hello World123")

        sb.append(True)
        self.assertEqual(str(sb), "Hello World123true")

    def test_charAt(self):
        sb = StringBuilder("Hello")
        self.assertEqual(sb.charAt(1), "e")

    def test_codePointAt(self):
        sb = StringBuilder("Hello")
        self.assertEqual(sb.codePointAt(1), ord("e"))

    def test_codePointBefore(self):
        sb = StringBuilder("Hello")
        self.assertEqual(sb.codePointBefore(1), ord("H"))

    def test_codePointCount(self):
        sb = StringBuilder("Hello")
        self.assertEqual(sb.codePointCount(1, 4), 3)

    def test_delete(self):
        sb = StringBuilder("Hello World")
        sb.delete(5, 11)
        self.assertEqual(str(sb), "Hello")

    def test_deleteCharAt(self):
        sb = StringBuilder("Hello")
        sb.deleteCharAt(1)
        self.assertEqual(str(sb), "Hllo")

    def test_ensureCapacity(self):
        sb = StringBuilder("Hello")
        sb.ensureCapacity(50)
        self.assertEqual(sb.capacity(), 50)  # Fixed by calling the method

    def test_getChars(self):
        sb = StringBuilder("Hello World")
        dst = [' '] * 5
        sb.getChars(6, 11, dst, 0)
        self.assertEqual(''.join(dst), "World")

    def test_indexOf(self):
        sb = StringBuilder("Hello World")
        self.assertEqual(sb.indexOf("World"), 6)
        self.assertEqual(sb.indexOf("world"), -1)

    def test_insert(self):
        sb = StringBuilder("Hello World")
        sb.insert(6, "Beautiful ")
        self.assertEqual(str(sb), "Hello Beautiful World")

    def test_lastIndexOf(self):
        sb = StringBuilder("Hello Hello Hello")
        self.assertEqual(sb.lastIndexOf("Hello"), 12)
        self.assertEqual(sb.lastIndexOf("Hello", 10), 6)

    def test_length(self):
        sb = StringBuilder("Hello")
        self.assertEqual(sb.length(), 5)

    def test_offsetByCodePoints(self):
        sb = StringBuilder("Hello")
        self.assertEqual(sb.offsetByCodePoints(1, 2), 3)

    def test_replace(self):
        sb = StringBuilder("Hello World")
        sb.replace(6, 11, "Python")
        self.assertEqual(str(sb), "Hello Python")

    def test_reverse(self):
        sb = StringBuilder("Hello")
        sb.reverse()
        self.assertEqual(str(sb), "olleH")

    def test_setCharAt(self):
        sb = StringBuilder("Hello")
        sb.setCharAt(1, 'a')
        self.assertEqual(str(sb), "Hallo")

    def test_setLength(self):
        sb = StringBuilder("Hello")
        sb.setLength(3)
        self.assertEqual(str(sb), "Hel")
        sb.setLength(5)
        self.assertEqual(str(sb), "Hel\0\0")

    def test_subSequence(self):
        sb = StringBuilder("Hello World")
        self.assertEqual(sb.subSequence(6, 11), "World")

    def test_substring(self):
        sb = StringBuilder("Hello World")
        self.assertEqual(sb.substring(6, 11), "World")

    def test_trimToSize(self):
        sb = StringBuilder("Hello World")
        sb.trimToSize()
        self.assertEqual(sb.capacity(), 11)  # Fixed by calling the method

if __name__ == "__main__":
    unittest.main()


