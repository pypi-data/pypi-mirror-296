# import unittest
#
# from jstring.stringbuffer import CharSequence
#
#
# class TestCharSequence(unittest.TestCase):
#
#     def test_subSequence(self):
#         cs = CharSequence("Hello World")
#         sub_seq = cs.subSequence(6, 11)
#         self.assertEqual(sub_seq.toString(), "World")
#
#     def test_length(self):
#         cs = CharSequence("Hello")
#         self.assertEqual(cs.length(), 5)
#
#     def test_charAt(self):
#         cs = CharSequence("Hello")
#         self.assertEqual(cs.charAt(1), "e")
#
# if __name__ == '__main__':
#     unittest.main()
