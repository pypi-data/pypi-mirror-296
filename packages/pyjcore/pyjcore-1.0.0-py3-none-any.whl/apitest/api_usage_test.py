from jcollections.hashtable import Hashtable
from jcollections.linkedhashmap import LinkedHashMap
from jcollections.hashmap import HashMap
from jcollections.treeset import TreeSet
from jcollections.linkedhashset import LinkedHashSet
from jcollections.hashset import HashSet
from jcollections.arraydeque import ArrayDeque
from jcollections.priorityqueue import PriorityQueue
from jcollections.stack import Stack
from jcollections.vector import Vector
from jcollections.Predicate import Predicate
from jcollections.arraylist import ArrayList
from jcollections.linkedlist import LinkedList
from jcollections.queue import Queue
from jstring import StringBuilder, String
from jcollections.treemap import TreeMap


def test_string():
    s = StringBuilder("Sariya Python Java Lib to mimic the java collections and APIs")
    print(s.toString())
    s.append("-Based on Python")
    print(s.toString())
    print(s.capacity())
    print(s.ensureCapacity(50))
    print(s.capacity())
    # print(s.reverse())
    print(s)

    print("SubSequence = ", s.substring(5, 9))

    s2 = String("Please locate where 'locate' occurs!")
    s2.indexOf('l')
    print(s2.indexOf('o'))


    str1 = String("Hello")
    str2 = String("World")

    if str1.equals(str2):
        print("Strings are equal")
    else:
        print("Strings are not equal")

    str3 = str1 + " " + str2
    print("Concatenated String: ", str3)

    print("Length of str1: ", str1.length())

    substr = str3.substring(6, 11)
    print("Substring: ", substr)

    print("Uppercase: ", str1.toUpperCase())
    print("Lowercase: ", str2.toLowerCase())

def test_arraylist():
    # Create an ArrayList instance
    array_list = ArrayList()

    # Add elements to the ArrayList
    array_list.add("Apple")
    array_list.add("Banana")
    array_list.add("Cherry")
    print("After adding elements:", array_list.toArray())

    array_list.add("Apple1")
    array_list.add("Banana1")
    array_list.add("Cherry1")
    print("After adding elements:", array_list.toArray())

    print("Len:", len(array_list.toArray()), " size:", array_list.size())
    # Add multiple elements using addAll
    array_list.addAll(["Date", "Elderberry", "Fig"])
    print("After adding multiple elements:", array_list.toArray())

    # Remove an element by index
    removed_element = array_list.remove(2)  # Removes "Cherry"
    print(f"Removed element: {removed_element}")
    print("After removing element by index:", array_list.toArray())

    # Remove an element by value
    was_removed = array_list.remove("Banana")
    print(f"Was 'Banana' removed? {was_removed}")
    print("After removing element by value:", array_list.toArray())

    # Convert to an array
    array_representation = array_list.toArray()
    print("Array representation of ArrayList:", array_representation)

    # Convert to an array with a specific type (simulated)
    array_representation_with_type = array_list.toArray(str)
    print("Array representation with type:", array_representation_with_type)

    alist = ArrayList()
    # Explicitly accessing _data to add elements therefore size update is also required
    # Can be taken care using __setattr__ method but may give out of index error
    # Note: _data has been replaced with __data. Therefore, accessing it may not work anymore.
    # In short, direct access to data, size and capacity variable is not allowed.
    alist.__data = ['1', '2', '3', '4']
    alist.__size = len(alist.__data)
    print("Size of alist:", alist.size())
    # Convert to an array without arguments
    print(alist.toArray())  # Output: ['1', '2', '3', '4']
    # Convert to an array with the 'str' type (elements remain strings)
    print(alist.toArray(str))  # Output: ['1', '2', '3', '4']

    # Convert to an array with the 'int' type (converts strings to integers)
    print(alist.toArray(int))  # Output: [1, 2, 3, 4]

    pred_list = ArrayList()
    pred_list.add(1)
    pred_list.add(2)
    pred_list.add(3)
    pred_list.add(4)
    pred_list.add(5)

    print("Size of pred list:", pred_list.size())

    # Define a predicate to remove even numbers
    is_even = Predicate(lambda x: x % 2 == 0)

    # Use the removeIf method to remove all even numbers
    pred_list.removeIf(is_even)

    # Print the result
    print(pred_list.toArray())  # Output should be [1, 3, 5]
    print("Size of pred list:", pred_list.size())

    pred_list.add(2)
    pred_list.add(4)
    pred_list.add(6)
    print("Size of pred list:", pred_list.size())
    print(pred_list.toArray())

    val_removed = pred_list.remove(2)
    print("Removed", val_removed, " List after remove", pred_list.toArray())

    try:
        val_removed = pred_list.remove(6)
    except Exception as e:
        print("Call Error:", e)
    finally:
        print("Make sure you remain in bounds")

    print("List has ", pred_list.toArray())
    print(pred_list.addAll([9, 8, 7, 6, 6, 10, 12]))
    print("List has ", pred_list.toArray())
    print("Len:", len(pred_list.toArray()), " size:", pred_list.size())

