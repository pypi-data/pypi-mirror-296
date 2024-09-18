from abc import abstractmethod
from jcollections.collection import Collection

class List(Collection):
    """
    Abstract class representing an ordered collection (a list).
    Extends the Collection class to include operations specific to lists, such as positional access to elements.
    """

    @abstractmethod
    def add(self, *args):
        """
        Adds an element or elements to the list.
        """
        pass

    @abstractmethod
    def clear(self):
        """
        Removes all the elements from this list (optional operation).
        """
        pass

    @abstractmethod
    def contains(self, o):
        """
        Returns True if this list contains the specified element.
        :param o: The element to check for.
        """
        pass

    @abstractmethod
    def containsAll(self, c):
        """
        Returns True if this list contains all the elements of the specified collection.
        :param c: The collection to check for containment.
        """
        pass

    @abstractmethod
    def equals(self, o):
        """
        Compares the specified object with this list for equality.
        :param o: The object to compare with.
        """
        pass

    @abstractmethod
    def get(self, index):
        """
        Returns the element at the specified position in this list.
        :param index: The index of the element to return.
        """
        pass

    @abstractmethod
    def hashCode(self):
        """
        Returns the hash code value for this list.
        """
        pass

    @abstractmethod
    def indexOf(self, o):
        """
        Returns the index of the first occurrence of the specified element in this list, or -1 if the list does not contain the element.
        :param o: The element to search for.
        """
        pass

    @abstractmethod
    def isEmpty(self):
        """
        Returns True if this list contains no elements.
        """
        pass

    @abstractmethod
    def iterator(self):
        """
        Returns an iterator over the elements in this list in proper sequence.
        """
        pass

    @abstractmethod
    def lastIndexOf(self, o):
        """
        Returns the index of the last occurrence of the specified element in this list, or -1 if the list does not contain the element.
        :param o: The element to search for.
        """
        pass

    @abstractmethod
    def listIterator(self, *args):
        """
        Returns a list iterator over the elements in this list.
        :param args: Optional start index for the iterator.
        """
        pass

    @abstractmethod
    def remove(self, *args):
        """
        Removes the element at the specified position in this list or a specified element.
        """
        pass

    @abstractmethod
    def removeAll(self, c):
        """
        Removes from this list all of its elements that are contained in the specified collection (optional operation).
        :param c: The collection of elements to be removed.
        """
        pass

    @abstractmethod
    def replaceAll(self, operator):
        """
        Replaces each element of this list with the result of applying the operator to that element.
        :param operator: A function to apply to each element.
        """
        pass

    @abstractmethod
    def retainAll(self, c):
        """
        Retains only the elements in this list that are contained in the specified collection (optional operation).
        :param c: The collection to retain elements from.
        """
        pass

    @abstractmethod
    def set(self, index, element):
        """
        Replaces the element at the specified position in this list with the specified element (optional operation).
        :param index: The index of the element to replace.
        :param element: The element to replace with.
        """
        pass

    @abstractmethod
    def size(self):
        """
        Returns the number of elements in this list.
        """
        pass

    @abstractmethod
    def sort(self, c):
        """
        Sorts this list according to the order induced by the specified Comparator.
        :param c: The comparator to determine the order of the list.
        """
        pass

    @abstractmethod
    def spliterator(self):
        """
        Creates a Spliterator over the elements in this list.
        """
        pass

    @abstractmethod
    def subList(self, fromIndex, toIndex):
        """
        Returns a view of the portion of this list between the specified fromIndex, inclusive, and toIndex, exclusive.
        :param fromIndex: The starting index of the sublist.
        :param toIndex: The ending index of the sublist.
        """
        pass

    @abstractmethod
    def toArray(self, *args):
        """
        Converts the list elements into an array.
        :param args: Optional argument specifying the type of array elements.
        """
        pass
