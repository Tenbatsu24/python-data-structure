from ds import *


class BinaryTree(DataStructure):

    def __init__(self, n: int):
        super().__init__(n)

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

    def __eq__(self, other):
        if other is self:
            return True
        elif type(other) == type(self):
            for (i, node) in enumerate(self.nodes):
                if not node == other[i]:
                    return False
        return True

    def __getitem__(self, item):
        return self.nodes[item] if item < self.max_size else None

    def __setitem__(self, key, value):
        self.nodes[key] = value

    def __reversed__(self):
        raise NotImplemented

    def __contains__(self, node):
        return len(list(filter(lambda n: n == node, self.nodes))) != 0

    def __add__(self, new_node):
        new_tree = BinaryTree(self.max_size)
        for node in self:
            new_tree += node
        new_tree += new_node
        return new_tree

    def __sub__(self, to_remove):
        new_tree = BinaryTree(self.max_size)
        for node in filter(lambda n: n != to_remove, self.nodes):
            new_tree += node
        return new_tree

    def __iadd__(self, new_node):
        super().__iadd__(new_node)
        if self[0] is None:
            self[0] = new_node
        else:
            # print(f"adding: {new_node}")
            parent_index = 0
            while parent_index < self.max_size:
                if new_node <= self[parent_index]:
                    left_child_index = self.get_left_child_index(parent_index)
                    if self[left_child_index] is None:
                        # print(f"adding to left of {parent_index}:{left_child_index}")
                        self[left_child_index] = new_node
                        break
                    else:
                        parent_index = left_child_index
                else:
                    right_child_index = self.get_right_child_index(parent_index)
                    if self[right_child_index] is None:
                        # print(f"adding to right of {parent_index}:{right_child_index}")
                        self[right_child_index] = new_node
                        break
                    else:
                        parent_index = right_child_index
        return self

    def __isub__(self, to_remove):
        super().__isub__(to_remove)
        index = None
        for (i, node) in enumerate(self.nodes):
            if node == to_remove:
                index = i
                break
        if index is not None:
            self.count -= 1
            self.handle_deletion(index)
        return self

    def __iter__(self):
        self.__iter = iter(self.inorder_traversal(0))
        return self

    def __next__(self):
        return self.__iter.__next__()

    def __str__(self):
        return f"{self.inorder_traversal(0)}"

    def pop(self):
        to_return = self[0]
        self -= to_return
        return to_return

    def handle_deletion(self, index):
        if self[self.get_left_child_index(index)] is not None or self[self.get_right_child_index(index)] is not None:
            swapped_parent = self.get_right_child_index(index)
            while self.nodes[swapped_parent] is not None:
                index, swapped_parent = self.shift_up(index, swapped_parent)
            index, _ = self.shift_up(index, self.get_left_child_index(index))
            self.handle_deletion(index)

    def shift_up(self, index, swapped_parent):
        self[index], self[swapped_parent] = self[swapped_parent], None
        return swapped_parent, self.get_right_child_index(swapped_parent)

    def inorder_traversal(self, root):
        res = []
        if self[root] is not None:
            res = self.inorder_traversal(self.get_left_child_index(root))
            res.append(self[root])
            res += self.inorder_traversal(self.get_right_child_index(root))
        return res


if __name__ == '__main__':
    tree = BinaryTree(20)
    for j in [1, 0, 2, 3]:
        tree += j

    tree2 = BinaryTree(2)
    tree2 += 3
    tree2 += 0

    print(tree.nodes)

    tree -= 1
    print(tree.nodes)

    print(tree.pop())
    print(tree.nodes)
    print(tree == tree2)
    tree2 += 5