def test_linkedlist():
    # Create a LinkedList and add some elements
    ll = LinkedList()
    ll.add("Zero")
    ll.add("First")
    ll.add("Second")
    ll.add("Third")
    ll.add("Fourth")
    ll.add("Last")
    ll.addLast("Fifth")
    ll.addFirst("New First")

    # Iterating over the list
    print("Iterating over the list:")
    for item in ll:
        print("Using ListIterator", item)

    # Cloning and printing the cloned list
    cloned_list = ll.clone()
    print("Cloned list size:", cloned_list.size())

    # Array representation
    print("Array representation:", ll.toArray())

    # Print various outputs
    print("Contains 'Third':", ll.contains("Third"))
    print("Element at index 2:", ll.get(2))
    print("First element:", ll.getFirst())
    print("Last element:", ll.getLast())
    print("Index of 'Third':", ll.indexOf("Third"))
    print("Last index of 'Second':", ll.lastIndexOf("Second"))
    print("Removed element at index 1:", ll.removeAt(1))
    print("Removed 'Fourth':", ll.removeElement("Fourth"))
    print("Polled first element:", ll.pollFirst())
    print("Polled last element:", ll.pollLast())
    print("Peek first element:", ll.peekFirst())
    print("Peek last element:", ll.peekLast())
    print("Popped element:", ll.pop())
    ll.push("New First")
    print("Size of the list:", ll.size())
    ll.clear()
    print("Size after clearing:", ll.size())
    print("Is the list empty:", ll.size() == 0)

    # Cloning and printing the cloned list
    cloned_list = ll.clone()
    print("Cloned list size:", cloned_list.size())

    # Array representation
    print("Array representation:", ll.toArray())

    # Iterating over the list
    print("Iterating over the list:")
    for item in ll:
        print(item)

def test_vector():
    # Testing Vector constructors
    print("Testing constructors...")
    v1 = Vector()  # Default constructor
    v2 = Vector(20)  # Constructor with initial capacity
    v3 = Vector(20, 5)  # Constructor with initial capacity and capacity increment
    v4 = Vector([1, 2, 3, 4, 5])  # Constructor with collection

    # Testing add and addElement
    print("Testing add methods...")
    v1.add(10)
    v1.add(20)
    v1.addElement(30)
    print(f"v1 after adding elements: {v1.elementData[:v1.size()]}")

    # Testing add with index
    v1.add(1, 15)
    print(f"v1 after adding 15 at index 1: {v1.elementData[:v1.size()]}")

    # Testing addAll
    v1.addAll([40, 50, 60])
    print(f"v1 after addAll: {v1.elementData[:v1.size()]}")

    # Testing addAll with index
    v1.addAll(2, [70, 80])
    print(f"v1 after addAll at index 2: {v1.elementData[:v1.size()]}")

    # Testing capacity and ensureCapacity
    print("Testing capacity and ensureCapacity...")
    print(f"v1 capacity before ensureCapacity: {len(v1.elementData)}")
    v1.ensureCapacity(50)
    print(f"v1 capacity after ensureCapacity: {len(v1.elementData)}")

    # Testing clear
    print("Testing clear...")
    v1.clear()
    print(f"v1 after clear: {v1.elementData[:v1.size()]}")

    # Testing contains and containsAll
    print("Testing contains and containsAll...")
    v1.addAll([1, 2, 3, 4, 5])
    print(f"v1 contains 3: {v1.contains(3)}")
    print(f"v1 contains all [2, 3, 4]: {v1.containsAll([2, 3, 4])}")
    print(f"v1 contains all [2, 6, 4]: {v1.containsAll([2, 6, 4])}")

    # Testing clone
    print("Testing clone...")
    v5 = v1.clone()
    print(f"v5 (clone of v1): {v5.elementData[:v5.size()]}")

    # Testing copyInto
    print("Testing copyInto...")
    array = [None] * v1.size()
    v1.copyInto(array)
    print(f"Array after copyInto: {array}")

    # Testing elementAt
    print("Testing elementAt...")
    print(f"Element at index 2: {v1.elementAt(2)}")

    # Testing elements (returning iterator)
    print("Testing elements (iterator)...")
    elements = v1.elements()
    print("Elements in v1:", end=" ")
    for e in elements:
        print(e, end=" ")
    print()

    # Testing firstElement and lastElement
    print("Testing firstElement and lastElement...")
    print(f"First element: {v1.firstElement()}")
    print(f"Last element: {v1.lastElement()}")

    # Testing get
    print("Testing get...")
    print(f"Element at index 3: {v1.get(3)}")

    # Testing indexOf and lastIndexOf
    print("Testing indexOf and lastIndexOf...")
    v1.add(3)  # Adding duplicate to test lastIndexOf
    print(f"Index of 3: {v1.indexOf(3)}")
    print(f"Last index of 3: {v1.lastIndexOf(3)}")

    # Testing isEmpty
    print("Testing isEmpty...")
    print(f"v1 is empty: {v1.isEmpty()}")
    v1.clear()
    print(f"v1 is empty after clear: {v1.isEmpty()}")

    # Testing iterator
    print("Testing iterator...")
    v1.addAll([10, 20, 30])
    iterator = v1.iterator()
    print("Elements in v1:", end=" ")
    for e in iterator:
        print(e, end=" ")
    print()

    # Testing listIterator (simplified as iterator)
    print("Testing listIterator...")
    list_iter = v1.listIterator()
    print("Elements in v1 using listIterator:", end=" ")
    for e in list_iter:
        print(e, end=" ")
    print()

    # Testing remove by index and element
    print("Testing remove by index and element...")
    v1.addAll([40, 50, 60])
    print(f"v1 before remove(2): {v1.elementData[:v1.size()]}")
    v1.remove(2)
    print(f"v1 after remove(2): {v1.elementData[:v1.size()]}")
    v1.removeElement(50)
    print(f"v1 after remove element 50: {v1.elementData[:v1.size()]}")

    # Testing removeAll
    print("Testing removeAll...")
    v1.removeAll([10, 60])
    print(f"v1 after removeAll [10, 60]: {v1.elementData[:v1.size()]}")

    # Testing removeAllElements
    print("Testing removeAllElements...")
    v1.removeAllElements()
    print(f"v1 after removeAllElements: {v1.elementData[:v1.size()]}")

    # Testing removeElement
    print("Testing removeElement...")
    v1.addAll([100, 200, 300])
    v1.removeElement(200)
    print(f"v1 after removeElement 200: {v1.elementData[:v1.size()]}")

    # Testing removeElementAt
    print("Testing removeElementAt...")
    v1.removeElementAt(1)
    print(f"v1 after removeElementAt index 1: {v1.elementData[:v1.size()]}")

    # Testing removeIf
    print("Testing removeIf...")
    v1.addAll([400, 500, 600])
    v1.removeIf(lambda x: x > 500)
    print(f"v1 after removeIf elements > 500: {v1.elementData[:v1.size()]}")

    # Testing retainAll
    print("Testing retainAll...")
    v1.addAll([700, 800, 900])
    try:
        v1.retainAll([300, 700, 800])
    except Exception as e:
        print(f"An error occurred: {e}")
    print(f"v1 after retainAll [300, 700, 800]: {v1.elementData[:v1.size()]}")

    # Testing set
    print("Testing set...")
    v1.set(1, 1000)
    print(f"v1 after set index 1 to 1000: {v1.elementData[:v1.size()]}")

    # Testing setElementAt
    print("Testing setElementAt...")
    v1.setElementAt(1100, 2)
    print(f"v1 after setElementAt index 2 to 1100: {v1.elementData[:v1.size()]}")

    # Testing setSize
    print("Testing setSize...")
    v1.setSize(5)
    print(f"v1 after setSize to 5: {v1.elementData[:v1.size()]}")

    # Testing size
    print("Testing size...")
    print(f"v1 size: {v1.size()}")

    # Testing sort
    print("Testing sort...")
    v1.sort(lambda x: x if x is not None else 0)
    print(f"v1 after sort: {v1.elementData[:v1.size()]}")

    # Testing spliterator
    print("Testing spliterator...")
    spliterator = v1.spliterator()
    print("Elements in v1 using spliterator:", end=" ")
    for e in spliterator:
        print(e, end=" ")
    print()

    # Testing subList
    print("Testing subList...")
    sub_list = v1.subList(1, 3)
    print(f"Sublist of v1 from index 1 to 3: {sub_list}")

    # Testing toArray
    print("Testing toArray...")
    array = v1.toArray()
    print(f"Array from v1: {array}")

    # Testing trimToSize
    print("Testing trimToSize...")
    v1.trimToSize()
    print(f"v1 after trimToSize: {len(v1.elementData)} (capacity)")

    # Testing parallelStream
    print("Testing parallelStream...")
    parallel_stream = v1.parallelStream()
    print("Elements in v1 using parallelStream:", end=" ")
    for e in parallel_stream:
        print(e, end=" ")
    print()

    # Testing stream
    print("Testing stream...")
    stream = v1.stream()
    print("Elements in v1 using stream:", end=" ")
    for e in stream:
        print(e, end=" ")
    print()


