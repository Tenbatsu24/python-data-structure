class DisjointSet:

    def __init__(self, n, use_pc=True):
        self.parent = [-1 for _ in range(n)]
        self.size = [1 for _ in range(n)]
        if use_pc:
            self.__find = self.__find_pc
        else:
            self.__find = self.__find_wo_pc

    def find(self, k):
        return self.__find(k)  # if self.pc else self.__find_wo_pc(k)

    def __find_wo_pc(self, k):
        return (k if self.parent[k] == k else self.find(self.parent[k])) if self.parent[k] >= 0 else k

    def __find_pc(self, k):
        if self.parent[k] < 0:
            return k
        else:
            self.parent[k] = self.__find_pc(self.parent[k])
            return self.parent[k]

    def union(self, a, b):
        root1 = self.find(a)
        root2 = self.find(b)

        if root1 != root2:
            self.__link_by_size(root1, root2)

    def __link_by_size(self, root1, root2):
        if self.size[root1] >= self.size[root2]:
            self.__link_to(root1, root2)
        else:
            self.__link_to(root2, root1)

    def __link_to(self, bigger, smaller):
        self.parent[smaller] = bigger
        self.size[bigger] += self.size[smaller]
        self.parent[bigger] = -self.size[bigger]


if __name__ == '__main__':
    my_set = DisjointSet(10, False)
    my_set.union(1, 7)
    my_set.union(3, 4)
    my_set.union(2, 5)
    my_set.union(7, 3)
    my_set.union(9, 5)
    my_set.union(8, 9)
    my_set.union(6, 4)
    print(my_set.parent)
