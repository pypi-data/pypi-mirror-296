from abc import ABC

from jcollections.Iterable import Iterable
from jcollections.collection import Collection


# Collection class already inherits from Iterable, so Set can simply inherit Collection
class Set(Collection, Iterable, ABC):
    """
    Abstract base class for a Set.

    A Set is a collection that does not allow duplicate elements and does not guarantee any specific order of elements.
    This class inherits from Collection and Iterable, making it both a Collection and an Iterable.

    Inherits from:
        - Collection: Provides methods for adding, removing, and querying elements.
        - Iterable: Provides methods for iterating over elements.
        - ABC: Abstract Base Class to enforce that this is an abstract class.
    """

    # The following methods are inherited abstract methods from Collection and Iterable
    # There's no need to declare them again unless providing optional or default implementations.

    def spliterator(self):
        """
        Creates a Spliterator over the elements in this set (optional).

        A Spliterator is used to traverse and partition elements of the Set. This method is optional and can be used to provide
        a custom implementation if needed. By default, it may not be implemented.
        """
        pass