def test_stack():
    # Test stack functionality with integers
    stack_int = Stack()
    print("Is stack empty (int)?", stack_int.empty())  # Should be True

    # Push elements
    stack_int.push(10)
    stack_int.push(20)
    stack_int.push(30)
    print("Stack after pushing 10, 20, 30 (int):", stack_int.toArray())  # [10, 20, 30]

    # Peek and pop
    print("Peek top of stack (int):", stack_int.peek())  # 30
    print("Pop top of stack (int):", stack_int.pop())  # 30
    print("Stack after pop (int):", stack_int.toArray())  # [10, 20]

    # Search in stack
    print("Search 10 in stack (int):", stack_int.search(10))  # 2 (2nd from the top)
    print("Search 100 (not in stack) (int):", stack_int.search(100))  # -1 (not found)

    # Testing with strings
    stack_str = Stack()
    stack_str.push("apple")
    stack_str.push("banana")
    stack_str.push("cherry")
    print("Stack after pushing apple, banana, cherry (str):", stack_str.toArray())  # ['apple', 'banana', 'cherry']

    # Peek and pop with strings
    print("Peek top of stack (str):", stack_str.peek())  # 'cherry'
    print("Pop top of stack (str):", stack_str.pop())  # 'cherry'
    print("Stack after pop (str):", stack_str.toArray())  # ['apple', 'banana']

    # Search in string stack
    print("Search 'apple' in stack (str):", stack_str.search("apple"))  # 2
    print("Search 'orange' (not in stack) (str):", stack_str.search("orange"))  # -1

    # Testing with custom objects
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

        def __eq__(self, other):
            return self.name == other.name and self.age == other.age

        def __repr__(self):
            return f"Person({self.name}, {self.age})"

    person1 = Person("John", 30)
    person2 = Person("Jane", 25)
    person3 = Person("Alice", 28)

    stack_obj = Stack()
    stack_obj.push(person1)
    stack_obj.push(person2)
    stack_obj.push(person3)
    print("Stack after pushing person1, person2, person3 (object):", stack_obj.toArray())  # [person1, person2, person3]

    # Peek and pop with objects
    print("Peek top of stack (object):", stack_obj.peek())  # person3
    print("Pop top of stack (object):", stack_obj.pop())  # person3
    print("Stack after pop (object):", stack_obj.toArray())  # [person1, person2]

    # Search in object stack
    print("Search person1 in stack (object):", stack_obj.search(person1))  # 2
    print("Search non-existent person (object):", stack_obj.search(Person("Bob", 40)))  # -1

    # Now testing some Vector methods inherited by Stack

    # Add elements using addAll (for example with integers)
    stack_int.addAll([40, 50])
    print("Stack after addAll([40, 50]) (int):", stack_int.toArray())  # [10, 20, 40, 50]

    # Set element at index 1
    stack_int.setElementAt(99, 1)
    print("Stack after setElementAt(99, 1) (int):", stack_int.toArray())  # [10, 99, 40, 50]

    # Remove element by index
    print("Remove element at index 2 (int):", stack_int.removeElementAt(2))  # Removes 40
    print("Stack after removeElementAt(2) (int):", stack_int.toArray())  # [10, 99, 50]

    # Copy elements to an array
    copy_array = [None] * 3
    stack_int.copyInto(copy_array)
    print("Copied stack (int) to array:", copy_array)  # [10, 99, 50]

    # Get first and last element
    print("First element (int):", stack_int.firstElement())  # 10
    print("Last element (int):", stack_int.lastElement())  # 50

    # Remove all elements
    stack_int.removeAllElements()
    print("Stack after removeAllElements (int):", stack_int.toArray())  # []

