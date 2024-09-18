from typing import TypeVar, Generic, Callable, Optional, Set, Collection
from jcollections.mapentry import MapEntry

# Define type variables for keys and values
K = TypeVar('K')  # Key type variable
V = TypeVar('V')  # Value type variable

class SortedMap(Generic[K, V]):
    """
    Abstract base class for a sorted map that maintains its keys in a sorted order.

    Provides methods for accessing and manipulating key-value pairs in a sorted map.

    Methods:
        comparator: Returns the comparator used to order the keys, or None if natural ordering is used.
        firstKey: Returns the first (smallest) key in the map.
        lastKey: Returns the last (largest) key in the map.
        headMap: Returns a view of the map with keys less than the specified `toKey`.
        subMap: Returns a view of the map with keys between `fromKey` (inclusive) and `toKey` (exclusive).
        tailMap: Returns a view of the map with keys greater than or equal to the specified `fromKey`.
        entrySet: Returns a set of MapEntry objects representing all key-value pairs in the map.
        keySet: Returns a set of all keys in the map.
        values: Returns a collection of all values in the map.
        clear: Removes all entries from the map.
        containsKey: Checks if the map contains a mapping for the specified key.
        containsValue: Checks if the map contains a mapping for the specified value.
        get: Retrieves the value associated with the specified key.
        put: Associates the specified value with the specified key in the map.
        putAll: Copies all key-value mappings from the specified map to this map.
        remove: Removes the mapping for the specified key from the map.
        size: Returns the number of key-value pairs in the map.
        isEmpty: Checks if the map is empty.
    """

    def comparator(self) -> Optional[Callable[[K, K], int]]:
        """
        Returns the comparator used to order the keys, or None if natural ordering is used.

        :return: A callable that compares two keys, or None.
        """
        pass

    def firstKey(self) -> K:
        """
        Returns the first (smallest) key in the map.

        :return: The smallest key in the map.
        :raises: ValueError if the map is empty.
        """
        pass

    def lastKey(self) -> K:
        """
        Returns the last (largest) key in the map.

        :return: The largest key in the map.
        :raises: ValueError if the map is empty.
        """
        pass

    def headMap(self, toKey: K) -> 'SortedMap[K, V]':
        """
        Returns a view of the map with keys less than the specified `toKey`.

        :param toKey: The key up to which the view is to be created.
        :return: A view of the map with keys less than `toKey`.
        """
        pass

    def subMap(self, fromKey: K, toKey: K) -> 'SortedMap[K, V]':
        """
        Returns a view of the map with keys between `fromKey` (inclusive) and `toKey` (exclusive).

        :param fromKey: The starting key of the view (inclusive).
        :param toKey: The ending key of the view (exclusive).
        :return: A view of the map with keys between `fromKey` and `toKey`.
        """
        pass

    def tailMap(self, fromKey: K) -> 'SortedMap[K, V]':
        """
        Returns a view of the map with keys greater than or equal to the specified `fromKey`.

        :param fromKey: The key from which the view starts.
        :return: A view of the map with keys greater than or equal to `fromKey`.
        """
        pass

    def entrySet(self) -> Set[MapEntry[K, V]]:
        """
        Returns a set of MapEntry objects representing all key-value pairs in the map.

        :return: A set of MapEntry objects.
        """
        pass

    def keySet(self) -> Set[K]:
        """
        Returns a set of all keys in the map.

        :return: A set of keys.
        """
        pass

    def values(self) -> Collection[V]:
        """
        Returns a collection of all values in the map.

        :return: A collection of values.
        """
        pass

    def clear(self) -> None:
        """
        Removes all entries from the map.
        """
        pass

    def containsKey(self, key: K) -> bool:
        """
        Checks if the map contains a mapping for the specified key.

        :param key: The key to check for presence in the map.
        :return: True if the map contains the key, False otherwise.
        """
        pass

    def containsValue(self, value: V) -> bool:
        """
        Checks if the map contains a mapping for the specified value.

        :param value: The value to check for presence in the map.
        :return: True if the map contains the value, False otherwise.
        """
        pass

    def get(self, key: K) -> Optional[V]:
        """
        Retrieves the value associated with the specified key.

        :param key: The key whose associated value is to be retrieved.
        :return: The value associated with the key, or None if the key is not present.
        """
        pass

    def put(self, key: K, value: V) -> Optional[V]:
        """
        Associates the specified value with the specified key in the map.
        If the key is already present, it updates the value.

        :param key: The key with which the value is to be associated.
        :param value: The value to associate with the key.
        :return: The previous value associated with the key, or None if there was no previous value.
        """
        pass

    def putAll(self, jmap: 'SortedMap[K, V]') -> None:
        """
        Copies all key-value mappings from the specified map to this map.

        :param jmap: The map whose mappings are to be copied.
        """
        pass

    def remove(self, key: K) -> Optional[V]:
        """
        Removes the mapping for the specified key from the map, if present.

        :param key: The key whose mapping is to be removed.
        :return: The previous value associated with the key, or None if the key was not present.
        """
        pass

    def size(self) -> int:
        """
        Returns the number of key-value pairs in the map.

        :return: The number of entries in the map.
        """
        pass

    def isEmpty(self) -> bool:
        """
        Checks if the map is empty.

        :return: True if the map is empty, False otherwise.
        """
        pass
