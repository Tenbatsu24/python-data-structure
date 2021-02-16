from ds import DataStructure
from list.list import List


class Stack(List):

    # Initializing a stack.
    # Use a dummy node, which is
    # easier for handling edge cases.
    def __init__(self, n):
        super().__init__(n)

    def __eq__(self, other):
        return self.__eq__(other) and isinstance(other, Stack)

    def __reversed__(self):
        raise NotImplemented

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

    def push(self, value):
        self.__iadd__(value)

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

    @classmethod
    def to_array(cls, stack):
        array = [None for _ in range(stack.max_size)]
        curr_node = stack.head
        size = 0
        while size != stack.max_size:
            if array[size] is not None:
                array[size] = stack[curr_node]
                curr_node = List.next_index(stack, curr_node)
                size += 1
            else:
                break
        return array