def test_queue():
    # Using ArrayList
    queue_with_array_list = Queue(ArrayList())

    queue_with_array_list.offer(100)  # Adds element
    queue_with_array_list.offer(200)

    print(queue_with_array_list.element())  # Output: 100 (Retrieves head without removing)
    print(queue_with_array_list.poll())  # Output: 100 (Removes head)
    print(queue_with_array_list.element())  # Output: 200

    # Access the underlying ArrayList and call a specific method
    array = queue_with_array_list.getList()

    # You can now call any ArrayList specific methods
    print(array.size())  # Output: 2 (ArrayList-specific method)
    print(array.isEmpty())  # Output: False

    # Using LinkedList
    queue_with_linked_list = Queue(LinkedList())

    queue_with_linked_list.offer(100)
    queue_with_linked_list.offer(200)

    # Access the underlying LinkedList and call specific methods
    linked = queue_with_linked_list.getList()

    # You can now call any LinkedList specific methods
    linked.addFirst(50)  # LinkedList-specific method
    print(linked.getFirst())  # Output: 50 (LinkedList-specific method)

def test_priorityQ():
    # Create PriorityQueue without comparator
    pq = PriorityQueue()

    # Test add and offer methods
    pq.add(10)
    pq.offer(5)
    pq.add(20)

    print(f"Queue size after adding elements: {pq.size()}")  # Expected: 3

    # Test peek method
    peek_value = pq.peek()
    print(f"Peek value: {peek_value}")  # Expected: 5

    # Test poll method
    poll_value = pq.poll()
    print(f"Poll value: {poll_value}")  # Expected: 5
    print(f"Queue size after polling: {pq.size()}")  # Expected: 2

    # Test remove method
    pq.remove(10)
    print(f"Queue size after removing element: {pq.size()}")  # Expected: 1

    # Test isEmpty method
    is_empty = pq.isEmpty()
    print(f"Queue is empty: {is_empty}")  # Expected: False

    # Test contains method
    contains_20 = pq.contains(20)
    print(f"Queue contains 20: {contains_20}")  # Expected: True

    # Test clear method
    pq.clear()
    print(f"Queue is empty after clearing: {pq.isEmpty()}")  # Expected: True

    # Test addAll method
    pq.addAll([10, 30, 50])
    print(f"Queue size after addAll: {pq.size()}")  # Expected: 3

    # Test toArray method
    array = pq.toArray()
    print(f"Array representation: {array}")  # Expected: [10, 30, 50]

    # Test removeAll method
    pq.removeAll([10, 50])
    print(f"Queue size after removeAll: {pq.size()}")  # Expected: 1
    print(f"Queue contains 30: {pq.contains(30)}")  # Expected: True

    # Test retainAll method
    pq.addAll([40, 60])
    pq.retainAll([30, 60])
    print(f"Queue size after retainAll: {pq.size()}")  # Expected: 2
    print(f"Queue contains 30: {pq.contains(30)}")  # Expected: True
    print(f"Queue contains 60: {pq.contains(60)}")  # Expected: True

    # Test removeIf method
    pq.add(70)
    pq.removeIf(lambda x: x > 60)
    print(f"Queue contains 70 after removeIf: {pq.contains(70)}")  # Expected: False

    # Test equals method
    pq2 = PriorityQueue()
    pq2.addAll([30, 60])
    are_equal = pq.equals(pq2)
    print(f"Queues are equal: {are_equal}")  # Expected: True

    # Test hashCode method
    hash_code1 = pq.hashCode()
    hash_code2 = pq2.hashCode()
    print(f"Hash codes are equal: {hash_code1 == hash_code2}")  # Expected: True

    # Test iterator method
    iterated = list(iter(pq))
    print(f"Iterator result: {iterated}")  # Expected: [30, 60]

    print("All API checks completed!")

