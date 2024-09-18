import re

class String:
    """
    A class representing a sequence of characters, providing various string manipulation methods.
    Supports initialization from different types including bytes, strings, lists of strings, and
    instances of StringBuilder or StringBuffer.

    Attributes:
        _value: The internal string value.
    """

    def __init__(self, *args):
        """
        Initializes the String object based on the provided arguments.

        :param args: Variable length arguments to initialize the string. Can be:
                     - No arguments: initializes to an empty string.
                     - One argument: can be a bytes object, a string, a list of strings,
                       or an instance of StringBuilder or StringBuffer.
                     - Two arguments: if the first is bytes, the second can be a charset or
                       a tuple specifying a subarray.
                     - Three arguments: used to initialize from a bytes object with a range.
        """
        if len(args) == 0:
            self._value = ""
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, bytes):
                self._value = arg.decode()  # Decode bytes using default UTF-8 charset
            elif isinstance(arg, str):
                self._value = arg
            elif isinstance(arg, list) and all(isinstance(i, str) for i in arg):
                self._value = ''.join(arg)  # Join list of strings
            else:
                # Import here to avoid circular dependency issues
                from .stringbuilder import StringBuilder
                from .stringbuffer import StringBuffer

                if isinstance(arg, StringBuilder):  # Handle StringBuilder instance
                    self._value = str(arg)
                elif isinstance(arg, StringBuffer):  # Handle StringBuffer instance
                    self._value = str(arg)
                else:
                    raise TypeError("Unsupported argument type")
        elif len(args) == 2:
            arg1, arg2 = args
            if isinstance(arg1, bytes):
                if isinstance(arg2, str):
                    self._value = arg1.decode(arg2)  # Decode bytes using specified charset
                elif isinstance(arg2, tuple) and len(arg2) == 2 and isinstance(arg2[0], int) and isinstance(arg2[1], int):
                    self._value = arg1[arg2[0]:arg2[1]].decode()  # Decode subarray
                else:
                    raise TypeError("Invalid second argument type")
            elif isinstance(arg1, list) and isinstance(arg2, int):
                if isinstance(arg1[0], str):
                    self._value = ''.join(arg1[arg2:])  # Join list from specified index
                else:
                    raise TypeError("Invalid argument types")
            else:
                raise TypeError("Unsupported argument types")
        elif len(args) == 3:
            arg1, arg2, arg3 = args
            if isinstance(arg1, bytes) and isinstance(arg2, int) and isinstance(arg3, int):
                self._value = arg1[arg2:arg2 + arg3].decode()  # Decode specified subarray
            else:
                raise TypeError("Unsupported argument types")
        else:
            raise TypeError("Too many arguments")

    def __str__(self):
        """
        Returns the string representation of the current value.

        :return: The internal string value.
        """
        return self._value

    def __repr__(self):
        """
        Returns a string representation that can be used to recreate the object.

        :return: A string representing the object.
        """
        return f"String('{self._value}')"

    def __eq__(self, other):
        """
        Checks equality between this String and another object.

        :param other: The object to compare with.
        :return: True if equal, otherwise False.
        """
        if isinstance(other, String):
            return self._value == other._value
        elif isinstance(other, str):
            return self._value == other
        return False

    def __add__(self, other):
        """
        Concatenates this String with another String or a regular string.

        :param other: The string or String object to concatenate.
        :return: A new String object representing the concatenated result.
        :raises TypeError: If the other object is not a string or String.
        """
        if isinstance(other, String):
            return String(self._value + other._value)
        elif isinstance(other, str):
            return String(self._value + other)
        else:
            raise TypeError("Can only concatenate String or str objects")

    def __len__(self):
        """
        Returns the length of the string.

        :return: The length of the string.
        """
        return len(self._value)

    def __getitem__(self, key):
        """
        Returns a new String representing the substring specified by the key.

        :param key: The index or slice to retrieve.
        :return: A new String object containing the substring.
        """
        return String(self._value[key])

    @staticmethod
    def from_char_array(char_array, offset=0, count=None):
        """
        Creates a String from a list of characters.

        :param char_array: The list of characters.
        :param offset: The starting index.
        :param count: The number of characters to use.
        :return: A new String object.
        """
        if count is None:
            count = len(char_array) - offset
        return String(''.join(char_array[offset:offset + count]))

    @staticmethod
    def from_code_points(code_points, offset=0, count=None):
        """
        Creates a String from a list of Unicode code points.

        :param code_points: The list of code points.
        :param offset: The starting index.
        :param count: The number of code points to use.
        :return: A new String object.
        """
        if count is None:
            count = len(code_points) - offset
        return String(''.join(chr(cp) for cp in code_points[offset:offset + count]))

    @staticmethod
    def from_string_buffer(buffer):
        """
        Creates a String from a StringBuffer object.

        :param buffer: The StringBuffer instance.
        :return: A new String object.
        """
        return String(str(buffer))

    @staticmethod
    def from_string_builder(builder):
        """
        Creates a String from a StringBuilder object.

        :param builder: The StringBuilder instance.
        :return: A new String object.
        """
        return String(str(builder))

    def toString(self):
        """
        Returns the string representation of the current value.

        :return: The internal string value.
        """
        return self.__str__()

    def charAt(self, index):
        """
        Returns the character at the specified index.

        :param index: The index of the character to return.
        :return: The character at the specified index.
        :raises IndexError: If the index is out of range.
        """
        if index < 0 or index >= len(self._value):
            raise IndexError("String index out of range")
        return self._value[index]

    def codePointAt(self, index):
        """
        Returns the Unicode code point of the character at the specified index.

        :param index: The index of the character.
        :return: The Unicode code point.
        :raises IndexError: If the index is out of range.
        """
        if index < 0 or index >= len(self._value):
            raise IndexError("String index out of range")
        return ord(self._value[index])

    def codePointBefore(self, index):
        """
        Returns the Unicode code point of the character before the specified index.

        :param index: The index after the character.
        :return: The Unicode code point of the previous character.
        :raises IndexError: If the index is out of range.
        """
        if index <= 0 or index > len(self._value):
            raise IndexError("String index out of range")
        return ord(self._value[index - 1])

    def codePointCount(self, beginIndex, endIndex):
        """
        Returns the number of Unicode code points in the specified text range.

        :param beginIndex: The starting index (inclusive).
        :param endIndex: The ending index (exclusive).
        :return: The number of code points in the range.
        """
        return len(self._value[beginIndex:endIndex].encode('utf-8'))

    def compareTo(self, another_string):
        """
        Compares this string with another string lexicographically.

        :param another_string: The string to compare with.
        :return: A negative integer, zero, or a positive integer as this string is less than,
                 equal to, or greater than the specified string.
        """
        return (self._value > another_string._value) - (self._value < another_string._value)

    def compareToIgnoreCase(self, another_string):
        """
        Compares this string with another string lexicographically, ignoring case.

        :param another_string: The string to compare with.
        :return: A negative integer, zero, or a positive integer as this string is less than,
                 equal to, or greater than the specified string, ignoring case considerations.
        """
        return (self._value.lower() > another_string.lower()) - (self._value.lower() < another_string.lower())

    def concat(self, s):
        """
        Concatenates the specified string to the end of this string.

        :param s: The string to concatenate.
        :return: A new String object representing the concatenated result.
        """
        return String(self._value + s._value)

    def contains(self, s):
        """
        Checks if the current string contains the specified substring.

        :param s: The substring to search for.
        :return: True if the substring is found, otherwise False.
        """
        return s in self._value

    def __setattr__(self, __name, __value):
        """
        Allows setting attributes, but restricts modification of the internal value.

        :param __name: The attribute name.
        :param __value: The attribute value.
        """
        super().__setattr__(__name, __value)

    def contentEquals(self, cs):
        """
        Compares this string to the specified CharSequence.

        :param cs: The CharSequence to compare with.
        :return: True if the CharSequence is equal to this string, otherwise False.
        """
        return self._value == str(cs)

    def contentEqualsBuffer(self, sb):
        """
        Compares this string to the specified StringBuffer.

        :param sb: The StringBuffer to compare with.
        :return: True if the StringBuffer is equal to this string, otherwise False.
        """
        return self._value == sb

    @staticmethod
    def copyValueOf(data, offset=0, count=None):
        """
        Returns a String that represents the characters of the specified character array.

        :param data: The character array.
        :param offset: The starting index.
        :param count: The number of characters to use.
        :return: A new String object.
        """
        return String(''.join(data[offset:offset+count]))

    def endsWith(self, suffix):
        """
        Checks if the current string ends with the specified suffix.

        :param suffix: The suffix to check.
        :return: True if the string ends with the suffix, otherwise False.
        """
        return self._value.endswith(suffix)

    def equals(self, anObject):
        """
        Compares this string to the specified object for equality.

        :param anObject: The object to compare with.
        :return: True if the object is equal to this string, otherwise False.
        """
        return self._value == str(anObject)

    def equalsIgnoreCase(self, another_string):
        """
        Compares this string to another string, ignoring case considerations.

        :param another_string: The string to compare with.
        :return: True if the strings are equal, ignoring case, otherwise False.
        """
        return self._value.lower() == another_string.lower()

    @staticmethod
    def format(*args):
        """
        Returns a formatted string using the specified format string and arguments.

        :param args: The format string and arguments for formatting.
        :return: A new String object representing the formatted result.
        :raises TypeError: If the arguments are not valid for formatting.
        """
        if len(args) == 1:
            raise TypeError("format() missing required positional arguments")
        elif len(args) == 2 and isinstance(args[0], str):
            format_string = args[0]
            format_args = args[1:]
            formatted_str = format_string.format(*format_args)
        elif len(args) > 2 and isinstance(args[0], (str, type(None))):
            format_string = args[1]
            format_args = args[2:]
            formatted_str = format_string.format(*format_args)
            print(f"Formatted locale string inside format method: {formatted_str}")  # Debugging line
        else:
            raise TypeError("Invalid arguments provided to format method")

        return String(formatted_str)

    def getBytes(self):
        """
        Encodes the string into bytes using the default charset (UTF-8).

        :return: The byte representation of the string.
        """
        return self._value.encode()

    def getBytesCharset(self, charset):
        """
        Encodes the string into bytes using the specified charset.

        :param charset: The charset to use for encoding.
        :return: The byte representation of the string.
        """
        return self._value.encode(charset)

    def getChars(self, src_begin, src_end, dst, dst_begin):
        """
        Copies characters from the specified range into the destination list.

        :param src_begin: The starting index of the source range.
        :param src_end: The ending index of the source range.
        :param dst: The destination list.
        :param dst_begin: The starting index in the destination list.
        """
        dst[dst_begin:dst_begin + (src_end - src_begin)] = list(self._value[src_begin:src_end])

    def hashCode(self):
        """
        Returns a hash code for this string.

        :return: The hash code of the string.
        """
        return hash(self._value)

    def indexOf(self, ch, from_index=0):
        """
        Returns the index of the first occurrence of the specified character.

        :param ch: The character to search for.
        :param from_index: The index to start the search from.
        :return: The index of the first occurrence, or -1 if not found.
        """
        return self._value.find(ch, from_index)

    def indexOfSubstring(self, s, from_index=0):
        """
        Returns the index of the first occurrence of the specified substring.

        :param s: The substring to search for.
        :param from_index: The index to start the search from.
        :return: The index of the first occurrence, or -1 if not found.
        """
        return self._value.find(s, from_index)

    def intern(self):
        """
        Returns the interned string. In Python, this is the same as the original string.

        :return: The interned string.
        """
        return self

    def isEmpty(self):
        """
        Checks if the string is empty.

        :return: True if the string is empty, otherwise False.
        """
        return len(self._value) == 0

    @staticmethod
    def join(delimiter, *elements):
        """
        Joins the specified elements into a single string, separated by the specified delimiter.

        :param delimiter: The delimiter to use.
        :param elements: The elements to join.
        :return: A new String object representing the joined result.
        """
        return String(delimiter.join(str(e) for e in elements))

    def lastIndexOf(self, ch, from_index=None):
        """
        Returns the index of the last occurrence of the specified character.

        :param ch: The character to search for.
        :param from_index: The index to start the search from, or None to search the entire string.
        :return: The index of the last occurrence, or -1 if not found.
        """
        if from_index is None:
            return self._value.rfind(chr(ch))
        return self._value.rfind(chr(ch), 0, from_index)

    def lastIndexOfSubstring(self, another_string, from_index=None):
        """
        Returns the index of the last occurrence of the specified substring.

        :param another_string: The substring to search for.
        :param from_index: The index to start the search from, or None to search the entire string.
        :return: The index of the last occurrence, or -1 if not found.
        """
        if from_index is None:
            return self._value.rfind(another_string)
        return self._value.rfind(another_string, 0, from_index)

    def length(self):
        """
        Returns the length of the string.

        :return: The length of the string.
        """
        return len(self._value)

    def matches(self, regex):
        """
        Checks if the string matches the specified regular expression.

        :param regex: The regular expression to match.
        :return: True if the string matches the regex, otherwise False.
        """
        return re.fullmatch(regex, self._value) is not None

    def offsetByCodePoints(self, index, codePointOffset):
        """
        Calculates the index offset by the specified number of code points.

        :param index: The starting index.
        :param codePointOffset: The number of code points to offset by.
        :return: The new index.
        """
        return index + codePointOffset

    def regionMatches(self, ignoreCase, toffset, other, ooffset, length):
        """
        Compares a substring of this string with a substring of another string.

        :param ignoreCase: Whether to ignore case during the comparison.
        :param toffset: The starting index of the substring in this string.
        :param other: The other string to compare with.
        :param ooffset: The starting index of the substring in the other string.
        :param length: The length of the substrings to compare.
        :return: True if the substrings are equal, otherwise False.
        """
        if ignoreCase:
            return self._value[toffset:toffset+length].lower() == other._value[ooffset:ooffset+length].lower()
        return self._value[toffset:toffset+length] == other._value[ooffset:ooffset+length]

    def replace(self, oldChar, newChar):
        """
        Replaces occurrences of the specified character with a new character.

        :param oldChar: The character to be replaced.
        :param newChar: The new character to replace with.
        :return: A new String object with the replacements.
        """
        return String(self._value.replace(oldChar, newChar))

    def replaceSequence(self, target, replacement):
        """
        Replaces occurrences of the specified substring with a new substring.

        :param target: The substring to be replaced.
        :param replacement: The new substring to replace with.
        :return: A new String object with the replacements.
        """
        return String(self._value.replace(target, replacement))

    def replaceAll(self, regex, replacement):
        """
        Replaces all occurrences of the substrings that match the specified regular expression.

        :param regex: The regular expression to match.
        :param replacement: The new substring to replace with.
        :return: A new String object with the replacements.
        """
        return String(re.sub(regex, replacement, self._value))

    def replaceFirst(self, regex, replacement):
        """
        Replaces the first occurrence of the substring that matches the specified regular expression.

        :param regex: The regular expression to match.
        :param replacement: The new substring to replace with.
        :return: A new String object with the replacement.
        """
        return String(re.sub(regex, replacement, self._value, 1))

    def split(self, delimiter=" ", limit=-1):
        """
        Splits the string into a list of substrings using the specified delimiter.

        :param delimiter: The delimiter to use for splitting.
        :param limit: The maximum number of substrings to return. If -1, there is no limit.
        :return: A list of String objects representing the substrings.
        """
        if limit == -1:
            split_result = self._value.split(delimiter)
        else:
            split_result = self._value.split(delimiter, limit)

        return [String(s) for s in split_result]

    def startsWith(self, prefix, toffset=0):
        """
        Checks if the string starts with the specified prefix.

        :param prefix: The prefix to check.
        :param toffset: The index to start the search from.
        :return: True if the string starts with the prefix, otherwise False.
        """
        return self._value.startswith(prefix, toffset)

    def subSequence(self, beginIndex, endIndex):
        """
        Returns a new String object that is a subsequence of this string.

        :param beginIndex: The starting index of the subsequence.
        :param endIndex: The ending index of the subsequence.
        :return: A new String object representing the subsequence.
        """
        return String(self._value[beginIndex:endIndex])

    def substring(self, beginIndex, endIndex=None):
        """
        Returns a new String object that is a substring of this string.

        :param beginIndex: The starting index of the substring.
        :param endIndex: The ending index of the substring. If None, the substring extends to the end of the string.
        :return: A new String object representing the substring.
        """
        if endIndex is None:
            return String(self._value[beginIndex:])
        return String(self._value[beginIndex:endIndex])

    def toCharArray(self):
        """
        Converts the string to a list of characters.

        :return: A list of characters.
        """
        return list(self._value)

    def toLowerCase(self):
        """
        Converts the string to lowercase.

        :return: A new String object with the lowercase representation.
        """
        return String(self._value.lower())

    def toUpperCase(self):
        """
        Converts the string to uppercase.

        :return: A new String object with the uppercase representation.
        """
        return String(self._value.upper())

    def trim(self):
        """
        Removes leading and trailing whitespace from the string.

        :return: A new String object with the whitespace removed.
        """
        return String(self._value.strip())

    @staticmethod
    def valueOf(value):
        """
        Returns a String object representing the specified value.

        :param value: The value to convert to a string.
        :return: A new String object.
        :raises TypeError: If the value is of an unsupported type.
        """
        if isinstance(value, (bool, int, float)):
            return String(str(value))
        elif isinstance(value, (str, list)):
            return String(value)
        else:
            raise TypeError("Unsupported type")
