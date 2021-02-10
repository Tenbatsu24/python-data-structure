from typing import Generic, TypeVar

from ds import DataStructure

T = TypeVar('T')


class Node:
    def __init__(self, data):
        self.item = data
        self.n = None
        self.p = None
        self.tail = None


class DoublyLinkedList(DataStructure, Generic[T]):

    def __init__(self, circular: bool = False):
        super().__init__()
        self.circular = circular

    def __eq__(self, other):
        super().__eq__(other)

    def __reversed__(self):
        super().__reversed__()

    def __contains__(self, item):
        super().__contains__(item)

    def __add__(self, other):
        super().__add__(other)
        if type(other) is DoublyLinkedList:
            for node in other:
                self.insert(node)
        elif type(other) is T:
            self.insert(Node(other))

    def __sub__(self, other):
        super().__sub__(other)

    def __iadd__(self, other):
        super().__iadd__(other)

    def __isub__(self, other):
        super().__isub__(other)

    def __iter__(self):
        super().__iter__()
        self.__i_next = self.head

    def __next__(self):
        super().__next__()
        if self.__i_next.n is not None:
            self.__i_next = self.__i_next.n
            return self.__i_next
        else:
            raise StopIteration

    def insert(self, node: Node):
        if self.head is None:
            self.head = node
        else:
            pass
