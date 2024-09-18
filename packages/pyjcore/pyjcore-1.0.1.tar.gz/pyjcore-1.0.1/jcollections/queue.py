from jcollections.arraylist import ArrayList
from jcollections.linkedlist import LinkedList

class Queue:
    def __init__(self, list_type):
        """
        Initializes a queue with the specified list type (ArrayList or LinkedList).
        """
        self.list = list_type

    def addLast(self, element):
        """
        Adds the given element to the end of the queue.
        Uses the appropriate method based on the list type:
        - For ArrayList, uses add (appends the element at the end).
        - For LinkedList, uses addLast (appends the element at the end).
        """
        if isinstance(self.list, ArrayList):
            self.list.add(element)  # For ArrayList, use add (appends at the end)
        elif isinstance(self.list, LinkedList):
            self.list.addLast(element)  # For LinkedList, use addLast

    def removeFirst(self):
        """
        Removes and returns the first element of the queue.
        Uses the appropriate method based on the list type:
        - For ArrayList, removes the element at index 0.
        - For LinkedList, uses removeFirst (removes the first element).
        Raises IndexError if the queue is empty.
        """
        if isinstance(self.list, ArrayList):
            if not self.list.isEmpty():
                return self.list.remove(0)  # For ArrayList, remove first element
            else:
                raise IndexError("Queue is empty")
        elif isinstance(self.list, LinkedList):
            return self.list.removeFirst()  # For LinkedList, directly removeFirst

    def peek(self):
        """
        Retrieves, but does not remove, the first element of the queue.
        Uses the appropriate method based on the list type:
        - For ArrayList, retrieves the element at index 0.
        - For LinkedList, uses peekFirst (retrieves the first element).
        Returns None if the queue is empty.
        """
        if isinstance(self.list, ArrayList):
            if not self.list.isEmpty():
                return self.list.get(0)  # For ArrayList, get the first element
            return None
        elif isinstance(self.list, LinkedList):
            return self.list.peekFirst()  # For LinkedList, peekFirst is available

    def poll(self):
        """
        Removes and returns the first element of the queue.
        Uses the appropriate method based on the list type:
        - For ArrayList, removes and returns the element at index 0.
        - For LinkedList, uses pollFirst (removes and returns the first element).
        Returns None if the queue is empty.
        """
        if isinstance(self.list, ArrayList):
            if not self.list.isEmpty():
                return self.removeFirst()  # For ArrayList, remove and return the first element
            return None
        elif isinstance(self.list, LinkedList):
            return self.list.pollFirst()  # For LinkedList, pollFirst is available

    def element(self):
        """
        Retrieves but does not remove the first element of the queue.
        Uses the appropriate method based on the list type:
        - For ArrayList, retrieves the element at index 0 and raises IndexError if the queue is empty.
        - For LinkedList, uses peekFirst and raises IndexError if the queue is empty.
        """
        if isinstance(self.list, ArrayList):
            if not self.list.isEmpty():
                return self.list.get(0)
            else:
                raise IndexError("No Such Element")  # Different from peek (raises exception if empty)
        elif isinstance(self.list, LinkedList):
            result = self.list.peekFirst()
            if result is None:
                raise IndexError("No Such Element")
            return result

    def offer(self, element):
        """
        Inserts the given element into the queue.
        Since capacity restrictions are not handled, this method behaves the same as addLast.
        Returns True to indicate successful insertion.
        """
        self.addLast(element)
        return True

    def getList(self):
        """
        Returns the internal list instance used by the queue.
        """
        return self.list
