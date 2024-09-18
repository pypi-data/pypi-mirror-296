from abc import abstractmethod

from jcollections.Iterable import Iterable


class Collection(Iterable):
    """
    Abstract class representing a general collection of elements.
    Extends the Iterable class to allow for iteration over the collection.
    Subclasses must implement all abstract methods to define specific collection behaviors.
    """

    @abstractmethod
    def add(self, *args):
        """
        Adds an element or elements to the collection.
        Subclasses must implement this method to define how elements are added to the collection.
        """
        pass

    @abstractmethod
    def clear(self):
        """
        Removes all the elements from this collection (optional operation).
        Subclasses must implement this to define how to clear the collection.
        """
        pass

    @abstractmethod
    def contains(self, o):
        """
        Returns True if this collection contains the specified element.
        :param o: The element to check for.
        """
        pass

    @abstractmethod
    def containsAll(self, c):
        """
        Returns True if this collection contains all the elements in the specified collection.
        :param c: The collection to check for containment.
        """
        pass

    @abstractmethod
    def equals(self, o):
        """
        Compares the specified object with this collection for equality.
        :param o: The object to compare with.
        :return: True if the specified object is equal to this collection, otherwise False.
        """
        pass

    @abstractmethod
    def hashCode(self):
        """
        Returns the hash code value for this collection.
        """
        pass

    @abstractmethod
    def isEmpty(self):
        """
        Returns True if this collection contains no elements.
        """
        pass

    @abstractmethod
    def iterator(self):
        """
        Returns an iterator over the elements in this collection.
        """
        pass

    @abstractmethod
    def parallelStream(self):
        """
        Returns a possibly parallel Stream with this collection as its source.
        """
        pass

    @abstractmethod
    def remove(self, o):
        """
        Removes a single instance of the specified element from this collection, if present.
        :param o: The element to be removed.
        """
        pass

    @abstractmethod
    def removeAll(self, c):
        """
        Removes all of this collection's elements that are also contained in the specified collection (optional operation).
        :param c: The collection of elements to be removed.
        """
        pass

    @abstractmethod
    def removeIf(self, predicate):
        """
        Removes all the elements of this collection that satisfy the given predicate.
        :param predicate: A function that returns True for elements to be removed.
        """
        pass

    @abstractmethod
    def retainAll(self, c):
        """
        Retains only the elements in this collection that are contained in the specified collection (optional operation).
        :param c: The collection to retain elements from.
        """
        pass

    @abstractmethod
    def size(self):
        """
        Returns the number of elements in this collection.
        """
        pass

    @abstractmethod
    def spliterator(self):
        """
        Creates a Spliterator over the elements in this collection.
        """
        pass

    @abstractmethod
    def stream(self):
        """
        Returns a sequential Stream with this collection as its source.
        """
        pass

    @abstractmethod
    def toArray(self, *args):
        """
        Converts the elements of the collection into an array.
        :param args: Optional argument specifying the type of array elements.
        """
        pass