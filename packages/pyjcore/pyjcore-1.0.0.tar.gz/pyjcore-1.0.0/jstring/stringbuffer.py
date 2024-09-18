from jstring import String


class CharSequence:
    """
    An abstract base class representing a sequence of characters.

    This class defines a common interface for character sequences, which can be implemented by various
    classes to provide different ways of handling sequences of characters.

    Methods:
        charAt: Returns the character at the specified index.
        length: Returns the length of the character sequence.
        subSequence: Returns a new CharSequence that is a subsequence of the current sequence.
        toString: Returns the string representation of the character sequence.
    """

    def charAt(self, index):
        """
        Returns the character at the specified index.

        :param index: The index of the character to return.
        :raises NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError

    def length(self):
        """
        Returns the length of the character sequence.

        :return: The length of the sequence.
        :raises NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError

    def subSequence(self, start, end):
        """
        Returns a new CharSequence that is a subsequence of the current sequence.

        :param start: The start index (inclusive) of the subsequence.
        :param end: The end index (exclusive) of the subsequence.
        :return: A new CharSequence that is a subsequence of the current sequence.
        :raises NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError

    def toString(self):
        """
        Returns the string representation of the character sequence.

        :return: The string representation of the sequence.
        :raises NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError

class StringBuffer(CharSequence):
    """
    A mutable sequence of characters, similar to Java's StringBuffer.

    This class provides a way to build and manipulate strings more efficiently than using immutable
    strings. It supports various operations to modify the contents, such as appending, inserting,
    deleting, and replacing characters.

    Attributes:
        value: A list of characters representing the current content of the buffer.

    Methods:
        __str__: Returns the string representation of the current content.
        append: Appends the string representation of the given object to the buffer.
        charAt: Returns the character at the specified index.
        length: Returns the length of the current content.
        subSequence: Returns a new String that is a subsequence of the buffer's content.
        toString: Returns the string representation of the current content.
        ensureCapacity: Ensures that the buffer's capacity is at least the specified minimum.
        trimToSize: Adjusts the buffer's capacity to match its current size by removing unused space.
        capacity: Returns the current capacity of the buffer.
        delete: Removes the characters in the specified range from the buffer.
        deleteCharAt: Removes the character at the specified index.
        indexOf: Finds the index of the first occurrence of a specified substring.
        lastIndexOf: Finds the index of the last occurrence of a specified substring.
        insert: Inserts the string representation of the given object at the specified offset.
        setCharAt: Sets the character at the specified index.
        setLength: Sets the length of the buffer's content, truncating or padding with null characters as needed.
        reverse: Reverses the characters in the buffer.
        replace: Replaces the characters in the specified range with a new string.
    """

    def __init__(self, initial=None):
        """
        Initializes a StringBuffer with optional initial data.

        :param initial: Initial content for the buffer, which can be a string, CharSequence, or integer
                        representing the initial capacity.
        """
        if isinstance(initial, int):
            self.value = [''] * initial
        elif isinstance(initial, CharSequence):
            self.value = list(initial.toString())
        elif isinstance(initial, str):
            self.value = list(initial)
        else:
            self.value = [''] * 16

    def __str__(self):
        """
        Returns the string representation of the current content of the buffer.

        :return: The current content as a string.
        """
        return ''.join(self.value)

    def append(self, obj):
        """
        Appends the string representation of the given object to the buffer.

        :param obj: The object to append. Supported types include CharSequence, str, bool, int, and float.
        :return: The current StringBuffer instance.
        """
        self.value.extend(list(str(obj)))
        return self

    def charAt(self, index):
        """
        Returns the character at the specified index.

        :param index: The index of the character to return.
        :return: The character at the specified index.
        """
        return self.value[index]

    def length(self):
        """
        Returns the length of the current content.

        :return: The length of the content.
        """
        return len(self.value)

    def subSequence(self, start, end):
        """
        Returns a new String that is a subsequence of the buffer's content.

        :param start: The starting index (inclusive) of the subsequence.
        :param end: The ending index (exclusive) of the subsequence.
        :return: A new String that is a subsequence of the content.
        """
        return String(''.join(self.value[start:end]))

    def toString(self):
        """
        Returns the string representation of the current content.

        :return: The current content as a string.
        """
        return ''.join(self.value)

    def ensureCapacity(self, minimumCapacity):
        """
        Ensures that the buffer's capacity is at least the specified minimum.

        :param minimumCapacity: The minimum capacity to ensure.
        """
        currentCapacity = self.capacity()
        if minimumCapacity > currentCapacity:
            self.value.extend([''] * (minimumCapacity - currentCapacity))

    def trimToSize(self):
        """
        Adjusts the buffer's capacity to match its current size by removing unused space.
        """
        self.value = [char for char in self.value if char]

    def capacity(self):
        """
        Returns the current capacity of the buffer.

        :return: The current capacity of the buffer.
        """
        return len(self.value)

    def delete(self, start, end):
        """
        Removes the characters in the specified range from the buffer.

        :param start: The starting index (inclusive).
        :param end: The ending index (exclusive).
        :return: The current StringBuffer instance.
        """
        del self.value[start:end]
        return self

    def deleteCharAt(self, index):
        """
        Removes the character at the specified index.

        :param index: The index of the character to remove.
        :return: The current StringBuffer instance.
        """
        del self.value[index]
        return self

    def indexOf(self, string, fromIndex=0):
        """
        Finds the index of the first occurrence of a specified substring.

        :param string: The substring to find.
        :param fromIndex: The index to start searching from.
        :return: The index of the first occurrence of the substring, or -1 if not found.
        """
        joined_value = ''.join(self.value)
        return joined_value.find(string, fromIndex)

    def lastIndexOf(self, string, fromIndex=None):
        """
        Finds the index of the last occurrence of a specified substring.

        :param string: The substring to find.
        :param fromIndex: The index to start searching backwards from (optional).
        :return: The index of the last occurrence of the substring, or -1 if not found.
        """
        joined_value = ''.join(self.value)
        return joined_value.rfind(string, 0, fromIndex)

    def insert(self, offset, obj):
        """
        Inserts the string representation of the given object at the specified offset.

        :param offset: The index at which to insert.
        :param obj: The object to insert. Supported types include CharSequence, str, bool, int, and float.
        :return: The current StringBuffer instance.
        :raises ValueError: If the object type is unsupported.
        """
        if isinstance(obj, CharSequence) or isinstance(obj, str):
            self.value[offset:offset] = list(str(obj))
        elif isinstance(obj, bool):
            self.value[offset:offset] = list(str(obj).lower())
        elif isinstance(obj, (int, float)):
            self.value[offset:offset] = list(str(obj))
        else:
            raise ValueError("Unsupported type for insert")
        return self

    def setCharAt(self, index, ch):
        """
        Sets the character at the specified index.

        :param index: The index at which to set the character.
        :param ch: The character to set.
        """
        self.value[index] = ch

    def setLength(self, newLength):
        """
        Sets the length of the buffer's content. If the new length is less than the current length,
        the content is truncated. If the new length is greater, the content is padded with null characters.

        :param newLength: The new length to set.
        """
        currentLength = self.length()
        if newLength < currentLength:
            del self.value[newLength:]
        elif newLength > currentLength:
            self.value.extend(['\0'] * (newLength - currentLength))

    def reverse(self):
        """
        Reverses the characters in the buffer.

        :return: The current StringBuffer instance.
        """
        self.value.reverse()
        return self

    def replace(self, start, end, str_):
        """
        Replaces the characters in the specified range with a new string.

        :param start: The starting index (inclusive) of the range to replace.
        :param end: The ending index (exclusive) of the range to replace.
        :param str_: The new string to insert.
        :return: The current StringBuffer instance.
        """
        self.value[start:end] = list(str_)
        return self
