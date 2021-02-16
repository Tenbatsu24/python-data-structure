from abc import abstractmethod


class DataStructure(object):

    def __init__(self, n: int):
        self.nodes = [None for _ in range(n)]
        self.size = 0
        self.next_free = 0
        self.max_size = n
        self.key_map = {}

    def __int__(self):
        return self.size

    def __abs__(self):
        return self.size

    def __len__(self):
        return self.size

    def __bool__(self):
        return self.size != 0

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

    @abstractmethod
    def __reversed__(self):
        pass

    def __contains__(self, item):
        return self.key_map.get(item) is not None

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    @abstractmethod
    def __iadd__(self, other):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass
