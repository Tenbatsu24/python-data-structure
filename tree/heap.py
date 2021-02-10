from bt import *


class Heap(BinaryTree):

    def __init__(self, n: int):
        super().__init__(n)
        self.next_free = 0

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
        new_index = self.next_free
        if self.next_free is not None:
            self[new_index] = new_node
            self.next_free += 1
            if self.next_free >= self.max_size:
                self.next_free = None
        else:
            return self
        self.heapify(new_index)
        return self

    def __isub__(self, to_remove):
        super().__isub__(to_remove)
        for index in range(self.max_size):
            if self[index] is None:
                self.next_free = index
                break
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
        self -= to_return
        return to_return

    def handle_deletion(self, index):
        right_child_index = self.get_right_child_index(index)
        left_child_index = self.get_left_child_index(index)

        left_child = self[left_child_index]
        right_child = self[right_child_index]

        if left_child is not None or right_child is not None:

            if left_child is not None and right_child is None:
                swap_index = left_child_index
            elif left_child is None and right_child is not None:
                swap_index = right_child_index
            elif right_child < left_child:
                swap_index = right_child_index
            else:
                swap_index = left_child_index

            index = self.shift_up(index, swap_index)
            self.handle_deletion(index)

    def shift_up(self, index, swap_index):
        self[index] = self[swap_index]
        self[swap_index] = None
        return swap_index

    def heapify(self, index):
        parent_index = self.get_parent_index(index)
        while index != 0 and self[parent_index] > self[index]:
            self[index], self[parent_index] = self[parent_index], self[index]
            index = parent_index
            parent_index = self.get_parent_index(index)

    def valid_index(self, index):
        return 0 <= index < self.max_size


if __name__ == '__main__':
    heap = Heap(16)
    for i in range(8, 2, -1):
        heap += i
    print(heap)
    print(heap.pop())
    print(heap)
    print(heap.pop())
    print(heap.pop())
    print(heap.pop())
    heap -= 5
    heap += 3
    print(heap)
    print(len(heap))