def test_deque():
    dq = ArrayDeque()

    # Test add, addFirst, addLast
    dq.add(10)
    dq.addFirst(5)
    dq.addLast(20)
    dq.addAll([25, 30, 40])
    print("After add, addFirst, addLast:", list(dq))

    # Test size
    print("Size:", dq.size())

    # Test contains
    print("Contains 10:", dq.contains(10))

    # Test getFirst and getLast
    print("First Element:", dq.getFirst())
    print("Last Element:", dq.getLast())

    # Test peek, peekFirst, peekLast
    print("Peek:", dq.peek())
    print("Peek First:", dq.peekFirst())
    print("Peek Last:", dq.peekLast())

    # Test poll, pollFirst, pollLast
    print("Poll:", dq.poll())
    print("Poll First:", dq.pollFirst())
    print("Poll Last:", dq.pollLast())
    print("After poll, pollFirst, pollLast:", list(dq))

    # Test push, pop
    dq.push(30)
    print("After push 30:", list(dq))
    print("Pop:", dq.pop())
    print("After pop:", list(dq))

    # Test remove, removeFirst, removeLast
    dq.add(40)
    dq.add(50)
    dq.remove(40)
    print("After remove 40:", list(dq))
    dq.removeFirst()
    print("After removeFirst:", list(dq))
    dq.removeLast()
    print("After removeLast:", list(dq))

    # Test addAll
    dq.addAll([60, 70, 80])
    print("After addAll:", list(dq))

    # Test clear
    dq.clear()
    print("After clear:", list(dq))


def test_hashset():
    # Initialize a HashSet
    hs = HashSet()

    print("### Testing add() ###")
    print("Adding 1:", hs.add(1))  # True
    print("Adding 2:", hs.add(2))  # True
    print("Adding 1 again:", hs.add(1))  # False
    print("HashSet:", hs)  # {1, 2}

    print("\n### Testing addAll() ###")
    hs.addAll([3, 4, 5])
    print("Added [3, 4, 5]:", hs)  # {1, 2, 3, 4, 5}

    print("\n### Testing contains() ###")
    print("Contains 3:", hs.contains(3))  # True
    print("Contains 6:", hs.contains(6))  # False

    print("\n### Testing remove() ###")
    print("Removing 2:", hs.remove(2))  # True
    print("Removing 6 (non-existing):", hs.remove(6))  # False
    print("HashSet after remove:", hs)  # {1, 3, 4, 5}

    print("\n### Testing size() ###")
    print("Size of HashSet:", hs.size())  # 4

    print("\n### Testing iterator() ###")
    print("Iterating over HashSet:")
    for item in hs.iterator():
        print(item)

    print("\n### Testing removeAll() ###")
    hs.removeAll([1, 4])
    print("After removeAll([1, 4]):", hs)  # {3, 5}

    print("\n### Testing retainAll() ###")
    hs.retainAll([3, 6])
    print("After retainAll([3, 6]):", hs)  # {3}

    print("\n### Testing clear() ###")
    hs.clear()
    print("After clear():", hs)  # {}

    print("\n### Testing isEmpty() ###")
    print("Is HashSet empty?", hs.isEmpty())  # True

    print("\n### Testing toArray() ###")
    hs.addAll([7, 8, 9])
    arr = hs.toArray()
    print("Array from HashSet:", arr)  # [7, 8, 9]

    print("\n### Testing clone() ###")
    hs_clone = hs.clone()
    print("Cloned HashSet:", hs_clone)  # {7, 8, 9}

    print("\n### Testing removeIf() ###")
    hs_clone.removeIf(lambda x: x % 2 == 0)
    print("After removeIf (removes evens):", hs_clone)  # {7, 9}

    print("\n### Testing stream() ###")
    print("Streaming (iterating) HashSet:")
    for item in hs.stream():
        print(item)

    print("\n### Testing parallelStream() ###")
    print("Parallel stream (iterating) HashSet:")
    for item in hs.parallelStream():
        print(item)

    print("\n### Testing equals() and hashCode() ###")
    hs2 = HashSet()
    hs2.addAll([7, 8, 9])
    print("HashSet equals hs2:", hs.equals(hs2))  # True
    print("HashSet hashCode:", hs.hashCode())  # Hash code of {7, 8, 9}


