from list.list import List


class DoublyLinkedList(List):

    def __reversed__(self):
        pass

    def __init__(self, n: int):
        super().__init__(n)

    def __iadd__(self, other):
        if self.next_free is not None:
            self[self.next_free] = other
            self.next_free = self.next_index(self.next_free)
            self.size += 1
            if self.size > self.max_size:
                self.next_free = None
        return self

    def insert(self, node, index: int = None):
        if self.next_free is not None:
            if index is None:
                self.__iadd__(node)
            else:
                pass

