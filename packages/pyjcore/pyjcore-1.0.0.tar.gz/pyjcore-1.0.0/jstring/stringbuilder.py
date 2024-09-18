class StringBuilder:
    """
    A mutable sequence of characters, similar to Java's StringBuilder.

    This class provides a way to build and manipulate strings more efficiently than using Python's built-in strings,
    which are immutable. It supports various operations to modify the contents, such as appending, inserting,
    deleting, and replacing characters.

    Attributes:
        _internal_capacity: The current capacity of the builder.
        data: A list of characters representing the current content of the builder.

    Methods:
        __str__: Returns the string representation of the current content.
        append: Appends the string representation of the given object to the builder.
        capacity: Returns the current capacity of the builder.
        charAt: Returns the character at the specified index.
        codePointAt: Returns the Unicode code point of the character at the specified index.
        codePointBefore: Returns the Unicode code point of the character before the specified index.
        codePointCount: Returns the number of Unicode code points in the specified text range.
        delete: Removes the characters in the specified range.
        deleteCharAt: Removes the character at the specified index.
        ensureCapacity: Ensures that the builder's capacity is at least the specified minimum.
        getChars: Copies characters from the builder into a specified destination list.
        indexOf: Finds the index of the first occurrence of a specified substring.
        insert: Inserts the string representation of the given object at the specified offset.
        lastIndexOf: Finds the index of the last occurrence of a specified substring.
        length: Returns the length of the current content.
        offsetByCodePoints: Calculates the offset of a position by a specified number of code points.
        replace: Replaces the characters in the specified range with a new string.
        reverse: Reverses the characters in the builder.
        setCharAt: Sets the character at the specified index.
        setLength: Sets the length of the builder's content, truncating or padding with null characters as needed.
        subSequence: Returns a new string that is a subsequence of the builder's content.
        substring: Returns a substring of the builder's content.
        toString: Returns the string representation of the current content.
        trimToSize: Adjusts the builder's capacity to match its current size.
    """

    def __init__(self, initial_data=None, capacity=16):
        """
        Initializes a StringBuilder with optional initial data and capacity.

        :param initial_data: Initial content for the builder, which can be a string, list, tuple, or an integer
                              representing the initial capacity.
        :param capacity: The initial capacity of the builder.
        """
        self._internal_capacity = capacity
        if isinstance(initial_data, int):
            self._internal_capacity = initial_data
            self.data = []
        elif isinstance(initial_data, str):
            self.data = list(initial_data)
            self._internal_capacity = max(self._internal_capacity, len(self.data))
        elif isinstance(initial_data, (list, tuple)):
            self.data = list(initial_data)
            self._internal_capacity = max(self._internal_capacity, len(self.data))
        elif initial_data is None:
            self.data = []
        else:
            raise TypeError("Unsupported type for initial_data")

    def __str__(self):
        """
        Returns the string representation of the current content of the builder.

        :return: The current content as a string.
        """
        return ''.join(self.data)

    def append(self, obj):
        """
        Appends the string representation of the given object to the builder.

        :param obj: The object to append. Supported types include bool, str, int, float, list, tuple, and StringBuilder.
        :return: The current StringBuilder instance.
        :raises TypeError: If the object is of an unsupported type.
        """
        if isinstance(obj, bool):
            self.data.append("true" if obj else "false")
        elif isinstance(obj, (str, int, float, list, tuple)):
            self.data.extend(str(obj))
        elif isinstance(obj, StringBuilder):
            self.data.extend(str(obj))
        else:
            raise TypeError("Unsupported type for append")
        return self

    def capacity(self):
        """
        Returns the current capacity of the builder.

        :return: The internal capacity of the builder.
        """
        return self._internal_capacity

    def charAt(self, index):
        """
        Returns the character at the specified index.

        :param index: The index of the character to return.
        :return: The character at the specified index.
        """
        return self.data[index]

    def codePointAt(self, index):
        """
        Returns the Unicode code point of the character at the specified index.

        :param index: The index of the character.
        :return: The Unicode code point of the character.
        """
        return ord(self.data[index])

    def codePointBefore(self, index):
        """
        Returns the Unicode code point of the character before the specified index.

        :param index: The index of the character after the one to return.
        :return: The Unicode code point of the preceding character.
        """
        return ord(self.data[index - 1])

    def codePointCount(self, beginIndex, endIndex):
        """
        Returns the number of Unicode code points in the specified text range.

        :param beginIndex: The beginning index (inclusive).
        :param endIndex: The ending index (exclusive).
        :return: The number of Unicode code points in the range.
        """
        return sum(1 for _ in range(beginIndex, endIndex))

    def delete(self, start, end):
        """
        Removes the characters in the specified range from the builder.

        :param start: The starting index (inclusive).
        :param end: The ending index (exclusive).
        :return: The current StringBuilder instance.
        """
        del self.data[start:end]
        return self

    def deleteCharAt(self, index):
        """
        Removes the character at the specified index.

        :param index: The index of the character to remove.
        :return: The current StringBuilder instance.
        """
        del self.data[index]
        return self

    def ensureCapacity(self, minimumCapacity):
        """
        Ensures that the builder's capacity is at least the specified minimum.

        :param minimumCapacity: The minimum capacity to ensure.
        """
        if self._internal_capacity < minimumCapacity:
            self._internal_capacity = minimumCapacity

    def getChars(self, srcBegin, srcEnd, dst, dstBegin):
        """
        Copies characters from the builder into a specified destination list.

        :param srcBegin: The starting index of the source range (inclusive).
        :param srcEnd: The ending index of the source range (exclusive).
        :param dst: The destination list to copy characters into.
        :param dstBegin: The starting index in the destination list.
        """
        dst[dstBegin:dstBegin + (srcEnd - srcBegin)] = self.data[srcBegin:srcEnd]

    def indexOf(self, jstr, fromIndex=0):
        """
        Finds the index of the first occurrence of a specified substring.

        :param jstr: The substring to find.
        :param fromIndex: The index to start searching from.
        :return: The index of the first occurrence of the substring, or -1 if not found.
        """
        try:
            return ''.join(self.data).index(jstr, fromIndex)
        except ValueError:
            return -1

    def insert(self, offset, obj):
        """
        Inserts the string representation of the given object at the specified offset.

        :param offset: The index at which to insert.
        :param obj: The object to insert.
        :return: The current StringBuilder instance.
        """
        self.data[offset:offset] = list(str(obj))
        return self

    def lastIndexOf(self, jstr, fromIndex=None):
        """
        Finds the index of the last occurrence of a specified substring.

        :param jstr: The substring to find.
        :param fromIndex: The index to start searching backwards from (optional).
        :return: The index of the last occurrence of the substring, or -1 if not found.
        """
        if fromIndex is None:
            return ''.join(self.data).rindex(jstr)
        return ''.join(self.data).rindex(jstr, 0, fromIndex + 1)

    def length(self):
        """
        Returns the length of the current content.

        :return: The length of the content.
        """
        return len(self.data)

    def offsetByCodePoints(self, index, codePointOffset):
        """
        Calculates the offset of a position by a specified number of code points.

        :param index: The starting index.
        :param codePointOffset: The number of code points to offset by.
        :return: The new index after offsetting.
        """
        return index + codePointOffset

    def replace(self, start, end, jstr):
        """
        Replaces the characters in the specified range with a new string.

        :param start: The starting index (inclusive).
        :param end: The ending index (exclusive).
        :param jstr: The string to replace the current content with.
        :return: The current StringBuilder instance.
        """
        self.data[start:end] = list(jstr)
        return self

    def reverse(self):
        """
        Reverses the characters in the builder.

        :return: The current StringBuilder instance.
        """
        self.data.reverse()
        return self

    def setCharAt(self, index, ch):
        """
        Sets the character at the specified index.

        :param index: The index at which to set the character.
        :param ch: The character to set.
        """
        self.data[index] = ch

    def setLength(self, newLength):
        """
        Sets the length of the builder's content. If the new length is less than the current length,
        the content is truncated. If the new length is greater, the content is padded with null characters.

        :param newLength: The new length to set.
        """
        if newLength < len(self.data):
            del self.data[newLength:]
        else:
            self.data.extend(['\0'] * (newLength - len(self.data)))

    def subSequence(self, start, end):
        """
        Returns a new string that is a subsequence of the builder's content.

        :param start: The starting index (inclusive).
        :param end: The ending index (exclusive).
        :return: A new string that is a subsequence of the content.
        """
        return ''.join(self.data[start:end])

    def substring(self, start, end=None):
        """
        Returns a substring of the builder's content.

        :param start: The starting index (inclusive).
        :param end: The ending index (exclusive), or None to include the rest of the content.
        :return: A new string that is a substring of the content.
        """
        return ''.join(self.data[start:end])

    def toString(self):
        """
        Returns the string representation of the current content.

        :return: The current content as a string.
        """
        return ''.join(self.data)

    def trimToSize(self):
        """
        Adjusts the builder's capacity to match its current size.

        This method is used to minimize the internal capacity to the length of the current content.
        """
        self._internal_capacity = len(self.data)