def test_linked_hash_set():
    # Initialize a LinkedHashSet
    lhs = LinkedHashSet()

    print("### Testing add() ###")
    print("Adding 1:", lhs.add(1))  # True
    print("Adding 2:", lhs.add(2))  # True
    print("Adding 1 again:", lhs.add(1))  # False
    print("LinkedHashSet:", lhs)  # [1, 2]

    print("\n### Testing addAll() ###")
    lhs.addAll([3, 4, 5])
    print("Added [3, 4, 5]:", lhs)  # [1, 2, 3, 4, 5]

    print("\n### Testing contains() ###")
    print("Contains 3:", lhs.contains(3))  # True
    print("Contains 6:", lhs.contains(6))  # False

    print("\n### Testing remove() ###")
    print("Removing 2:", lhs.remove(2))  # True
    print("Removing 6 (non-existing):", lhs.remove(6))  # False
    print("LinkedHashSet after remove:", lhs)  # [1, 3, 4, 5]

    print("\n### Testing size() ###")
    print("Size of LinkedHashSet:", lhs.size())  # 4

    print("\n### Testing iterator() ###")
    print("Iterating over LinkedHashSet:")
    for item in lhs.iterator():
        print(item)

    print("\n### Testing removeAll() ###")
    lhs.removeAll([1, 4])
    print("After removeAll([1, 4]):", lhs)  # [3, 5]

    print("\n### Testing retainAll() ###")
    lhs.retainAll([3, 6])
    print("After retainAll([3, 6]):", lhs)  # [3]

    print("\n### Testing clear() ###")
    lhs.clear()
    print("After clear():", lhs)  # []

    print("\n### Testing isEmpty() ###")
    print("Is LinkedHashSet empty?", lhs.isEmpty())  # True

    print("\n### Testing toArray() ###")
    lhs.addAll([7, 8, 9])
    arr = lhs.toArray()
    print("Array from LinkedHashSet:", arr)  # [7, 8, 9]

    print("\n### Testing clone() ###")
    lhs_clone = lhs.clone()
    print("Cloned LinkedHashSet:", lhs_clone)  # [7, 8, 9]

    print("\n### Testing removeIf() ###")
    lhs_clone.removeIf(lambda x: x % 2 == 0)
    print("After removeIf (removes evens):", lhs_clone)  # [7, 9]

    print("\n### Testing stream() ###")
    print("Streaming (iterating) LinkedHashSet:")
    for item in lhs.stream():
        print(item)

    print("\n### Testing parallelStream() ###")
    print("Parallel stream (iterating) LinkedHashSet:")
    for item in lhs.parallelStream():
        print(item)

    print("\n### Testing equals() and hashCode() ###")
    lhs2 = LinkedHashSet()
    lhs2.addAll([7, 8, 9])
    print("LinkedHashSet equals lhs2:", lhs.equals(lhs2))  # True
    print("LinkedHashSet hashCode:", lhs.hashCode())  # Hash code of [7, 8, 9]


def test_tree_set():
    ts = TreeSet()

    # Adding elements
    ts.add(10)
    ts.add(5)
    ts.add(15)
    ts.add(7)

    print("TreeSet elements after adding: ", list(ts.iterator()))

    # Test first and last
    print("First element: ", ts.first())
    print("Last element: ", ts.last())

    # Test ceiling and floor
    print("Ceiling of 8: ", ts.ceiling(8))

    # Test headSet, subSet, and tailSet
    print("HeadSet (<10): ", ts.headSet(10))
    print("SubSet (5, 15): ", ts.subSet(5, 15))
    print("TailSet (>=7): ", ts.tailSet(7))

    # Test removeIf, removeAll, retainAll, containsAll
    ts.removeIf(lambda x: x % 2 == 0)
    print("TreeSet after removeIf (remove even): ", list(ts.iterator()))

    ts.addAll([4, 6, 7])
    ts.removeAll([7, 6])
    print("TreeSet after removeAll (remove 7, 6): ", list(ts.iterator()))

    ts.addAll([4, 8, 9])
    ts.retainAll([4, 9])
    print("TreeSet after retainAll (retain 4, 9): ", list(ts.iterator()))

    # Poll first and last
    print("Poll first: ", ts.pollFirst())
    print("Poll last: ", ts.pollLast())

    print("Final TreeSet: ", list(ts.iterator()))

def test_hashmap():
    print("### HashMap Usage Test ###")

    # Create a new HashMap
    hmap = HashMap[int, str]()
    print("\nCreated a new HashMap")

    # Test put and get methods
    hmap.put(1, "one")
    hmap.put(2, "two")
    print(f"\nPut: (1, 'one'), (2, 'two')")
    print(f"Get key 1: {hmap.get(1)}")
    print(f"Get key 2: {hmap.get(2)}")

    # Test containsKey and containsValue
    print(f"\nContains key 1? {hmap.containsKey(1)}")
    print(f"Contains value 'one'? {hmap.containsValue('one')}")
    print(f"Contains key 3? {hmap.containsKey(3)}")

    # Test size and isEmpty
    print(f"\nCurrent size: {hmap.size()}")
    print(f"Is map empty? {hmap.isEmpty()}")

    # Test keySet and values
    print(f"\nKeys in the map: {hmap.keySet()}")
    print(f"Values in the map: {list(hmap.values())}")

    # Test putIfAbsent and remove
    print("\nPutting key 3 with value 'three'")
    hmap.putIfAbsent(3, "three")
    print(f"Get key 3 after putIfAbsent: {hmap.get(3)}")
    print("Removing key 3")
    hmap.remove(3)
    print(f"Get key 3 after removal: {hmap.get(3)}")

    # Test compute and computeIfAbsent
    print("\nUpdating value for key 2 using compute")
    hmap.compute(2, lambda k, v: v + "_updated")
    print(f"Updated value for key 2: {hmap.get(2)}")
    print("Using computeIfAbsent to set key 3 with 'three_new'")
    hmap.computeIfAbsent(3, lambda k: "three_new")
    print(f"Get key 3 after computeIfAbsent: {hmap.get(3)}")

    # Test entrySet with MapEntry
    print("\nEntry set of the map (key-value pairs):")
    entry_set = hmap.entrySet()
    for entry in entry_set:
        print(f"Key: {entry.getKey()}, Value: {entry.getValue()}")

    # Test clear
    print("\nClearing the map")
    hmap.clear()
    print(f"Map size after clear: {hmap.size()}")
    print(f"Is map empty after clear? {hmap.isEmpty()}")
    print("### End of HashMap Usage Test ###")

