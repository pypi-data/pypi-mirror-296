from collections.abc import Set

from jcollections.hashmap import HashMap
from jcollections.mapentry import MapEntry
from typing import Dict, List, Callable, Optional, TypeVar

K = TypeVar('K')  # Type variable for keys
V = TypeVar('V')  # Type variable for values

class LinkedHashMap(HashMap[K, V]):
    """
    A hash map implementation that maintains insertion order or access order of entries.

    Inherits from the `HashMap` class and adds functionality to maintain the order of keys based
    on either insertion or access order. This class provides methods to handle the order of key-value
    pairs and manage the map's entries efficiently.

    Attributes:
        _access_order (bool): If True, maintains access order of entries; otherwise, maintains insertion order.
        _insertion_order (List[K]): A list to keep track of the order of keys.
        _map (Dict[K, V]): Internal dictionary to store key-value pairs.
    """

    def __init__(self, initial_capacity=16, load_factor=0.75, access_order=False):
        """
        Constructs a new LinkedHashMap with the specified initial capacity, load factor, and order type.

        :param initial_capacity: Initial capacity of the hash map (default is 16).
        :param load_factor: Load factor for resizing the hash map (default is 0.75).
        :param access_order: If True, maintain access order; otherwise, maintain insertion order (default is False).
        """
        super().__init__(initial_capacity, load_factor)
        self._access_order = access_order
        self._insertion_order: List[K] = []
        self._map: Dict[K, V] = {}

    def put(self, key: K, value: V) -> Optional[V]:
        """
        Associates the specified value with the specified key in the map. If the key is new, it is added
        to the order list. If access order is enabled, the key is moved to the end of the list.

        :param key: The key with which the value is to be associated.
        :param value: The value to associate with the key.
        :return: The previous value associated with the key, or None if there was no previous value.
        """
        if key not in self._map:
            self._insertion_order.append(key)
        elif self._access_order:
            self._insertion_order.remove(key)
            self._insertion_order.append(key)
        self._map[key] = value
        return value

    def get(self, key: K) -> Optional[V]:
        """
        Retrieves the value associated with the specified key. If access order is enabled, the key is moved
        to the end of the order list.

        :param key: The key whose associated value is to be returned.
        :return: The value associated with the key, or None if the key is not present.
        """
        if key in self._map:
            if self._access_order:
                if key in self._insertion_order:
                    self._insertion_order.remove(key)
                self._insertion_order.append(key)
            return self._map[key]
        return None

    def remove(self, key: K) -> Optional[V]:
        """
        Removes the mapping for the specified key if it exists and updates the order list accordingly.

        :param key: The key whose mapping is to be removed.
        :return: The previous value associated with the key, or None if the key was not present.
        """
        if key in self._insertion_order:
            self._insertion_order.remove(key)
        return super().remove(key)

    def clear(self) -> None:
        """
        Removes all entries from the map and clears the order list.
        """
        super().clear()
        self._insertion_order.clear()

    def entrySet(self) -> List[MapEntry[K, V]]:
        """
        Returns a list of MapEntry objects representing all key-value pairs in the map, in the order of keys.

        :return: A list of MapEntry objects.
        """
        return [MapEntry(key, self._map[key]) for key in self._insertion_order]

    def keySet(self) -> Set[K]:
        """
        Returns a set of all keys in the map, maintaining the order of insertion or access.

        :return: A set of keys.
        """
        return set(self._insertion_order)

    def values(self) -> List[V]:
        """
        Returns a list of all values in the map, maintaining the order of keys.

        :return: A list of values.
        """
        return [self._map[key] for key in self._insertion_order]

    def forEach(self, action: Callable[[K, V], None]) -> None:
        """
        Applies the specified action to each entry in the map in the order of keys.

        :param action: A callable that accepts a key and a value.
        """
        for key in self._insertion_order:
            action(key, self._map[key])

    def getOrDefault(self, key: K, default_value: V) -> V:
        """
        Returns the value associated with the specified key, or a default value if the key is not present.

        :param key: The key whose associated value is to be returned.
        :param default_value: The default value to return if the key is not present.
        :return: The value associated with the key, or the default value.
        """
        return self._map.get(key, default_value)

    def replaceAll(self, function: Callable[[K, V], V]) -> None:
        """
        Replaces each value in the map with the result of applying the specified function to each key-value pair.

        :param function: A callable that accepts a key and a value and returns a new value.
        """
        for key in self._insertion_order:
            self._map[key] = function(key, self._map[key])

    def removeEldestEntry(self, eldest: MapEntry[K, V]) -> bool:
        """
        Override this method in subclasses to implement a policy for removing the eldest entry.

        :param eldest: The eldest entry in the map.
        :return: True if the eldest entry should be removed, False otherwise.
        """
        return False

    def __str__(self) -> str:
        """
        Returns a string representation of the LinkedHashMap.

        :return: A string representation of the map.
        """
        return f"LinkedHashMap({self._map})"
