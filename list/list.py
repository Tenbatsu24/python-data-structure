from ds import DataStructure


class List(DataStructure):

    def __init__(self, n):
        super(List, self).__init__(n)
        self.head = 0

    def __iter__(self):
        self.__iter = filter(lambda node: node is not None, self.nodes)
        return self

    def __next__(self):
        return self.__iter.__next__()

    def next_index(self, index):
        return (index + 1) % self.max_size