def test_linked_hash_map():
    print("### LinkedHashMap Usage Test ###")

    # Create a new LinkedHashMap with default capacity and load factor
    lmap = LinkedHashMap()
    print("\nCreated a new LinkedHashMap")

    # Test put and get methods
    lmap.put(1, "one")
    lmap.put(2, "two")
    lmap.put(3, "three")
    print(f"\nPut: (1, 'one'), (2, 'two'), (3, 'three')")
    print(f"Get key 1: {lmap.get(1)}")
    print(f"Get key 2: {lmap.get(2)}")

    # Test containsKey and containsValue
    print(f"\nContains key 1? {lmap.containsKey(1)}")
    print(f"Contains value 'one'? {lmap.containsValue('one')}")
    print(f"Contains key 4? {lmap.containsKey(4)}")

    # Test keySet and values
    print(f"\nKeys in the LinkedHashMap: {lmap.keySet()}")
    print(f"Values in the LinkedHashMap: {list(lmap.values())}")

    # Test remove and clear
    print("\nRemoving key 2")
    lmap.remove(2)
    print(f"Get key 2 after removal: {lmap.get(2)}")

    # Test isEmpty
    print(f"\nIs LinkedHashMap empty? {lmap.isEmpty()}")

    # Test putAll
    print("\nTesting putAll method")
    map_to_add = HashMap()  # Use HashMap instead of dict
    map_to_add.put(4, "four")
    map_to_add.put(5, "five")
    lmap.putAll(map_to_add)
    print(f"After putAll: {lmap.keySet()}")

    # Test putIfAbsent
    print("\nTesting putIfAbsent method")
    lmap.putIfAbsent(6, "six")
    lmap.putIfAbsent(1, "new_one")
    print(f"PutIfAbsent key 6 (new key): {lmap.get(6)}")
    print(f"PutIfAbsent key 1 (existing key): {lmap.get(1)}")

    # Test size
    print(f"\nSize of LinkedHashMap: {lmap.size()}")

    # Test clone (simulated)
    lmap_clone = lmap.clone()
    print("\nTesting clone method")
    print(f"Cloned LinkedHashMap: {lmap_clone}")

    # Test access order
    lmap = LinkedHashMap(access_order=True)
    print("\nCreated a LinkedHashMap with access order")
    lmap.put(1, "one")
    lmap.put(2, "two")
    lmap.put(3, "three")
    print(f"Keys before accessing any entry: {lmap.keySet()}")

    # Accessing key 1 should move it to the end
    lmap.get(1)
    print(f"Keys after accessing key 1: {lmap.keySet()}")

    # Test entrySet
    print("\nEntry set of the map:")
    entry_set = lmap.entrySet()
    for entry in entry_set:
        print(f"Key: {entry.getKey()}, Value: {entry.getValue()}")

    # Test replaceAll
    print("\nReplacing all values using replaceAll method")
    lmap.replaceAll(lambda k, v: v + "_updated")
    print(f"Values in the LinkedHashMap after replaceAll: {list(lmap.values())}")

    # Test compute, computeIfAbsent, computeIfPresent
    print("\nTesting compute, computeIfAbsent, and computeIfPresent methods")
    lmap.compute(1, lambda k, v: v + "_computed" if v else "computed_value")
    lmap.computeIfAbsent(4, lambda k: "computedAbsent")
    lmap.computeIfPresent(5, lambda k, v: v + "_computedPresent")
    print(f"Computed key 1: {lmap.get(1)}")
    print(f"ComputedIfAbsent key 4: {lmap.get(4)}")
    print(f"ComputedIfPresent key 5: {lmap.get(5)}")

    # Test merge
    print("\nTesting merge method")
    lmap.merge(6, "merged_value", lambda v1, v2: v1 + "_" + v2)
    lmap.merge(1, "new_value", lambda v1, v2: v1 + "_" + v2)
    print(f"Merge key 6 (new key): {lmap.get(6)}")
    print(f"Merge key 1 (existing key): {lmap.get(1)}")

    # Test remove (with value) and replace methods
    print("\nTesting remove with value and replace methods")
    lmap.removeIf(6, "merged_value")  # Should not remove as value differs
    print(f"Remove key 6 with wrong value: {lmap.get(6)}")
    lmap.removeIf(6, "merged_value_new")  # Should remove as value matches
    print(f"Remove key 6 with correct value: {lmap.get(6)}")
    lmap.replace(1, "one_updated")
    print(f"Replace key 1 value: {lmap.get(1)}")

    print("### End of LinkedHashMap Usage Test ###")

