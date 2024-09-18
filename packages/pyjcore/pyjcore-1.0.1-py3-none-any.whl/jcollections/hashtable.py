from typing import Optional, Set, Collection, Any, TypeVar
from collections import defaultdict
from threading import RLock

from jcollections.map import Map

K = TypeVar('K')  # Type variable for keys
V = TypeVar('V')  # Type variable for values

class Hashtable(Map[K, V]):
    """
    A thread-safe implementation of a hash table (dictionary) that uses locks to ensure thread safety.

    Inherits from the `Map` interface and provides implementations for key-value storage, retrieval,
    and other map operations. The hash table is initially empty and can be populated with an optional
    initial set of data.

    Attributes:
        _table (defaultdict): Internal dictionary to store key-value pairs.
        _lock (RLock): Reentrant lock to ensure thread safety.
        _capacity (int): The initial capacity of the hash table (not directly used in this implementation).
        _load_factor (float): The load factor for the hash table (not directly used in this implementation).
        _size (int): The number of key-value pairs currently in the hash table.
    """

    def __init__(self, initial_capacity: int = 11, load_factor: float = 0.75, data: Optional[Map[K, V]] = None):
        """
        Constructs a new Hashtable with the specified initial capacity, load factor, and optional initial data.

        :param initial_capacity: The initial capacity of the hash table (default is 11).
        :param load_factor: The load factor for resizing the hash table (default is 0.75).
        :param data: Optional map containing initial key-value pairs to populate the hash table.
        """
        self._table = defaultdict(lambda: None)
        self._lock = RLock()
        self._capacity = initial_capacity
        self._load_factor = load_factor
        self._size = 0
        if data:
            self.putAll(data)

    def clear(self) -> None:
        """
        Removes all entries from the hash table and resets the size to 0.
        """
        with self._lock:
            self._table.clear()
            self._size = 0

    def containsKey(self, key: K) -> bool:
        """
        Checks if the hash table contains the specified key.

        :param key: The key to check for.
        :return: True if the key is present, False otherwise.
        """
        with self._lock:
            return key in self._table

    def containsValue(self, value: V) -> bool:
        """
        Checks if the hash table contains the specified value.

        :param value: The value to check for.
        :return: True if the value is present, False otherwise.
        """
        with self._lock:
            return value in self._table.values()

    def entrySet(self) -> Set[Any]:
        """
        Returns a set of all key-value pairs in the hash table.

        :return: A set of (key, value) tuples representing all entries.
        """
        with self._lock:
            return set(self._table.items())

    def get(self, key: K) -> Optional[V]:
        """
        Retrieves the value associated with the specified key.

        :param key: The key to retrieve the value for.
        :return: The value associated with the key, or None if the key is not present.
        """
        with self._lock:
            return self._table.get(key, None)

    def isEmpty(self) -> bool:
        """
        Checks if the hash table is empty.

        :return: True if the hash table contains no entries, False otherwise.
        """
        with self._lock:
            return self._size == 0

    def keySet(self) -> Set[K]:
        """
        Returns a set of all keys in the hash table.

        :return: A set of keys.
        """
        with self._lock:
            return set(self._table.keys())

    def put(self, key: K, value: V) -> Optional[V]:
        """
        Associates the specified value with the specified key in the hash table.

        If the key already exists, the old value is replaced with the new value.

        :param key: The key with which the value is to be associated.
        :param value: The value to associate with the key.
        :return: The previous value associated with the key, or None if there was no previous value.
        """
        with self._lock:
            old_value = self._table.get(key)
            if old_value is None:
                self._size += 1
            self._table[key] = value
            return old_value

    def putAll(self, jmap: Map[K, V]) -> None:
        """
        Copies all key-value pairs from the specified map to this hash table.

        :param jmap: The map whose mappings are to be copied.
        """
        with self._lock:
            for key in jmap.keySet():
                self.put(key, jmap.get(key))

    def remove(self, key: K) -> Optional[V]:
        """
        Removes the mapping for the specified key if it exists.

        :param key: The key whose mapping is to be removed.
        :return: The previous value associated with the key, or None if there was no mapping.
        """
        with self._lock:
            old_value = self._table.pop(key, None)
            if old_value is not None:
                self._size -= 1
            return old_value

    def size(self) -> int:
        """
        Returns the number of key-value pairs in the hash table.

        :return: The number of entries in the hash table.
        """
        with self._lock:
            return self._size

    def values(self) -> Collection[V]:
        """
        Returns a collection of all values in the hash table.

        :return: A collection of values.
        """
        with self._lock:
            return self._table.values()

    def clone(self) -> 'Hashtable[K, V]':
        """
        Creates a shallow copy of this hash table.

        :return: A new Hashtable instance containing the same key-value pairs.
        """
        with self._lock:
            return Hashtable(data=self)

    def rehash(self) -> None:
        """
        Rehashes the internal table. This method is a placeholder for resizing or reorganizing the table
        if needed. The current implementation simply reassigns the internal table to a new defaultdict.
        """
        with self._lock:
            new_table = defaultdict(lambda: None)
            for key, value in self._table.items():
                new_table[key] = value
            self._table = new_table

    # Other default methods from the Map interface like compute, computeIfAbsent, etc. are inherited.
