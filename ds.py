from abc import abstractmethod


class DataStructure(object):

    def __init__(self, n: int):
        self.nodes = [None for _ in range(n)]
        self.count = 0
        self.next_free = 0
        self.max_size = n

    def __int__(self):
        return self.count

    def __abs__(self):
        return self.count

    def __len__(self):
        return len(list(filter(lambda n: n is not None, self.nodes)))

    def __bool__(self):
        return self.count != 0

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __reversed__(self):
        pass

    @abstractmethod
    def __contains__(self, item):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __iadd__(self, other):
        pass

    def __isub__(self, other):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass
