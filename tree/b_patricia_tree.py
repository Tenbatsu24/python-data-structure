ROGUE = -1
DEFAULT = 0

LENGTH = 5
PRUNE = 1 << LENGTH
MSB = (1 << (LENGTH - 1)) - 1


class BinaryNode:

    def __init__(self, sign, key=ROGUE, word_length=1):
        self.word = sign
        self.key = key
        self.word_length = word_length
        self.left = None
        self.right = None

    def set_left(self, node):
        if not self.left:
            self.left = node
        else:
            if node.key != ROGUE:
                self.left.key = node.key

    def set_right(self, node):
        if not self.right:
            self.right = node
        else:
            if node.key != ROGUE:
                self.right.key = node.key

    def __setitem__(self, key, value):
        if key:
            self.set_right(value)
        else:
            self.set_left(value)

    def __getitem__(self, item):
        if item:
            return self.right
        else:
            return self.left


def get_sign_bit(residue):
    return int((MSB - residue) < 0)


def shift_left(residue, by=1):
    left = residue
    for _ in range(by):
        left = ((left << 1) | PRUNE) ^ PRUNE
    return left


def match(word, target, target_length, match_offset):
    return word | (target << (LENGTH - match_offset - target_length)) == word


class BinaryPatriciaTree:
    def __init__(self, default=DEFAULT):
        self.root = BinaryNode(0, default, 0)

    def add_word(self, word, key, length):
        residue = word
        curr_node = self.root
        while length:
            sign = get_sign_bit(residue)
            curr_node[sign] = BinaryNode(sign)
            curr_node = curr_node[sign]
            residue = shift_left(residue)
            length -= 1
        curr_node.key = key

    def contract(self):
        self.__contract(self.root)

    def __contract(self, node):
        self.__contract_branch(node, node.left, node.right)
        self.__contract_branch(node, node.right, node.left)

    def __contract_branch(self, node, branch, other_branch):
        if branch is not None:
            self.__contract(branch)
            if not other_branch and node.key == ROGUE:
                node.word = (node.word << branch.word_length) + branch.word
                node.word_length += branch.word_length
                node.key = branch.key
                node.left, node.right = branch.left, branch.right

    def match(self, word):
        curr_node = self.root
        matched_to, match_offset = curr_node.key, 0
        sign = get_sign_bit(word)
        curr_node = curr_node[sign]
        residue = word

        while curr_node:
            if match(word, curr_node.word, curr_node.word_length, match_offset):
                matched_to = curr_node.key if curr_node.key != ROGUE else matched_to
                match_offset += curr_node.word_length

                residue = shift_left(residue, match_offset)
                sign = get_sign_bit(residue)
                curr_node = curr_node[sign]
            else:
                curr_node = None
        return matched_to


if __name__ == '__main__':
    pt = BinaryPatriciaTree()
    a = 0b11111
    b = 0b11110
    c = 0b01110
    d = 0b01111
    e = 0b10000

    pt.add_word(a, 1, 5)
    pt.add_word(b, 2, 5)
    pt.add_word(c, 3, 5)
    pt.add_word(d, 6, 5)
    pt.add_word(e, 7, 1)
    pt.contract()

    print(pt.match(e))
    print(pt.match(d))
    print(pt.match(b))
    print(pt.match(0b11011))
