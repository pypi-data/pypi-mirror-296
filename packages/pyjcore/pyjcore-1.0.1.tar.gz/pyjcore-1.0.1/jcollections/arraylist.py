from collections.abc import Iterator
from jcollections import Predicate
from jcollections.collection import Collection
from jcollections.list import List

class ArrayList(List):
    """
    A concrete implementation of the List interface using a resizable array.
    Provides dynamic resizing and positional access to elements.
    """

    def __init__(self, initial_capacity=5, c=None):
        """
        Initializes the ArrayList with an optional initial capacity or from an existing collection.
        :param initial_capacity: Initial capacity of the array (default: 5).
        :param c: Optional collection to initialize the ArrayList with.
        """
        if isinstance(initial_capacity, int):
            self.__data = [None] * initial_capacity
            self.__size = 0
            self.__capacity = initial_capacity
        elif isinstance(initial_capacity, Collection):
            self.__data = list(initial_capacity)
            self.__size = len(self.__data)
            self.__capacity = self.__size
        else:
            raise TypeError("Invalid type for initial_capacity. Must be int or Collection.")

        if c:
            self.addAll(c)

    def ensureCapacity(self, minimumCapacity=None):
        """
        Ensures that the ArrayList has enough capacity to hold additional elements.
        If minimumCapacity is not provided, the capacity is doubled.
        :param minimumCapacity: The minimum required capacity.
        """
        if minimumCapacity is None:
            minimumCapacity = self.__capacity * 2

        if self.__capacity < minimumCapacity:
            self.__resize(minimumCapacity)

    def add(self, *args):
        """
        Adds an element at the end of the list or at the specified index.
        :param args: Can be a single element or (index, element).
        """
        if len(args) == 1:
            element = args[0]
            if self.__size == self.__capacity:
                self.__resize(self.__capacity * 2)

            self.__data[self.__size] = element
            self.__size += 1
            return True
        elif len(args) == 2:
            index, element = args
            if index < 0 or index > self.__size:
                raise IndexError("Index out of bounds")
            if self.__size >= self.__capacity:
                self.__resize(self.__capacity * 2)
            for i in range(self.__size, index, -1):
                self.__data[i] = self.__data[i - 1]
            self.__data[index] = element
            self.__size += 1
            return True
        else:
            raise TypeError("Invalid number of arguments")

    def addAll(self, *args):
        """
        Adds all elements from a collection at the end or at the specified index.
        :param args: Can be a collection or (index, collection).
        """
        if len(args) == 1:
            collection = args[0]
            if self.__size + len(collection) > self.__capacity:
                self.ensureCapacity(self.__size + len(collection))
            for element in collection:
                self.add(element)
            return True
        elif len(args) == 2:
            index, collection = args
            if index < 0 or index > self.__size:
                raise IndexError("Index out of bounds")
            if self.__size + len(collection) > self.__capacity:
                self.ensureCapacity(self.__size + len(collection))
            for i, element in enumerate(collection):
                self.add(index + i, element)
            return True
        else:
            raise TypeError("Invalid number of arguments")

    def __resize(self, new_capacity):
        """
        Resizes the internal array to the specified new capacity.
        :param new_capacity: The new capacity of the array.
        """
        if new_capacity > self.__capacity:
            new__data = [None] * new_capacity
            for i in range(self.__size):
                new__data[i] = self.__data[i]
            self.__data = new__data
            self.__capacity = new_capacity

    def __iter__(self) -> Iterator:
        """
        Returns an iterator over the elements in the list.
        """
        return iter(self.__data[:self.__size])

    def __setattr__(self, name, value):
        """
        Sets an attribute on the ArrayList object. Overrides the default __setattr__ to handle internal attributes.
        :param name: The name of the attribute.
        :param value: The value to set.
        """
        if name == '__data':
            super().__setattr__(name, value)
        else:
            super().__setattr__(name, value)

    def clear(self):
        """
        Removes all elements from the list.
        """
        self.__data = [None] * self.__capacity
        self.__size = 0

    def contains(self, o):
        """
        Checks if the specified element is present in the list.
        :param o: The element to check for.
        :return: True if the element is present, otherwise False.
        """
        return o in self.__data[:self.__size]

    def containsAll(self, c):
        """
        Checks if the list contains all elements from the specified collection.
        :param c: The collection of elements to check.
        :return: True if all elements are present, otherwise False.
        """
        return all(self.contains(element) for element in c)

    def equals(self, o):
        """
        Compares this list with another object for equality.
        :param o: The object to compare with.
        :return: True if the objects are equal, otherwise False.
        """
        if isinstance(o, ArrayList):
            return self.__data[:self.__size] == o.__data[:o.__size]
        return False

    def get(self, index):
        """
        Returns the element at the specified index.
        :param index: The index of the element to return.
        :return: The element at the specified index.
        """
        if index < 0 or index >= self.__size:
            raise IndexError("Index out of bounds")
        return self.__data[index]

    def hashCode(self):
        """
        Returns the hash code of the list.
        """
        return hash(tuple(self.__data[:self.__size]))

    def indexOf(self, o):
        """
        Returns the index of the first occurrence of the specified element, or -1 if not present.
        :param o: The element to search for.
        """
        try:
            return self.__data[:self.__size].index(o)
        except ValueError:
            return -1

    def isEmpty(self):
        """
        Returns True if the list is empty.
        """
        return self.__size == 0

    def iterator(self):
        """
        Returns an iterator over the elements in the list.
        """
        return iter(self.__data[:self.__size])

    def lastIndexOf(self, o):
        """
        Returns the index of the last occurrence of the specified element, or -1 if not present.
        :param o: The element to search for.
        """
        for i in range(self.__size - 1, -1, -1):
            if self.__data[i] == o:
                return i
        return -1

    def listIterator(self, *args):
        """
        Returns a list iterator over the elements in the list.
        :param args: Optional start index for the iterator.
        """
        if len(args) == 0:
            return iter(self.__data[:self.__size])
        elif len(args) == 1:
            index = args[0]
            if index < 0 or index >= self.__size:
                raise IndexError("Index out of bounds")
            return iter(self.__data[index:self.__size])
        else:
            raise TypeError("Invalid number of arguments")

    def remove(self, value_or_index):
        """
        Removes the element at the specified index or the specified value.
        :param value_or_index: Index of the element to remove or the value to remove.
        """
        if isinstance(value_or_index, int):
            index = value_or_index
            if index < 0 or index >= self.size():
                raise IndexError("Index out of bounds")
            removed_element = self.__data[index]
            self._shift_left(index)
            self.__size -= 1
            return removed_element
        else:
            value = value_or_index
            for i in range(self.size()):
                if self.__data[i] == value:
                    self._shift_left(i)
                    self.__size -= 1
                    return True
            return False

    def removeAll(self, c):
        """
        Removes all elements in the collection from the list.
        :param c: The collection of elements to remove.
        """
        removed = False
        for element in c:
            while self.contains(element):
                self.remove(self.indexOf(element))
                removed = True
        return removed

    def _shift_left(self, index):
        """
        Shifts elements to the left after an element has been removed.
        :param index: The index from where to start shifting elements.
        """
        for i in range(index, self.__size - 1):
            self.__data[i] = self.__data[i + 1]
        self.__data[self.__size - 1] = None

    def retainAll(self, c):
        """
        Retains only the elements in the list that are also present in the specified collection.
        :param c: The collection of elements to retain.
        """
        to_remove = [element for element in self.__data[:self.__size] if element not in c]
        return self.removeAll(to_remove)

    def replaceAll(self, operator):
        """
        Replaces each element of this list with the result of applying the operator to that element.
        :param operator: A function to apply to each element.
        """
        for i in range(self.__size):
            self.__data[i] = operator(self.__data[i])

    def set(self, index, element):
        """
        Replaces the element at the specified position in this list with the specified element.
        :param index: The index of the element to replace.
        :param element: The new element.
        :return: The old element at the specified position.
        """
        if index < 0 or index >= self.__size:
            raise IndexError("Index out of bounds")
        old_value = self.__data[index]
        self.__data[index] = element
        return old_value

    def size(self):
        """
        Returns the number of elements in the list.
        """
        return self.__size

    def sort(self, c):
        """
        Sorts the list according to the order induced by the specified comparator.
        :param c: The comparator function used for sorting.
        """
        self.__data[:self.__size] = sorted(self.__data[:self.__size], key=c)

    def spliterator(self):
        """
        Returns a Spliterator over the elements in the list.
        """
        return iter(self.__data[:self.__size])

    def subList(self, fromIndex, toIndex):
        """
        Returns a view of the portion of this list between fromIndex, inclusive, and toIndex, exclusive.
        :param fromIndex: The start index of the sublist.
        :param toIndex: The end index of the sublist.
        """
        if fromIndex < 0 or toIndex > self.__size or fromIndex > toIndex:
            raise IndexError("Index out of bounds")
        sublist = ArrayList()
        sublist.__data = self.__data[fromIndex:toIndex]
        sublist.__size = toIndex - fromIndex
        return sublist

    def toArray(self, *args) -> list:
        """
        Converts the list to an array.
        :param args: Optional argument to specify the type of array elements.
        :return: The array of elements in the list.
        """
        if len(args) == 0:
            return self.__data[:self.__size]
        elif len(args) == 1:
            a_type = args[0]
            if not isinstance(a_type, type):
                raise TypeError("Argument must be a type (e.g., str, int)")
            return [a_type(element) for element in self.__data[:self.__size]]
        else:
            raise TypeError("Invalid number of arguments")

    def parallelStream(self):
        """
        Returns a parallel stream of the list for parallel processing.
        """
        return self.stream()

    def stream(self):
        """
        Returns a sequential stream of the list for processing.
        """
        return iter(self.__data[:self.__size])

    def removeIf(self, predicate: Predicate) -> bool:
        """
        Removes all elements that satisfy the given predicate.
        :param predicate: A function that returns True for elements to be removed.
        :return: True if any elements were removed, otherwise False.
        """
        removed = False
        i = 0
        while i < self.__size:
            if predicate(self.__data[i]):
                self.remove(i)
                removed = True
            else:
                i += 1
        return removed