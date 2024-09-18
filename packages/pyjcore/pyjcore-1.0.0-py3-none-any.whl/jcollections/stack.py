from jcollections.vector import Vector

class Stack(Vector):
    def __init__(self):
        """
        Initializes an empty stack by calling the constructor of the parent Vector class.
        """
        super().__init__()

    def empty(self):
        """
        Checks if the stack is empty.
        Returns True if the stack contains no elements, False otherwise.
        """
        return self.elementCount == 0

    def peek(self):
        """
        Returns the object at the top of the stack without removing it.
        Raises IndexError if the stack is empty.
        """
        if self.empty():
            raise IndexError("peek from empty stack")
        return self.elementData[self.elementCount - 1]

    def pop(self):
        """
        Removes and returns the object at the top of the stack.
        Raises IndexError if the stack is empty.
        """
        if self.empty():
            raise IndexError("pop from empty stack")
        element = self.elementData[self.elementCount - 1]
        self.removeElementAt(self.elementCount - 1)
        return element

    def push(self, item):
        """
        Pushes the given item onto the top of the stack.
        Returns the pushed item.
        """
        self.addElement(item)
        return item

    def search(self, o):
        """
        Searches for the given object in the stack and returns its 1-based position from the top.
        The top element is considered position 1.
        Returns -1 if the object is not found.
        """
        try:
            index = self.lastIndexOf(o)
            if index == -1:
                return -1  # Element not found
            return self.elementCount - index
        except ValueError:
            return -1
