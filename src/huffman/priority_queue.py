class PriorityQueue:
    def __init__(self):
        self.queue: list = []

    def push(self, value):
        self.queue.append(value)
        self._put_to_real_position(len(self.queue) - 1)

    def _put_to_real_position(self, current: int):
        if current == 0:
            return
        parent = (current - 1) // 2
        if self.queue[current] < self.queue[parent]:
            self.queue[parent], self.queue[current] = self.queue[current], self.queue[parent]
            self._put_to_real_position(parent)

    def pop(self):
        if len(self.queue) == 1:
            return self.queue.pop()
        if len(self.queue) == 0:
            return None
        value = self.queue[0]
        self.queue[0] = self.queue.pop()
        self._heapify(0)
        return value

    def _heapify(self, current: int):
        smallest = current
        left = 2 * current + 1
        right = 2 * current + 2

        if left < len(self.queue) and self.queue[left] < self.queue[smallest]:
            smallest = left
        if right < len(self.queue) and self.queue[right] < self.queue[smallest]:
            smallest = right

        if smallest != current:
            self.queue[current], self.queue[smallest] = self.queue[smallest], self.queue[current]
            self._heapify(smallest)

    def __len__(self):
        return len(self.queue)

    def __str__(self):
        return f'[{", ".join(str(node) for node in self.queue)}]'

    def __repr__(self):
        return f'PriorityQueue({self.queue!r})'