def test_hashtable():
    # Initialize with default constructor
    table = Hashtable()

    print("Created a new Hashtable")

    # Test put operation
    table.put(1, 'one')
    table.put(2, 'two')
    table.put(3, 'three')
    print(f"Put: (1, 'one'), (2, 'two'), (3, 'three')")

    # Test get operation
    print(f"Get key 1: {table.get(1)}")
    print(f"Get key 2: {table.get(2)}")

    # Test contains operations
    print(f"Contains key 1? {table.containsKey(1)}")
    print(f"Contains value 'one'? {table.containsValue('one')}")
    print(f"Contains key 4? {table.containsKey(4)}")

    # Test entrySet, keySet, and values
    print(f"Keys in the Hashtable: {table.keySet()}")
    print(f"Values in the Hashtable: {list(table.values())}")

    # Test remove operation
    print(f"Removing key 2: {table.remove(2)}")
    print(f"Get key 2 after removal: {table.get(2)}")

    # Test isEmpty and size
    print(f"Is Hashtable empty? {table.isEmpty()}")
    print(f"Size of Hashtable: {table.size()}")

    # Test putAll operation
    other_map = Hashtable()
    other_map.put(4, 'four')
    other_map.put(5, 'five')
    table.putAll(other_map)
    print(f"After putAll: {table.keySet()}")

    # Test putIfAbsent
    print(f"PutIfAbsent key 6 (new key): {table.putIfAbsent(6, 'six')}")
    print(f"PutIfAbsent key 1 (existing key): {table.putIfAbsent(1, 'new_one')}")

    # Test compute, computeIfAbsent, and computeIfPresent
    table.compute(1, lambda k, v: f'{v}_computed')
    print(f"Computed key 1: {table.get(1)}")
    table.computeIfAbsent(7, lambda k: 'computedAbsent')
    print(f"ComputedIfAbsent key 7: {table.get(7)}")
    table.computeIfPresent(5, lambda k, v: f'{v}_present')
    print(f"ComputedIfPresent key 5: {table.get(5)}")

    # Test merge operation
    table.merge(6, 'merged_value', lambda v1, v2: f'{v1}_new_value')
    print(f"Merge key 6 (existing key): {table.get(6)}")

    # Test clone
    cloned_table = table.clone()
    print(f"Cloned Hashtable: {cloned_table.keySet()}")

    # Test rehash
    table.rehash()
    print("Rehashed Hashtable")


def test_treemap():
    # Instantiate the TreeMap
    tree_map = TreeMap()

    # Add some key-value pairs
    print("Adding key-value pairs:")
    tree_map.put(1, "One")
    tree_map.put(3, "Three")
    tree_map.put(2, "Two")
    print(f"Map after adding entries: {tree_map}")

    # Get the size of the map
    size = tree_map.size()
    print(f"Size of the map: {size}")

    # Accessing first and last keys
    first_key = tree_map.firstKey()
    last_key = tree_map.lastKey()
    print(f"First key: {first_key}")
    print(f"Last key: {last_key}")

    # Get a submap view of the TreeMap
    sub_map = tree_map.subMap(1, 3)
    print(f"Submap from 1 to 3: {sub_map}")

    # Getting ceiling entry for a key
    ceiling_entry = tree_map.ceilingEntry(2)
    print(f"Ceiling entry for key 2: {ceiling_entry}")

    # Removing an entry
    removed_value = tree_map.remove(2)
    print(f"Removed entry with key 2, value: {removed_value}")
    print(f"Map after removal: {tree_map}")

    # Iterating through the map
    print("Iterating through the map:")
    tree_map.forEach(lambda k, v: print(f"Key: {k}, Value: {v}"))

    # Get descending order view
    descending_map = tree_map.descendingMap()
    print(f"Descending map: {descending_map}")

    # Clone the map
    cloned_map = tree_map.clone()
    print(f"Cloned map: {cloned_map}")

    # Replace values
    replaced_value = tree_map.replace(3, "ThreeUpdated")
    print(f"Replaced value for key 3, old value: {replaced_value}")
    print(f"Map after replacement: {tree_map}")

    # Poll first and last entries
    poll_first = tree_map.pollFirstEntry()
    poll_last = tree_map.pollLastEntry()
    print(f"Polled first entry: {poll_first}")
    print(f"Polled last entry: {poll_last}")
    print(f"Map after polling: {tree_map}")

    # Additional test scenarios
    print("Additional test scenarios:")

    # Test with an empty map
    empty_map = TreeMap()
    print(f"Empty map: {empty_map}")

    try:
        empty_first_key = empty_map.firstKey()
    except KeyError as e:
        print(f"Error accessing first key in empty map: {e}")

    try:
        empty_last_key = empty_map.lastKey()
    except KeyError as e:
        print(f"Error accessing last key in empty map: {e}")

    # Adding more entries to test
    empty_map.put(10, "Ten")
    empty_map.put(5, "Five")
    empty_map.put(7, "Seven")
    print(f"Map after adding more entries: {empty_map}")

    # Testing subMap and headMap on populated map
    test_sub_map = empty_map.subMap(5, 10)
    print(f"Submap from 5 to 10: {test_sub_map}")

    test_head_map = empty_map.headMap(7)
    print(f"Head map up to 7: {test_head_map}")

    test_tail_map = empty_map.tailMap(5)
    print(f"Tail map from 5: {test_tail_map}")

    # Testing removal of non-existent key
    non_existent_removal = empty_map.remove(100)
    print(f"Remove non-existent key 100: {non_existent_removal}")
