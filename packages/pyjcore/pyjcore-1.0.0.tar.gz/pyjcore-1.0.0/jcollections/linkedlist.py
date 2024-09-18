from jcollections.list import List

class LinkedListIterator:
    def __init__(self, linked_list):
        """
        Initializes the iterator with the given linked list.
        """
        self.current = linked_list.head

    def __iter__(self):
        """
        Returns the iterator instance itself.
        """
        return self

    def __next__(self):
        """
        Returns the next element in the iteration.
        Raises StopIteration if there are no more elements.
        """
        if self.current is None:
            raise StopIteration
        data = self.current.data
        self.current = self.current.next
        return data

class Node:
    def __init__(self, data=None):
        """
        Initializes a node with the given data and no links.
        """
        self.data = data
        self.next = None
        self.prev = None

class LinkedList(List):
    def __init__(self, collection=None):
        """
        Initializes an empty linked list or creates it from a given collection.
        """
        self.head = None
        self.tail = None
        self._size = 0

        if collection:
            for item in collection:
                self.add(item)

    def add(self, *args):
        """
        Adds an element to the list:
        - Single argument: Adds the element at the end.
        - Two arguments: Adds the element at the specified index.
        """
        if len(args) == 1:
            element = args[0]
            self.addLast(element)
            return True
        elif len(args) == 2:
            index, element = args
            self.addAt(index, element)
            return True
        else:
            raise TypeError("Invalid number of arguments")

    def addFirst(self, element):
        """
        Adds an element to the beginning of the list.
        """
        new_node = Node(element)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def addLast(self, element):
        """
        Adds an element to the end of the list.
        """
        new_node = Node(element)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def addAt(self, index, element):
        """
        Adds an element at the specified index:
        - Index 0: Adds at the beginning.
        - Index size: Adds at the end.
        - Otherwise: Inserts at the specified index.
        """
        if index < 0 or index > self._size:
            raise IndexError("Index out of bounds")

        if index == 0:
            self.addFirst(element)
        elif index == self._size:
            self.addLast(element)
        else:
            new_node = Node(element)
            current = self.head
            for _ in range(index):
                current = current.next
            previous = current.prev
            previous.next = new_node
            new_node.prev = previous
            new_node.next = current
            current.prev = new_node
            self._size += 1

    def addAll(self, *args):
        """
        Adds all elements from a collection:
        - Single argument: Adds all elements at the end.
        - Two arguments: Adds elements at the specified index.
        """
        if len(args) == 1:
            collection = args[0]
            for item in collection:
                self.addLast(item)
            return True
        elif len(args) == 2:
            index, collection = args
            if index < 0 or index > self._size:
                raise IndexError("Index out of bounds")
            for item in collection:
                self.addAt(index, item)
                index += 1
            return True
        else:
            raise TypeError("Invalid number of arguments")

    def clear(self):
        """
        Removes all elements from the list and resets size to 0.
        """
        self.head = self.tail = None
        self._size = 0

    def clone(self):
        """
        Creates and returns a deep copy of the list.
        """
        cloned_list = LinkedList()
        current = self.head
        while current:
            cloned_list.addLast(current.data)
            current = current.next
        return cloned_list

    def contains(self, element):
        """
        Checks if the list contains the specified element.
        """
        return self.indexOf(element) != -1

    def descendingIterator(self):
        """
        Returns an iterator that traverses the list in reverse order.
        """
        current = self.tail
        while current:
            yield current.data
            current = current.prev

    def element(self):
        """
        Returns the first element of the list.
        Raises IndexError if the list is empty.
        """
        if self.head is None:
            raise IndexError("LinkedList is empty")
        return self.head.data

    def get(self, index):
        """
        Retrieves the element at the specified index.
        Raises IndexError if the index is out of bounds.
        """
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    def getFirst(self):
        """
        Returns the first element of the list.
        Raises IndexError if the list is empty.
        """
        if self.head is None:
            raise IndexError("LinkedList is empty")
        return self.head.data

    def getLast(self):
        """
        Returns the last element of the list.
        Raises IndexError if the list is empty.
        """
        if self.tail is None:
            raise IndexError("LinkedList is empty")
        return self.tail.data

    def indexOf(self, element):
        """
        Finds the index of the first occurrence of the specified element.
        Returns -1 if the element is not found.
        """
        current = self.head
        index = 0
        while current:
            if current.data == element:
                return index
            current = current.next
            index += 1
        return -1

    def lastIndexOf(self, element):
        """
        Finds the index of the last occurrence of the specified element.
        Returns -1 if the element is not found.
        """
        current = self.tail
        index = self._size - 1
        while current:
            if current.data == element:
                return index
            current = current.prev
            index -= 1
        return -1

    def listIterator(self, index=0):
        """
        Returns an iterator starting from the specified index.
        Raises IndexError if the index is out of bounds.
        """
        current = self.head
        for _ in range(index):
            if current is None:
                raise IndexError("Index out of bounds")
            current = current.next
        while current:
            yield current.data
            current = current.next

    def offer(self, element):
        """
        Adds the element to the end of the list (similar to addLast).
        """
        self.addLast(element)
        return True

    def offerFirst(self, element):
        """
        Adds the element to the beginning of the list (similar to addFirst).
        """
        self.addFirst(element)
        return True

    def offerLast(self, element):
        """
        Adds the element to the end of the list (similar to addLast).
        """
        self.addLast(element)
        return True

    def peek(self):
        """
        Returns the first element of the list without removing it.
        Returns None if the list is empty.
        """
        if self.head is None:
            return None
        return self.head.data

    def peekFirst(self):
        """
        Returns the first element of the list without removing it.
        """
        return self.peek()

    def peekLast(self):
        """
        Returns the last element of the list without removing it.
        Returns None if the list is empty.
        """
        if self.tail is None:
            return None
        return self.tail.data

    def poll(self):
        """
        Removes and returns the first element of the list.
        Returns None if the list is empty.
        """
        if self.head is None:
            return None
        return self.removeFirst()

    def pollFirst(self):
        """
        Removes and returns the first element of the list.
        """
        return self.poll()

    def pollLast(self):
        """
        Removes and returns the last element of the list.
        Returns None if the list is empty.
        """
        if self.tail is None:
            return None
        return self.removeLast()

    def pop(self):
        """
        Removes and returns the first element of the list (similar to pollFirst).
        """
        return self.removeFirst()

    def push(self, element):
        """
        Adds the element to the beginning of the list (similar to addFirst).
        """
        self.addFirst(element)

    def remove(self, *args):
        """
        Removes an element from the list:
        - No arguments: Removes the first element.
        - Single integer argument: Removes the element at the specified index.
        - Single non-integer argument: Removes the first occurrence of the specified element.
        """
        if len(args) == 0:
            return self.removeFirst()
        elif len(args) == 1:
            if isinstance(args[0], int):
                return self.removeAt(args[0])
            else:
                return self.removeElement(args[0])
        else:
            raise TypeError("Invalid number of arguments")

    def removeAt(self, index):
        """
        Removes the element at the specified index.
        Raises IndexError if the index is out of bounds.
        """
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        current = self.head
        for _ in range(index):
            current = current.next
        self._removeNode(current)
        return current.data

    def removeFirst(self):
        """
        Removes and returns the first element of the list.
        Raises IndexError if the list is empty.
        """
        if self.head is None:
            raise IndexError("LinkedList is empty")
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None
        self._size -= 1
        return data

    def removeLast(self):
        """
        Removes and returns the last element of the list.
        Raises IndexError if the list is empty.
        """
        if self.tail is None:
            raise IndexError("LinkedList is empty")
        data = self.tail.data
        self.tail = self.tail.prev
        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None
        self._size -= 1
        return data

    def removeElement(self, element):
        """
        Removes the first occurrence of the specified element.
        Returns True if an element was removed, False otherwise.
        """
        current = self.head
        while current:
            if current.data == element:
                self._removeNode(current)
                return True
            current = current.next
        return False

    def _removeNode(self, node):
        """
        Removes the given node from the list.
        """
        if node.prev is None:
            self.head = node.next
        else:
            node.prev.next = node.next
        if node.next is None:
            self.tail = node.prev
        else:
            node.next.prev = node.prev
        self._size -= 1

    def removeFirstOccurrence(self, element):
        """
        Removes the first occurrence of the specified element.
        """
        return self.removeElement(element)

    def removeLastOccurrence(self, element):
        """
        Removes the last occurrence of the specified element.
        """
        current = self.tail
        while current:
            if current.data == element:
                self._removeNode(current)
                return True
            current = current.prev
        return False

    def set(self, index, element):
        """
        Sets the element at the specified index.
        Raises IndexError if the index is out of bounds.
        """
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        current = self.head
        for _ in range(index):
            current = current.next
        current.data = element

    def size(self):
        """
        Returns the number of elements in the list.
        """
        return self._size

    def spliterator(self):
        """
        Returns an iterator for the list.
        """
        return self.iterator()

    def toArray(self, *args):
        """
        Converts the list to an array:
        - No arguments: Returns a new list.
        - Single argument: Fills the provided array with list elements.
        """
        array = []
        current = self.head
        while current:
            array.append(current.data)
            current = current.next
        if len(args) == 0:
            return array
        elif len(args) == 1:
            a = args[0]
            if len(a) < len(array):
                a = array[:len(array)]
            else:
                for i in range(len(array)):
                    a[i] = array[i]
            return a
        else:
            raise TypeError("Invalid number of arguments")

    def subList(self, fromIndex, toIndex):
        """
        Returns a sublist from the specified range.
        Raises IndexError if the indices are out of bounds or invalid.
        """
        if fromIndex < 0 or toIndex > self._size or fromIndex > toIndex:
            raise IndexError("Index out of bounds")
        sublist = LinkedList()
        current = self.head
        for _ in range(fromIndex):
            current = current.next
        for _ in range(toIndex - fromIndex):
            sublist.addLast(current.data)
            current = current.next
        return sublist

    def __iter__(self):
        """
        Returns an iterator for the linked list.
        """
        return LinkedListIterator(self)

    def containsAll(self, collection):
        """
        Checks if all elements in the specified collection are in the list.
        """
        for item in collection:
            if not self.contains(item):
                return False
        return True

    def equals(self, other):
        """
        Checks if this list is equal to another list.
        """
        if not isinstance(other, LinkedList):
            return False
        if self.size() != other.size():
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True

    def __hash__(self):
        """
        Returns the hash code for the list.
        """
        return hash(tuple(self))

    def isEmpty(self):
        """
        Checks if the list is empty.
        """
        return self.size() == 0

    def iterator(self):
        """
        Returns an iterator for the list.
        """
        return iter(self)

    def parallelStream(self):
        """
        Not implemented. Raises NotImplementedError.
        """
        raise NotImplementedError("parallelStream not implemented")

    def removeAll(self, collection):
        """
        Removes all elements that are present in the specified collection.
        """
        modified = False
        for item in collection:
            while self.contains(item):
                self.remove(item)
                modified = True
        return modified

    def removeIf(self, predicate):
        """
        Removes all elements that satisfy the given predicate.
        """
        current = self.head
        prev = None
        modified = False
        while current:
            if predicate(current.data):
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                modified = True
            else:
                prev = current
            current = current.next
        return modified

    def replaceAll(self, operator):
        """
        Replaces each element with the result of applying the given operator.
        """
        current = self.head
        while current:
            current.data = operator(current.data)
            current = current.next

    def retainAll(self, collection):
        """
        Retains only elements that are present in the specified collection.
        """
        current = self.head
        prev = None
        modified = False
        while current:
            if current.data not in collection:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                modified = True
            else:
                prev = current
            current = current.next
        return modified

    def sort(self, key=None, reverse=False):
        """
        Sorts the list elements.
        - key: A function to customize the sorting.
        - reverse: If True, sorts in descending order.
        """
        if self.size() <= 1:
            return

        # Convert to list, sort, and rebuild linked list
        lst = list(self)
        lst.sort(key=key, reverse=reverse)

        self.head = None
        for item in lst:
            self.add(item)

    def hashCode(self):
        """
        Returns the hash code for the list.
        """
        return hash(tuple(self))

    def stream(self):
        """
        Returns a generator for iterating over the list elements.
        """
        return (item for item in self)
