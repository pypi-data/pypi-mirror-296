from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Optional, Set, Collection, Any

K = TypeVar('K')  # Type variable for keys
V = TypeVar('V')  # Type variable for values


class Map(ABC, Generic[K, V]):
    """
    An abstract base class defining a map (dictionary) data structure.

    This class outlines the fundamental operations that any concrete map implementation must support.

    Type Parameters:
        K: Type of the keys in the map.
        V: Type of the values in the map.
    """

    @abstractmethod
    def clear(self) -> None:
        """
        Removes all entries from the map.
        """
        pass

    @abstractmethod
    def containsKey(self, key: K) -> bool:
        """
        Checks if the map contains the specified key.

        :param key: The key to check for.
        :return: True if the key is present, False otherwise.
        """
        pass

    @abstractmethod
    def containsValue(self, value: V) -> bool:
        """
        Checks if the map contains the specified value.

        :param value: The value to check for.
        :return: True if the value is present, False otherwise.
        """
        pass

    @abstractmethod
    def entrySet(self) -> Set[Any]:
        """
        Returns a set of all key-value pairs in the map.

        :return: A set of key-value pairs.
        """
        pass

    @abstractmethod
    def get(self, key: K) -> Optional[V]:
        """
        Retrieves the value associated with the specified key.

        :param key: The key to retrieve the value for.
        :return: The value associated with the key, or None if the key is not present.
        """
        pass

    @abstractmethod
    def isEmpty(self) -> bool:
        """
        Checks if the map is empty.

        :return: True if the map contains no entries, False otherwise.
        """
        pass

    @abstractmethod
    def keySet(self) -> Set[K]:
        """
        Returns a set of all keys in the map.

        :return: A set of keys.
        """
        pass

    @abstractmethod
    def put(self, key: K, value: V) -> Optional[V]:
        """
        Associates the specified value with the specified key in the map.

        :param key: The key with which the value is to be associated.
        :param value: The value to associate with the key.
        :return: The previous value associated with the key, or None if there was no previous value.
        """
        pass

    @abstractmethod
    def putAll(self, jmap: 'Map[K, V]') -> None:
        """
        Copies all mappings from the specified map to this map.

        :param jmap: The map whose mappings are to be copied.
        """
        pass

    @abstractmethod
    def remove(self, key: K) -> Optional[V]:
        """
        Removes the mapping for the specified key if it exists.

        :param key: The key whose mapping is to be removed.
        :return: The previous value associated with the key, or None if there was no mapping.
        """
        pass

    @abstractmethod
    def size(self) -> int:
        """
        Returns the number of key-value pairs in the map.

        :return: The number of entries in the map.
        """
        pass

    @abstractmethod
    def values(self) -> Collection[V]:
        """
        Returns a collection of all values in the map.

        :return: A collection of values.
        """
        pass

    # Default methods

    def compute(self, key: K, remappingFunction: Callable[[K, Optional[V]], Optional[V]]) -> Optional[V]:
        """
        Computes a new value for the specified key using the given remapping function.

        If the key is present, the existing value is passed to the function; otherwise, the function is
        called with None.

        :param key: The key to compute a new value for.
        :param remappingFunction: Function to compute the new value.
        :return: The new value associated with the key, or None if the key was removed.
        """
        current_value = self.get(key)
        new_value = remappingFunction(key, current_value)
        if new_value is None:
            if current_value is not None:
                self.remove(key)
        else:
            self.put(key, new_value)
        return new_value

    def computeIfAbsent(self, key: K, mappingFunction: Callable[[K], V]) -> V:
        """
        Computes a value for the specified key if the key is not already associated with a value.

        :param key: The key for which to compute a value.
        :param mappingFunction: Function to compute the value.
        :return: The computed value if the key was absent, or the existing value if the key was present.
        """
        value = self.get(key)
        if value is None:
            value = mappingFunction(key)
            self.put(key, value)
        return value

    def computeIfPresent(self, key: K, remappingFunction: Callable[[K, V], V]) -> Optional[V]:
        """
        Computes a new value for the specified key if the key is already associated with a value.

        :param key: The key for which to compute a new value.
        :param remappingFunction: Function to compute the new value.
        :return: The new value if the key was present, or None if the key was absent.
        """
        value = self.get(key)
        if value is not None:
            new_value = remappingFunction(key, value)
            self.put(key, new_value)
            return new_value
        return None

    def getOrDefault(self, key: K, defaultValue: V) -> V:
        """
        Retrieves the value associated with the specified key, or returns a default value if the key is not present.

        :param key: The key to retrieve the value for.
        :param defaultValue: The value to return if the key is not present.
        :return: The value associated with the key, or the default value if the key is absent.
        """
        value = self.get(key)
        return value if value is not None else defaultValue

    def merge(self, key: K, value: V, remappingFunction: Callable[[V, V], V]) -> V:
        """
        Merges the specified value with the existing value associated with the key using the given remapping function.

        If the key is not present, the value is simply added. If the key is present, the existing value is
        merged with the specified value.

        :param key: The key to merge the value with.
        :param value: The value to merge.
        :param remappingFunction: Function to merge the existing and new values.
        :return: The new value associated with the key.
        """
        old_value = self.get(key)
        if old_value is None:
            self.put(key, value)
            return value
        else:
            new_value = remappingFunction(old_value, value)
            self.put(key, new_value)
            return new_value

    def putIfAbsent(self, key: K, value: V) -> Optional[V]:
        """
        Adds the specified key-value pair to the map if the key is not already associated with a value.

        :param key: The key to add.
        :param value: The value to associate with the key.
        :return: The current value associated with the key, or None if the key was not present.
        """
        current_value = self.get(key)
        if current_value is None:
            self.put(key, value)
        return current_value

    def removeIf(self, key: K, value: V) -> bool:
        """
        Removes the specified key-value pair from the map if it is currently associated with the specified value.

        :param key: The key to remove.
        :param value: The value to match.
        :return: True if the key-value pair was removed, False otherwise.
        """
        current_value = self.get(key)
        if current_value == value:
            self.remove(key)
            return True
        return False

    def replace(self, key: K, value: V) -> Optional[V]:
        """
        Replaces the value associated with the specified key if the key is currently present.

        :param key: The key whose value is to be replaced.
        :param value: The new value to associate with the key.
        :return: The previous value associated with the key, or None if the key was not present.
        """
        if self.containsKey(key):
            return self.put(key, value)
        return None

    def replaceAll(self, function: Callable[[K, V], V]) -> None:
        """
        Replaces all values in the map with values computed by applying the given function to each key-value pair.

        :param function: Function to compute new values based on the current key-value pairs.
        """
        for key in self.keySet():
            self.put(key, function(key, self.get(key)))
