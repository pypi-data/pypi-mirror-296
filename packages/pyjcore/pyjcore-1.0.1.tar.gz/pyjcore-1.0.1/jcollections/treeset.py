from bisect import bisect_left, bisect_right
from jcollections.sortedset import SortedSet

class TreeSet(SortedSet):
    """
    Implementation of a TreeSet, a sorted set that maintains elements in ascending order.

    Inherits from:
        - SortedSet: Provides abstract methods for sorted set operations.
    """

    def __init__(self, elements=None, comparator=None):
        """
        Constructs a new, empty TreeSet with optional elements and comparator.

        :param elements: Optional collection of elements to add to the TreeSet at initialization.
        :param comparator: Optional comparator function to define the ordering of elements.
        """
        self._elements = []  # List to hold the elements in sorted order
        self._comparator = comparator

        if elements:
            self.addAll(elements)

    def comparator(self):
        """
        Returns the comparator used to order elements in the set.

        :return: The comparator function, or None if natural ordering is used.
        """
        return self._comparator

    def first(self):
        """
        Returns the first (lowest) element in the TreeSet.

        :return: The first element.
        :raises ValueError: If the TreeSet is empty.
        """
        if not self._elements:
            raise ValueError("TreeSet is empty.")
        return self._elements[0]

    def last(self):
        """
        Returns the last (highest) element in the TreeSet.

        :return: The last element.
        :raises ValueError: If the TreeSet is empty.
        """
        if not self._elements:
            raise ValueError("TreeSet is empty.")
        return self._elements[-1]

    def add(self, e):
        """
        Adds the specified element to the TreeSet.

        :param e: The element to add.
        :return: True if the element was added, False if it was already present.
        """
        idx = bisect_left(self._elements, e)  # Find the insertion point
        if idx == len(self._elements) or self._elements[idx] != e:
            self._elements.insert(idx, e)  # Insert element in sorted order
            return True
        return False

    def addAll(self, collection):
        """
        Adds all elements from the specified collection to the TreeSet.

        :param collection: Collection of elements to add.
        :return: True if any elements were added, False otherwise.
        """
        added = False
        for e in collection:
            added |= self.add(e)
        return added

    def ceiling(self, e):
        """
        Returns the least element greater than or equal to `e`, or None if not found.

        :param e: The element to compare.
        :return: The least element greater than or equal to `e`, or None if not found.
        """
        idx = bisect_left(self._elements, e)
        if idx < len(self._elements):
            return self._elements[idx]
        return None

    def clear(self):
        """
        Removes all elements from the TreeSet.
        """
        self._elements.clear()

    def contains(self, o):
        """
        Checks if the TreeSet contains the specified element.

        :param o: The element to check for.
        :return: True if the element is present, False otherwise.
        """
        idx = bisect_left(self._elements, o)
        return idx < len(self._elements) and self._elements[idx] == o

    def headSet(self, toElement):
        """
        Returns a view of elements strictly less than `toElement`.

        :param toElement: The upper bound (exclusive).
        :return: List of elements less than `toElement`.
        """
        idx = bisect_left(self._elements, toElement)
        return self._elements[:idx]

    def subSet(self, fromElement, toElement):
        """
        Returns a view of elements from `fromElement` (inclusive) to `toElement` (exclusive).

        :param fromElement: The lower bound (inclusive).
        :param toElement: The upper bound (exclusive).
        :return: List of elements in the specified range.
        """
        from_idx = bisect_left(self._elements, fromElement)
        to_idx = bisect_right(self._elements, toElement) - 1
        return self._elements[from_idx:to_idx]

    def tailSet(self, fromElement):
        """
        Returns a view of elements greater than or equal to `fromElement`.

        :param fromElement: The lower bound (inclusive).
        :return: List of elements greater than or equal to `fromElement`.
        """
        idx = bisect_left(self._elements, fromElement)
        return self._elements[idx:]

    def iterator(self):
        """
        Returns an iterator over the elements in ascending order.

        :return: Iterator for the elements.
        """
        return iter(self._elements)

    def size(self):
        """
        Returns the number of elements in the TreeSet.

        :return: Number of elements in the TreeSet.
        """
        return len(self._elements)

    def isEmpty(self):
        """
        Checks if the TreeSet is empty.

        :return: True if the TreeSet is empty, False otherwise.
        """
        return len(self._elements) == 0

    def remove(self, o):
        """
        Removes the specified element from the TreeSet if present.

        :param o: The element to remove.
        :return: True if the element was removed, False if it was not present.
        """
        idx = bisect_left(self._elements, o)
        if idx < len(self._elements) and self._elements[idx] == o:
            del self._elements[idx]
            return True
        return False

    def pollFirst(self):
        """
        Removes and returns the first (lowest) element, or None if the set is empty.

        :return: The first element, or None if the set is empty.
        """
        if self.isEmpty():
            return None
        return self._elements.pop(0)

    def pollLast(self):
        """
        Removes and returns the last (highest) element, or None if the set is empty.

        :return: The last element, or None if the set is empty.
        """
        if self.isEmpty():
            return None
        return self._elements.pop()

    def removeAll(self, collection):
        """
        Removes all elements in the specified collection from the TreeSet.

        :param collection: Collection of elements to remove.
        :return: True if any elements were removed, False otherwise.
        """
        removed = False
        for e in collection:
            removed |= self.remove(e)
        return removed

    def retainAll(self, collection):
        """
        Retains only the elements in this set that are contained in the specified collection.

        :param collection: Collection of elements to retain.
        :return: True if the set was modified, False otherwise.
        """
        retained_elements = [e for e in self._elements if e in collection]
        if len(retained_elements) != len(self._elements):
            self._elements = retained_elements
            return True
        return False

    def removeIf(self, predicate):
        """
        Removes all elements that satisfy the given predicate.

        :param predicate: Function that returns True for elements to remove.
        :return: True if any elements were removed, False otherwise.
        """
        removed = False
        filtered_elements = [e for e in self._elements if not predicate(e)]
        if len(filtered_elements) != len(self._elements):
            self._elements = filtered_elements
            removed = True
        return removed

    def stream(self):
        """
        Returns a stream (an iterator) with this set as its source.

        :return: Iterator for the elements.
        """
        return iter(self._elements)

    def parallelStream(self):
        """
        Returns a stream (an iterator) as a parallel stream.

        Note: In Python, there is no direct equivalent for parallel streams as in Java.
        This method returns the same as `stream()` for simplicity.

        :return: Iterator for the elements.
        """
        return iter(self._elements)

    def toArray(self, array=None):
        """
        Converts the elements in this set to an array.

        :param array: Optional array to store elements. If not provided, a new list is created.
        :return: List containing the elements of the TreeSet.
        """
        if array is None:
            return self._elements.copy()
        # If the provided array is too small, grow it
        array[:len(self._elements)] = self._elements
        return array

    def containsAll(self, collection):
        """
        Checks if this set contains all the elements in the specified collection.

        :param collection: Collection of elements to check for.
        :return: True if all elements are present, False otherwise.
        """
        return all(self.contains(e) for e in collection)

    def equals(self, other):
        """
        Compares the specified object with this set for equality.

        :param other: The object to compare with.
        :return: True if the object is a TreeSet and contains the same elements, False otherwise.
        """
        if not isinstance(other, TreeSet):
            return False
        return self._elements == other._elements

    def hashCode(self):
        """
        Returns the hash code value for this set.

        :return: Hash code of the set.
        """
        return hash(tuple(self._elements))

    def __iter__(self):
        """
        Implement the iterable interface.

        :return: Iterator for the elements.
        """
        return self.iterator()
