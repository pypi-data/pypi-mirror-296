from typing import Callable, Optional, Dict, TypeVar, Set, Collection
from jcollections.mapentry import MapEntry
from jcollections.sortedmap import SortedMap

# Define type variables for keys and values
K = TypeVar('K')  # Key type variable
V = TypeVar('V')  # Value type variable


class TreeMap(SortedMap[K, V]):
    """
    A TreeMap implementation of the SortedMap interface that maintains its keys in a sorted order.

    This class provides a way to map keys to values while keeping the keys sorted based on a comparator or natural ordering.

    Attributes:
        _map: Internal storage for key-value pairs as a dictionary.
        _comparator: Optional comparator function used to order the keys.

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
        ceilingEntry: Retrieves the least key greater than or equal to the specified key.
        descendingMap: Returns a TreeMap with entries in descending order.
        clone: Creates a shallow copy of the map.
        replace: Replaces the value for a specified key if it exists.
        pollFirstEntry: Removes and returns the first (smallest) entry.
        pollLastEntry: Removes and returns the last (largest) entry.
        forEach: Applies a function to each key-value pair in the map.
    """

    def __init__(self, comparator: Optional[Callable[[K, K], int]] = None, jmap: Optional[Dict[K, V]] = None):
        """
        Initializes a TreeMap with optional comparator and initial data.

        :param comparator: Optional comparator to order the keys.
        :param jmap: Optional initial data to populate the map.
        """
        self._map: Dict[K, V] = jmap if jmap is not None else {}  # Internal storage of keys and values
        self._comparator = comparator

    def comparator(self) -> Optional[Callable[[K, K], int]]:
        """
        Returns the comparator used to order the keys, or None if natural ordering is used.

        :return: A callable that compares two keys, or None.
        """
        return self._comparator

    def firstKey(self) -> K:
        """
        Returns the first (smallest) key in the map.

        :return: The smallest key in the map.
        :raises KeyError: If the map is empty.
        """
        if not self._map:
            raise KeyError("TreeMap is empty")
        return min(self._map.keys())

    def lastKey(self) -> K:
        """
        Returns the last (largest) key in the map.

        :return: The largest key in the map.
        :raises KeyError: If the map is empty.
        """
        if not self._map:
            raise KeyError("TreeMap is empty")
        return max(self._map.keys())

    def headMap(self, toKey: K) -> 'TreeMap[K, V]':
        """
        Returns a view of the map with keys less than the specified `toKey`.

        :param toKey: The key up to which the view is to be created.
        :return: A TreeMap with keys less than `toKey`.
        """
        return TreeMap(self._comparator, {k: v for k, v in self._map.items() if k < toKey})

    def subMap(self, fromKey: K, toKey: K) -> 'TreeMap[K, V]':
        """
        Returns a view of the map with keys between `fromKey` (inclusive) and `toKey` (exclusive).

        :param fromKey: The starting key of the view (inclusive).
        :param toKey: The ending key of the view (exclusive).
        :return: A TreeMap with keys between `fromKey` and `toKey`.
        """
        return TreeMap(self._comparator, {k: v for k, v in self._map.items() if fromKey <= k < toKey})

    def tailMap(self, fromKey: K) -> 'TreeMap[K, V]':
        """
        Returns a view of the map with keys greater than or equal to the specified `fromKey`.

        :param fromKey: The key from which the view starts.
        :return: A TreeMap with keys greater than or equal to `fromKey`.
        """
        return TreeMap(self._comparator, {k: v for k, v in self._map.items() if k >= fromKey})

    def entrySet(self) -> Set[MapEntry[K, V]]:
        """
        Returns a set of MapEntry objects representing all key-value pairs in the map.

        :return: A set of MapEntry objects.
        """
        return {MapEntry(k, v) for k, v in self._map.items()}

    def keySet(self) -> Set[K]:
        """
        Returns a set of all keys in the map.

        :return: A set of keys.
        """
        return set(self._map.keys())

    def values(self) -> Collection[V]:
        """
        Returns a collection of all values in the map.

        :return: A collection of values.
        """
        return set(self._map.values())

    def clear(self) -> None:
        """
        Removes all entries from the map.
        """
        self._map.clear()

    def containsKey(self, key: K) -> bool:
        """
        Checks if the map contains a mapping for the specified key.

        :param key: The key to check for presence in the map.
        :return: True if the map contains the key, False otherwise.
        """
        return key in self._map

    def containsValue(self, value: V) -> bool:
        """
        Checks if the map contains a mapping for the specified value.

        :param value: The value to check for presence in the map.
        :return: True if the map contains the value, False otherwise.
        """
        return value in self._map.values()

    def get(self, key: K) -> Optional[V]:
        """
        Retrieves the value associated with the specified key.

        :param key: The key whose associated value is to be retrieved.
        :return: The value associated with the key, or None if the key is not present.
        """
        return self._map.get(key)

    def put(self, key: K, value: V) -> Optional[V]:
        """
        Associates the specified value with the specified key in the map.
        If the key is already present, it updates the value.

        :param key: The key with which the value is to be associated.
        :param value: The value to associate with the key.
        :return: The previous value associated with the key, or None if there was no previous value.
        """
        return self._map.setdefault(key, value)

    def putAll(self, jmap: 'SortedMap[K, V]') -> None:
        """
        Copies all key-value mappings from the specified map to this map.

        :param jmap: The map whose mappings are to be copied.
        """
        for entry in jmap.entrySet():
            self.put(entry.getKey(), entry.getValue())

    def remove(self, key: K) -> Optional[V]:
        """
        Removes the mapping for the specified key from the map, if present.

        :param key: The key whose mapping is to be removed.
        :return: The previous value associated with the key, or None if the key was not present.
        """
        return self._map.pop(key, None)

    def size(self) -> int:
        """
        Returns the number of key-value pairs in the map.

        :return: The number of entries in the map.
        """
        return len(self._map)

    def isEmpty(self) -> bool:
        """
        Checks if the map is empty.

        :return: True if the map is empty, False otherwise.
        """
        return len(self._map) == 0

    def ceilingEntry(self, key: K) -> Optional[MapEntry[K, V]]:
        """
        Retrieves the least key greater than or equal to the specified key.

        :param key: The key for which the ceiling entry is to be retrieved.
        :return: A MapEntry with the ceiling key and its associated value, or None if no such key exists.
        """
        if self._comparator:
            sorted_keys = sorted(self._map.keys(), key=lambda k1: self._comparator(k1, key))
            for k in sorted_keys:
                if self._comparator(k, key) >= 0:
                    return MapEntry(k, self._map[k])
        else:
            sorted_keys = sorted(self._map.keys())
            for k in sorted_keys:
                if k >= key:
                    return MapEntry(k, self._map[k])
        return None

    def descendingMap(self) -> 'TreeMap[K, V]':
        """
        Returns a TreeMap with entries in descending order.

        :return: A TreeMap with entries in reverse order.
        """
        return TreeMap(self._comparator, dict(sorted(self._map.items(), reverse=True)))

    def clone(self) -> 'TreeMap[K, V]':
        """
        Creates a shallow copy of the map.

        :return: A new TreeMap instance with the same key-value pairs.
        """
        new_map = TreeMap(self._comparator)
        new_map._map = self._map.copy()
        return new_map

    def replace(self, key: K, value: V) -> Optional[V]:
        """
        Replaces the value for a specified key if it exists.

        :param key: The key whose value is to be replaced.
        :param value: The new value to associate with the key.
        :return: The old value associated with the key, or None if the key was not present.
        """
        if key in self._map:
            old_value = self._map[key]
            self._map[key] = value
            return old_value
        return None

    def pollFirstEntry(self) -> Optional[MapEntry[K, V]]:
        """
        Removes and returns the first (smallest) entry.

        :return: A MapEntry with the smallest key and its associated value, or None if the map is empty.
        """
        if self._map:
            first_key = min(self._map.keys())
            return MapEntry(first_key, self._map.pop(first_key))
        return None

    def pollLastEntry(self) -> Optional[MapEntry[K, V]]:
        """
        Removes and returns the last (largest) entry.

        :return: A MapEntry with the largest key and its associated value, or None if the map is empty.
        """
        if self._map:
            last_key = max(self._map.keys())
            return MapEntry(last_key, self._map.pop(last_key))
        return None

    def forEach(self, action: Callable[[K, V], None]) -> None:
        """
        Applies a function to each key-value pair in the map.

        :param action: A function that takes a key and a value, and returns nothing.
        """
        for k, v in self._map.items():
            action(k, v)

    def __repr__(self):
        """
        Returns a string representation of the TreeMap.

        :return: A string representation of the map.
        """
        return str(self._map)
