from typing import TypeVar, Dict, Set, Collection, Optional, Generic

from jcollections.map import Map
from jcollections.mapentry import MapEntry

# Define type variables for keys and values
K = TypeVar('K')  # Key type variable
V = TypeVar('V')  # Value type variable

class HashMap(Map[K, V], Generic[K, V]):
    """
    A basic hash map implementation that maps keys to values using a dictionary.

    Inherits from the `Map` class and provides methods to manage key-value pairs
    efficiently using a hash table. This implementation offers basic hash map functionalities.

    Attributes:
        store (Dict[K, V]): The underlying dictionary that stores key-value pairs.
        initial_capacity (int): The initial capacity of the hash map (default is 16).
        load_factor (float): The load factor for resizing the hash map (default is 0.75).
    """

    def __init__(self, initial_capacity: int = 16, load_factor: float = 0.75):
        """
        Initializes a new HashMap with the specified initial capacity and load factor.

        :param initial_capacity: The initial capacity of the hash map (default is 16).
        :param load_factor: The load factor for resizing the hash map (default is 0.75).
        """
        self.store: Dict[K, V] = {}  # Internal dictionary to store key-value pairs
        self.initial_capacity = initial_capacity  # Initial capacity of the hash map
        self.load_factor = load_factor  # Load factor for resizing

    def clear(self) -> None:
        """
        Clears all entries from the hash map.
        """
        self.store.clear()

    def containsKey(self, key: K) -> bool:
        """
        Checks if the hash map contains a mapping for the specified key.

        :param key: The key to check for presence in the hash map.
        :return: True if the hash map contains the key, False otherwise.
        """
        return key in self.store

    def containsValue(self, value: V) -> bool:
        """
        Checks if the hash map contains a mapping for the specified value.

        :param value: The value to check for presence in the hash map.
        :return: True if the hash map contains the value, False otherwise.
        """
        return value in self.store.values()

    def entrySet(self) -> Set[MapEntry[K, V]]:
        """
        Returns a set of MapEntry objects representing all key-value pairs in the hash map.

        :return: A set of MapEntry objects.
        """
        return {MapEntry(key, value) for key, value in self.store.items()}

    def get(self, key: K) -> Optional[V]:
        """
        Retrieves the value associated with the specified key.

        :param key: The key whose associated value is to be retrieved.
        :return: The value associated with the key, or None if the key is not present.
        """
        return self.store.get(key)

    def isEmpty(self) -> bool:
        """
        Checks if the hash map is empty.

        :return: True if the hash map is empty, False otherwise.
        """
        return len(self.store) == 0

    def keySet(self) -> Set[K]:
        """
        Returns a set of all keys in the hash map.

        :return: A set of keys.
        """
        return set(self.store.keys())

    def put(self, key: K, value: V) -> Optional[V]:
        """
        Associates the specified value with the specified key in the hash map.
        If the key is already present, it updates the value.

        :param key: The key with which the value is to be associated.
        :param value: The value to associate with the key.
        :return: The previous value associated with the key, or None if there was no previous value.
        """
        return self.store.setdefault(key, value)

    def putAll(self, jmap: 'Map[K, V]') -> None:
        """
        Copies all key-value mappings from the specified map to this hash map.

        :param jmap: The map whose mappings are to be copied.
        """
        for entry in jmap.entrySet():
            self.put(entry.getKey(), entry.getValue())

    def remove(self, key: K) -> Optional[V]:
        """
        Removes the mapping for the specified key from the hash map, if present.

        :param key: The key whose mapping is to be removed.
        :return: The previous value associated with the key, or None if the key was not present.
        """
        return self.store.pop(key, None)

    def size(self) -> int:
        """
        Returns the number of key-value pairs in the hash map.

        :return: The number of entries in the hash map.
        """
        return len(self.store)

    def values(self) -> Collection[V]:
        """
        Returns a collection of all values in the hash map.

        :return: A collection of values.
        """
        return self.store.values()

    def clone(self) -> 'HashMap[K, V]':
        """
        Creates a shallow copy of the hash map.

        :return: A new HashMap instance containing the same key-value pairs.
        """
        new_map = HashMap(self.initial_capacity, self.load_factor)
        new_map.store = self.store.copy()
        return new_map
