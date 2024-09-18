from heapq import heappush, heappop, heapify
from jcollections.collection import Collection
from jcollections.queue import Queue

class PriorityQueue(Collection, Queue):
    def __init__(self, initial=None, comparator=None, initial_capacity=11):
        """
        Initializes a PriorityQueue with optional initial elements, a comparator, and an initial capacity.
        - `initial`: Collection or list of initial elements.
        - `comparator`: Function to compare elements for priority.
        - `initial_capacity`: Initial capacity (not used in this implementation).
        """
        # Initialize with a default list_type (ArrayList or LinkedList can be used if needed)
        super().__init__(list_type=None)  # Default list_type is None; can be ArrayList or LinkedList

        self.comparator = comparator
        self._heap = []  # Internal heap to store elements in heap order

        # Add initial elements to the priority queue
        if isinstance(initial, Collection) or isinstance(initial, list):
            for item in initial:
                self.add(item)
        elif initial:
            raise TypeError("Initial input must be a Collection or None")

    def add(self, e):
        """
        Adds an element to the priority queue.
        - If a comparator is defined, use it to determine the priority.
        - Otherwise, add the element directly.
        """
        if self.comparator:
            heappush(self._heap, (self.comparator(e), e))
        else:
            heappush(self._heap, e)
        return True

    def offer(self, e):
        """
        Adds an element to the priority queue.
        Same as `add()`; included for consistency with Queue interface.
        """
        return self.add(e)

    def peek(self):
        """
        Retrieves but does not remove the highest-priority element from the queue.
        - Returns None if the queue is empty.
        """
        if self.isEmpty():
            return None
        return self._heap[0][1] if self.comparator else self._heap[0]

    def poll(self):
        """
        Removes and returns the highest-priority element from the queue.
        - Returns None if the queue is empty.
        """
        if self.isEmpty():
            return None
        return heappop(self._heap)[1] if self.comparator else heappop(self._heap)

    def remove(self, o):
        """
        Removes a specific element from the queue.
        - Re-heapify the heap after removal.
        - Returns True if the element was removed, False if not found.
        """
        try:
            self._heap.remove(o)
            heapify(self._heap)  # Re-heapify the heap after removing the element
            return True
        except ValueError:
            return False

    def contains(self, o):
        """
        Checks if the queue contains a specific element.
        """
        return o in self._heap

    def size(self):
        """
        Returns the number of elements in the queue.
        """
        return len(self._heap)

    def clear(self):
        """
        Removes all elements from the queue.
        """
        self._heap = []

    def isEmpty(self):
        """
        Checks if the queue is empty.
        """
        return len(self._heap) == 0

    def iterator(self):
        """
        Returns an iterator over the elements in the queue.
        """
        return iter(self._heap)

    def toArray(self):
        """
        Converts the queue to a list.
        """
        return list(self._heap)

    def toArrayWithType(self, arr):
        """
        Converts the queue to an array with the runtime type of the specified array.
        Note: In Python, this is implemented the same as `toArray()`.
        """
        return list(self._heap)

    def comparator(self):
        """
        Returns the comparator function used for the priority queue.
        """
        return self.comparator

    def spliterator(self):
        """
        Returns a spliterator (not implemented, as it's not common in Python).
        """
        pass

    def addAll(self, collection):
        """
        Adds all elements from another collection to the queue.
        """
        for item in collection:
            self.add(item)

    def element(self):
        """
        Retrieves but does not remove the highest-priority element.
        - Raises IndexError if the queue is empty.
        """
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self.peek()

    def removeAll(self, collection):
        """
        Removes all elements that are also contained in the specified collection.
        """
        for item in collection:
            self.remove(item)

    def retainAll(self, collection):
        """
        Retains only the elements contained in the specified collection.
        - Removes all elements not in the collection.
        """
        self._heap = [item for item in self._heap if item in collection]
        heapify(self._heap)

    def __iter__(self):
        """
        Returns an iterator over the elements in the priority queue.
        """
        return iter(self._heap)

    def containsAll(self, collection):
        """
        Returns True if all elements in the given collection are in the queue.
        """
        return all(item in self._heap for item in collection)

    def equals(self, other):
        """
        Compares this queue with another for equality.
        - Returns True if the queues have the same elements in the same order.
        """
        if not isinstance(other, PriorityQueue):
            return False
        return self._heap == other._heap

    def hashCode(self):
        """
        Returns the hash code for this queue.
        """
        return hash(tuple(self._heap))

    def removeIf(self, predicate):
        """
        Removes all elements that satisfy the given predicate.
        """
        self._heap = [item for item in self._heap if not predicate(item)]
        heapify(self._heap)

    def stream(self):
        """
        Returns a generator for the elements in the queue.
        """
        return iter(self._heap)

    def parallelStream(self):
        """
        Returns a parallel stream (not applicable in Python, so using normal stream).
        """
        return self.stream()
