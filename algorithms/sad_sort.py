from list.stack import Stack


def sad_sort(n: list, size: int = None):
    res = []
    if size is None:
        size = len(n)
    stack = Stack(size)
    for x in n:
        while stack.size != 0 and x > stack.peek():
            number = stack.pop()
            res.append(number)
        stack += x
    while stack:
        number = stack.pop()
        res.append(number)
    return res


if __name__ == '__main__':
    test_0 = [1, 2, 3, 4]
    for i in test_0:
        for j in filter(lambda n: n != i, test_0):
            for k in filter(lambda n: n != i and n != j, test_0):
                for l in filter(lambda n: n != i and n != j and n != k, test_0):
                    res = sad_sort([i, j, k, l], 4)
                    print(f"{[i, j, k, l]}->{res}: {res == [1, 2, 3, 4]}")
    print()
    print()

    test_1 = [1, 2, 3]
    for i in test_1:
        for j in filter(lambda n: n != i, test_1):
            for k in filter(lambda n: n != i and n != j, test_1):
                res = sad_sort([i, j, k], 3)
                print(f"{[i, j, k]}->{res}: {res == [1, 2, 3]}")
