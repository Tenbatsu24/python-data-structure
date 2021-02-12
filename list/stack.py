from ds import DataStructure


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Stack(DataStructure):

    # Initializing a stack.
    # Use a dummy node, which is
    # easier for handling edge cases.
    def __init__(self, n):
        super().__init__(n)
        self.head = 0

    def __eq__(self, other):
        return self.__eq__(other) and isinstance(other, Stack)

    def __reversed__(self):
        raise NotImplemented

    def __iter__(self):
        self.__iter = filter(lambda node: node is not None, self.nodes)
        return self

    def __next__(self):
        return self.__iter.__next__()

    # String representation of the stack
    def __str__(self):
        curr_index = self.head
        curr = self[curr_index]

        string = f"start -> {curr}"
        curr_index = self.next_index(curr_index)
        curr = self[curr_index]
        while curr is not None and curr_index != self.head:
            string += f" -> {curr}"
            curr_index = self.next_index(curr_index)
            curr = self[curr_index]
        return string

    def next_index(self, index):
        return (index + 1) % self.max_size

    # Get the top item of the stack
    def peek(self):
        # print(f"head->{self[self.head]}, len-> {len(self)}")
        if len(self) == 0:
            raise Exception("Peeking from an empty stack")
        return self[self.head]

    # Push a value into the stack.
    def __iadd__(self, value):
        if self.next_free is not None:
            self[self.next_free] = value
            self.head = self.next_free
            self.next_free = self.next_index(self.next_free)
            self.size += 1
            if self.size > self.max_size:
                self.next_free = None
        return self

    # Remove a value from the stack and return.
    def pop(self):
        if not self:
            raise Exception("Popping from an empty stack")
        removed = self[self.head]
        self[self.head] = None
        self.size -= 1
        self.next_free = self.head
        self.head = self.next_index(self.head - 2)
        return removed
