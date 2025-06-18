from huffman.priority_queue import PriorityQueue


class Node:
    def __init__(self, weight, char=None, left=None, right=None, code=None):
        self.weight: int = weight
        self.char: str | None = char
        self.left: Node | None = left
        self.right: Node | None = right
        self.code: str | None = code

    def has_left_child(self):
        return self.left

    def has_right_child(self):
        return self.right

    def is_leaf(self):
        return not (self.has_left_child() or self.has_right_child())

    def __lt__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.weight < other.weight

    def __str__(self):
        output = [
            f'Char: {repr(self.char)}' if self.char else 'Char: None',
            f'Weight: {self.weight}' if self.weight else 'Char: None',
        ]
        return ' : '.join(output)

    def __repr__(self):
        return (f'Node(char={repr(self.char)}, weight={self.weight}, '
                f'left={repr(self.left.char) if self.left else None}, '
                f'right={repr(self.right.char) if self.right else None}')


class HuffmanTree:
    def __init__(self):
        self._root: Node | None = None
        self._encoding: dict[str, str] = {}

    def get_encoding(self, frequency: dict[str, int]):
        self._build_tree(frequency=frequency)
        self._encode(node=self._root, code='')
        return self._encoding

    def _build_tree(self, frequency: dict[str, int]):
        tree = PriorityQueue()
        for char, weight in frequency.items():
            tree.push(Node(char=char, weight=weight))
        while len(tree) > 1:
            left = tree.pop()
            right = tree.pop()
            tree.push(
                Node(
                    weight=left.weight + right.weight,
                    left=left,
                    right=right
                )
            )
        self._root = tree.pop()

    def _encode(self, node: Node, code: str):
        if node.is_leaf():
            self._encoding[node.char] = node.code
            return
        if node.has_left_child():
            node.left.code = code + '0'
            self._encode(node=node.left, code=code + '0')
        if node.has_right_child():
            node.right.code = code + '1'
            self._encode(node=node.right, code=code + '1')
