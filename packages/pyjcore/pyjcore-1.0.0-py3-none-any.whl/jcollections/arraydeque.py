from jcollections.collection import Collection


class ArrayDeque(Collection):
    def __init__(self, initial=None):
        """
        Constructs an empty deque or deque with an initial collection or initial capacity.

        :param initial: Can be None, a Collection, or an integer (capacity).
        """
        self._deque = []

        # Handle case for ArrayDeque() - initialize empty deque
        if initial is None:
            self._deque = []

        # Handle case for ArrayDeque(Collection<? extends E> c) - initialize deque with elements
        elif isinstance(initial, Collection) or isinstance(initial, list):
            for item in initial:
                self.add(item)

        # Handle case for ArrayDeque(int numElements) - initialize deque with specified capacity
        elif isinstance(initial, int):
            self._capacity = initial  # Capacity is tracked separately
            self._deque = [None] * initial  # Initialize with None placeholders to given capacity

        else:
            raise TypeError("Invalid argument type. Must be None, Collection, or an integer.")

    def __iter__(self):
        """Returns an iterator over the elements in the deque in proper sequence."""
        return iter(self._deque)

    def add(self, e):
        """Inserts the element at the end of the deque (tail)."""
        self._deque.append(e)
        return True

    def addFirst(self, e):
        """Inserts the element at the front of the deque."""
        self._deque.insert(0, e)

    def addLast(self, e):
        """Inserts the element at the end of the deque."""
        self._deque.append(e)

    def addAll(self, collection):
        """Adds all elements from another collection to the deque."""
        for item in collection:
            self.add(item)

    def contains(self, o):
        """Returns True if the deque contains the specified element."""
        return o in self._deque

    def descendingIterator(self):
        """Returns an iterator over the elements in reverse order."""
        return iter(self._deque[::-1])

    def element(self):
        """Retrieves, but does not remove, the first element of the deque."""
        return self.getFirst()

    def getFirst(self):
        """Retrieves, but does not remove, the first element."""
        if not self._deque:
            raise IndexError("Deque is empty")
        return self._deque[0]

    def getLast(self):
        """Retrieves, but does not remove, the last element."""
        if not self._deque:
            raise IndexError("Deque is empty")
        return self._deque[-1]

    def iterator(self):
        """Returns an iterator over the elements in the deque."""
        return iter(self._deque)

    def offer(self, e):
        """Inserts the element at the tail if possible."""
        self.addLast(e)
        return True

    def offerFirst(self, e):
        """Inserts the element at the front of the deque unless capacity is exceeded."""
        self.addFirst(e)
        return True

    def offerLast(self, e):
        """Inserts the element at the end of the deque unless capacity is exceeded."""
        self.addLast(e)
        return True

    @property
    def __class__(self):
        """Returns the class of this object."""
        return super().__class__

    def peek(self):
        """Retrieves, but does not remove, the first element of the deque."""
        return self.peekFirst()

    def peekFirst(self):
        """Retrieves, but does not remove, the first element."""
        return self._deque[0] if self._deque else None

    def peekLast(self):
        """Retrieves, but does not remove, the last element."""
        return self._deque[-1] if self._deque else None

    def poll(self):
        """Retrieves and removes the first element."""
        return self.pollFirst()

    def pollFirst(self):
        """Retrieves and removes the first element."""
        return self._deque.pop(0) if self._deque else None

    def pollLast(self):
        """Retrieves and removes the last element."""
        return self._deque.pop() if self._deque else None

    def pop(self):
        """Pops an element from the stack (first element)."""
        return self.pollFirst()

    def push(self, e):
        """Pushes an element onto the stack (head of the deque)."""
        self.addFirst(e)

    def remove(self, o=None):
        """
        Retrieves and removes the first element, or removes a specific element.
        - If no argument is given, removes and returns the first element.
        - If an argument is given, removes the specified element.
        """
        if o is None:
            return self.pollFirst()
        else:
            try:
                self._deque.remove(o)
                return True
            except ValueError:
                return False

    def removeFirst(self):
        """Retrieves and removes the first element."""
        return self.pollFirst()

    def removeLast(self):
        """Retrieves and removes the last element."""
        return self.pollLast()

    def removeFirstOccurrence(self, o):
        """Removes the first occurrence of the specified element."""
        return self.remove(o)

    def removeLastOccurrence(self, o):
        """Removes the last occurrence of the specified element."""
        if o in self._deque:
            index = len(self._deque) - 1 - self._deque[::-1].index(o)
            del self._deque[index]
            return True
        return False

    def size(self):
        """Returns the number of elements in the deque."""
        return len(self._deque)

    def clear(self):
        """Removes all elements from the deque."""
        self._deque.clear()

    def containsAll(self, c):
        """Returns True if the deque contains all elements from the specified collection."""
        return all(item in self._deque for item in c)

    def equals(self, o):
        """Compares this deque with another for equality."""
        if not isinstance(o, ArrayDeque):
            return False
        return self._deque == o._deque

    def hashCode(self):
        """Returns a hash code for the deque."""
        return hash(tuple(self._deque))

    def isEmpty(self):
        """Returns True if the deque is empty."""
        return len(self._deque) == 0

    def parallelStream(self):
        """Returns a possibly parallel stream with this deque as its source."""
        # Placeholder for parallel stream functionality
        pass

    def removeAll(self, c):
        """Removes all elements in the deque that are also contained in the specified collection."""
        modified = False
        for item in c:
            while item in self._deque:
                self._deque.remove(item)
                modified = True
        return modified

    def removeIf(self, predicate):
        """Removes all elements of the deque that satisfy the given predicate."""
        original_size = len(self._deque)
        self._deque = [item for item in self._deque if not predicate(item)]
        return len(self._deque) != original_size

    def retainAll(self, c):
        """Retains only the elements in the deque that are also in the specified collection."""
        original_size = len(self._deque)
        self._deque = [item for item in self._deque if item in c]
        return len(self._deque) != original_size

    def spliterator(self):
        """Creates a spliterator over the elements in the deque."""
        # Placeholder for spliterator functionality
        pass

    def stream(self):
        """Returns a sequential stream with this deque as its source."""
        # Placeholder for stream functionality
        pass

    def toArray(self, *args):
        """Converts the deque to an array."""
        return list(self._deque)
