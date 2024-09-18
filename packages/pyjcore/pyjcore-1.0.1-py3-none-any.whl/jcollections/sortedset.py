from abc import ABC, abstractmethod

from jcollections.set import Set


class SortedSet(Set, ABC):
    @abstractmethod
    def comparator(self):
        """
        Returns the comparator used to order the elements in this set, or null
        if this set uses the natural ordering of its elements.
        """
        pass

    @abstractmethod
    def first(self):
        """
        Returns the first (lowest) element currently in this set.
        """
        pass

    @abstractmethod
    def last(self):
        """
        Returns the last (highest) element currently in this set.
        """
        pass

    @abstractmethod
    def headSet(self, toElement):
        """
        Returns a view of the portion of this set whose elements are strictly less than toElement.
        :param toElement: the high endpoint (exclusive) of the subset
        :return: a view of the portion of this set whose elements are strictly less than toElement
        """
        pass

    @abstractmethod
    def subSet(self, fromElement, toElement):
        """
        Returns a view of the portion of this set whose elements range from fromElement (inclusive) to toElement (exclusive).
        :param fromElement: the low endpoint (inclusive) of the subset
        :param toElement: the high endpoint (exclusive) of the subset
        :return: a view of the portion of this set whose elements range from fromElement to toElement
        """
        pass

    @abstractmethod
    def tailSet(self, fromElement):
        """
        Returns a view of the portion of this set whose elements are greater than or equal to fromElement.
        :param fromElement: the low endpoint (inclusive) of the subset
        :return: a view of the portion of this set whose elements are greater than or equal to fromElement
        """
        pass

    def spliterator(self):
        """
        Creates a Spliterator over the elements in this sorted set (optional implementation).
        """
        # Optional method, can be implemented if needed
        pass
