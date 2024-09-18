from abc import abstractmethod

from jcollections.collection import Collection


class AbstractQueue(Collection):
    @abstractmethod
    def add(self, e):
        """
        Inserts the specified element into this queue if possible without violating capacity restrictions.
        Returns True on success or raises an exception if the queue is full.
        """
        pass

    @abstractmethod
    def element(self):
        """
        Retrieves, but does not remove, the head of this queue.
        Raises an exception if the queue is empty.
        """
        pass

    @abstractmethod
    def offer(self, e):
        """
        Inserts the specified element into this queue if possible without violating capacity restrictions.
        Returns True on success or False if the queue is full.
        """
        pass

    @abstractmethod
    def peek(self):
        """
        Retrieves, but does not remove, the head of this queue, or returns None if the queue is empty.
        """
        pass

    @abstractmethod
    def poll(self):
        """
        Retrieves and removes the head of this queue, or returns None if the queue is empty.
        """
        pass

    @abstractmethod
    def remove(self, o):
        """
        Retrieves and removes the head of this queue.
        Raises an exception if the queue is empty.
        """
        pass
