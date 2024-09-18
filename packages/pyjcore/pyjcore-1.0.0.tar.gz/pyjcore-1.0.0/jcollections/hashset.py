from jcollections.set import Set

class HashSet(Set):
    """
    Implementation of a HashSet, a collection that does not allow duplicate elements
    and does not guarantee any specific order of elements.

    Inherits from:
        - Set: Provides abstract methods for set operations.
    """

    def __init__(self, initial_capacity: int = 16, load_factor: float = 0.75, elements=None):
        """
        Constructs a HashSet with the specified initial capacity and load factor.

        :param initial_capacity: The initial capacity of the HashSet. (Not used in Python's set)
        :param load_factor: The load factor of the HashSet. (Not used in Python's set)
        :param elements: An optional collection of elements to add to the HashSet at initialization.
        """
        self._set = set()  # Using Python's built-in set for internal storage
        self._initial_capacity = initial_capacity
        self._load_factor = load_factor

        if elements:
            self.addAll(elements)

    def add(self, e) -> bool:
        """
        Adds the specified element if it is not already present in the set.

        :param e: The element to add.
        :return: True if the element was added, False if it was already present.
        """
        if e not in self._set:
            self._set.add(e)
            return True
        return False

    def addAll(self, c) -> bool:
        """
        Adds all elements from the specified collection if they are not already present.

        :param c: Collection of elements to add.
        :return: True if any elements were added, False otherwise.
        """
        initial_size = len(self._set)
        self._set.update(c)
        return len(self._set) > initial_size

    def clear(self) -> None:
        """
        Removes all elements from the set.
        """
        self._set.clear()

    def contains(self, o) -> bool:
        """
        Checks if the set contains the specified element.

        :param o: The element to check for.
        :return: True if the set contains the element, False otherwise.
        """
        return o in self._set

    def containsAll(self, c) -> bool:
        """
        Checks if the set contains all elements of the specified collection.

        :param c: Collection of elements to check for.
        :return: True if all elements are present, False otherwise.
        """
        return all(item in self._set for item in c)

    def equals(self, o) -> bool:
        """
        Compares the set with another object for equality.

        :param o: The object to compare with.
        :return: True if the object is a HashSet and contains the same elements, False otherwise.
        """
        if isinstance(o, HashSet):
            return self._set == o._set
        return False

    def hashCode(self) -> int:
        """
        Returns a hash code value for this set.

        :return: Hash code of the set.
        """
        return hash(frozenset(self._set))

    def isEmpty(self) -> bool:
        """
        Checks if the set contains no elements.

        :return: True if the set is empty, False otherwise.
        """
        return len(self._set) == 0

    def iterator(self):
        """
        Returns an iterator over the elements in the set.

        :return: Iterator for the set.
        """
        return iter(self._set)

    def remove(self, o) -> bool:
        """
        Removes the specified element if it is present.

        :param o: The element to remove.
        :return: True if the element was removed, False if it was not present.
        """
        if o in self._set:
            self._set.remove(o)
            return True
        return False

    def removeAll(self, c) -> bool:
        """
        Removes from the set all elements that are contained in the specified collection.

        :param c: Collection of elements to remove.
        :return: True if any elements were removed, False otherwise.
        """
        initial_size = len(self._set)
        self._set.difference_update(c)
        return len(self._set) < initial_size

    def retainAll(self, c) -> bool:
        """
        Retains only the elements in the set that are contained in the specified collection.

        :param c: Collection of elements to retain.
        :return: True if the set was modified, False otherwise.
        """
        initial_size = len(self._set)
        self._set.intersection_update(c)
        return len(self._set) < initial_size

    def size(self) -> int:
        """
        Returns the number of elements in the set.

        :return: Size of the set.
        """
        return len(self._set)

    def spliterator(self):
        """
        Creates a Spliterator over the elements in the set.

        :return: An iterator for the set (mock implementation, as Python does not have a direct Spliterator equivalent).
        """
        return iter(self._set)

    def toArray(self):
        """
        Returns an array containing all the elements in the set.

        :return: List of elements in the set.
        """
        return list(self._set)

    def clone(self):
        """
        Returns a shallow copy of this HashSet instance.

        :return: A new HashSet instance with the same elements.
        """
        return HashSet(elements=self._set)

    def __str__(self):
        """
        Returns a string representation of this set.

        :return: String representation of the set.
        """
        return str(self._set)

    def removeIf(self, predicate) -> bool:
        """
        Removes all elements that satisfy the given predicate.

        :param predicate: Function that returns True for elements to remove.
        :return: True if any elements were removed, False otherwise.
        """
        initial_size = len(self._set)
        self._set = {x for x in self._set if not predicate(x)}
        return len(self._set) < initial_size

    def stream(self):
        """
        Returns a sequential stream (iterator in Python terms) of the set elements.

        :return: Iterator for the set.
        """
        return iter(self._set)

    def parallelStream(self):
        """
        In Python, no direct parallel stream equivalent. Mocked as the same as stream().

        :return: Iterator for the set (same as stream() in Python).
        """
        return iter(self._set)

    def __iter__(self):
        """
        Returns an iterator to make the class iterable.

        :return: Iterator for the set.
        """
        return self.iterator()
