from abc import ABC, abstractmethod

class Iterable(ABC):
    """
    Abstract base class for iterable objects. Subclasses must implement the __iter__() method.
    This ensures that instances of the subclass can return an iterator over the elements.
    """

    @abstractmethod
    def __iter__(self):
        """
        Returns an iterator over the elements in the collection.
        Subclasses must implement this method to return an iterator object.
        """
        pass

    # FIXME: Don't need the __next__() method here because it's typically part of the iterator class, not the iterable itself.
    # @abstractmethod
    # def __next__(self):
    #     pass
