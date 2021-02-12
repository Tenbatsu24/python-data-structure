from ds import *


class Heap(DataStructure):

    def __init__(self, n: int):
        super().__init__(n)
        self.next_free = n - 1

    def __has_next_left(self, parent):
        return self.get_left_child_index(parent) < self.max_size

    def __has_next_right(self, parent):
        return self.get_right_child_index(parent) < self.max_size

    @staticmethod
    def get_parent_index(child_index: int):
        return int((child_index - 1) // 2)

    @staticmethod
    def get_left_child_index(parent_index: int):
        return parent_index * 2 + 1

    @staticmethod
    def get_right_child_index(parent_index: int):
        return (parent_index + 1) * 2

    def __reversed__(self):
        raise NotImplemented

    def __eq__(self, other):
        return super().__eq__(other) and isinstance(other, Heap)

    def __add__(self, new_node):
        new_heap = Heap(self.max_size)
        for node in self:
            new_heap += node
        new_heap += new_node
        return new_heap

    def __sub__(self, to_remove):
        new_heap = Heap(self.max_size)
        for node in filter(lambda n: n != to_remove, self.nodes):
            new_heap += node
        return new_heap

    def __iadd__(self, new_node):
        if self.next_free != -1:
            new_index = self.next_free
            if self[new_index] is None:
                self.size += 1
                self[new_index] = new_node
                self.key_map[new_node] = new_index
                # print(self.key_map)
                self.next_free = self.max_size - 1
            else:
                self.next_free -= 1
                self.__iadd__(new_node)
        else:
            return self

        self.heapify(new_index)
        return self

    def __isub__(self, to_remove):
        index = self.key_map.get(to_remove)
        # print(f"{to_remove} at {index}")
        if index is not None:
            self.key_map.pop(to_remove)
            self.size -= 1
            self.handle_deletion(index)
        return self

    def __iter__(self):
        self.__iter = filter(lambda node: node is not None, self.nodes)
        return self

    def __next__(self):
        return self.__iter.__next__()

    def __str__(self):
        return list(filter(lambda n: n is not None, self.nodes)).__str__()

    def pop(self):
        to_return = self[0]
        # print(f"to return = {to_return}")
        self.__isub__(to_return)
        return to_return

    def handle_deletion(self, index):

        right_child_index = self.get_right_child_index(index)
        left_child_index = self.get_left_child_index(index)

        left_child = self[left_child_index]
        right_child = self[right_child_index]

        if left_child is not None or right_child is not None:

            if left_child is not None and right_child is None:
                child_index = left_child_index
            elif left_child is None and right_child is not None:
                child_index = right_child_index
            elif right_child < left_child:
                child_index = right_child_index
            else:
                child_index = left_child_index

            index = self.swap(index, child_index)
            self.handle_deletion(index)
        else:
            self[index] = None

    def swap(self, index, swap_index):
        self[index], self[swap_index] = self[swap_index], self[index]

        if self[index] is not None:
            self.key_map[self[index]] = index

        if self[swap_index] is not None:
            self.key_map[self[swap_index]] = swap_index

        return swap_index

    def heapify(self, index):
        # print(f"I heapify on index: {index}")
        parent_index = self.get_parent_index(index)
        # print(f"My parent is: {parent_index}")
        while index != 0 and (self[index] is not None) and ((self[parent_index] is None) or (self[parent_index] > self[index])):
            index = self.swap(index, parent_index)
            parent_index = self.get_parent_index(index)

    def decr_key(self, node):
        # print(node.__repr__(), node.dist)
        # print(self.key_map)
        index = self.key_map.get(node)
        if index is not None:
            self.heapify(index)
        # print(self)


if __name__ == '__main__':
    heap = Heap(16)
    for i in range(8, 2, -1):
        heap += i
    print(heap, heap.size)
    while heap:
        print(heap.pop())
        print(heap.nodes, heap.size)
