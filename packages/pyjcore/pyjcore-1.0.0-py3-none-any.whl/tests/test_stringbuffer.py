import unittest

from jstring import StringBuffer


class TestStringBuffer(unittest.TestCase):

    def test_constructor_empty(self):
        sb = StringBuffer()
        self.assertEqual(sb.toString(), "")
        self.assertEqual(sb.capacity(), 16)

    def test_constructor_with_string(self):
        sb = StringBuffer("Hello")
        self.assertEqual(sb.toString(), "Hello")
        self.assertEqual(sb.length(), 5)

    def test_append(self):
        sb = StringBuffer("Hello")
        sb.append(" World")
        self.assertEqual(sb.toString(), "Hello World")

    def test_charAt(self):
        sb = StringBuffer("Hello")
        self.assertEqual(sb.charAt(1), "e")

    def test_ensureCapacity(self):
        sb = StringBuffer("Hello")
        sb.ensureCapacity(50)
        self.assertEqual(sb.capacity(), 50)

    def test_trimToSize(self):
        sb = StringBuffer("Hello World")
        sb.trimToSize()
        self.assertEqual(sb.capacity(), 11)

    def test_delete(self):
        sb = StringBuffer("Hello World")
        sb.delete(5, 11)
        self.assertEqual(sb.toString(), "Hello")

    def test_deleteCharAt(self):
        sb = StringBuffer("Hello")
        sb.deleteCharAt(1)
        self.assertEqual(sb.toString(), "Hllo")

    def test_indexOf(self):
        sb = StringBuffer("Hello World")
        self.assertEqual(sb.indexOf("World"), 6)

    def test_lastIndexOf(self):
        sb = StringBuffer("Hello World World")
        self.assertEqual(sb.lastIndexOf("World"), 12)

    def test_insert(self):
        sb = StringBuffer("Hello World")
        sb.insert(6, "Beautiful ")
        self.assertEqual(sb.toString(), "Hello Beautiful World")

    def test_setCharAt(self):
        sb = StringBuffer("Hello")
        sb.setCharAt(1, "a")
        self.assertEqual(sb.toString(), "Hallo")

    def test_setLength(self):
        sb = StringBuffer("Hello")
        sb.setLength(3)
        self.assertEqual(sb.toString(), "Hel")
        sb.setLength(5)
        self.assertEqual(sb.toString(), "Hel\0\0")  # or "Hel  " if you use spaces

    def test_reverse(self):
        sb = StringBuffer("Hello")
        sb.reverse()
        self.assertEqual(sb.toString(), "olleH")

    def test_replace(self):
        sb = StringBuffer("Hello World")
        sb.replace(6, 11, "Python")
        self.assertEqual(sb.toString(), "Hello Python")
