import collections


class Node:
    def __init__(self, data, parent):
        self.parent = parent
        self.data = data
        self.children = {}

    def __contains__(self, item):
        return item in self.children

    def __getitem__(self, item):
        return self.children[item]

    def __setitem__(self, key, value):
        self.children[key] = Node(value, self)

    def __hash__(self):
        if isinstance(self.data, collections.Hashable):
            return hash(self.data)
        else:
            raise TypeError("The value of this node is not Hashable")

    def __eq__(self, other):
        try:
            return hash(self) == hash(other)
        except TypeError:
            return self.data == other.data


class HierarchyTree:
    def __init__(self, root_data):
        self.root = Node(root_data, None)

    def __getitem__(self, path):
        current = self.root
        reached_end = True
        index_reached = 0

        for i, identifier in enumerate(path):
            if identifier in current:
                current = current[identifier]
                index_reached = i
            else:
                reached_end = False
                break
        return current, reached_end, index_reached
