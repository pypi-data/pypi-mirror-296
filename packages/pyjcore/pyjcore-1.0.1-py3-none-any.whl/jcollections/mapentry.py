from typing import TypeVar, Generic

# Define type variables K and V
K = TypeVar('K')
V = TypeVar('V')

class MapEntry(Generic[K, V]):
    def __init__(self, key: K, value: V):
        self._key = key
        self._value = value

    def getKey(self) -> K:
        return self._key

    def getValue(self) -> V:
        return self._value

    def setValue(self, value: V) -> V:
        old_value = self._value
        self._value = value
        return old_value

    def equals(self, o) -> bool:
        if isinstance(o, MapEntry):
            return self._key == o.getKey() and self._value == o.getValue()
        return False

    def hashCode(self) -> int:
        return hash((self._key, self._value))

    def __repr__(self):
        return f"({self._key}, {self._value})"
