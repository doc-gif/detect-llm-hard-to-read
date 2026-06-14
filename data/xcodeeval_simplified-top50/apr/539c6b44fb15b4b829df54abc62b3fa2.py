class MinHeap:
    def __init__(self, initial=None):
        self.a = [] if initial is None else initial[:]
        self.n = len(self.a)
        if self.n > 0:
            for i in range((self.n - 2) // 2, -1, -1):
                self._heapify_down(i)

    def _heapify_up(self, idx):
        if idx > 0:
            parent = (idx - 1) // 2
            if self.a[parent] > self.a[idx]:
                self.a[parent], self.a[idx] = self.a[idx], self.a[parent]
                self._heapify_up(parent)

    def _heapify_down(self, idx):
        left = idx * 2 + 1
        right = idx * 2 + 2
        smallest = idx
        if left < self.n and self.a[smallest] > self.a[left]:
            smallest = left
        if right < self.n and self.a[smallest] > self.a[right]:
            smallest = right
        if smallest != idx:
            self.a[idx], self.a[smallest] = self.a[smallest], self.a[idx]
            self._heapify_down(smallest)

    def push(self, val):
        if self.n == len(self.a):
            self.a.append(val)
        else:
            self.a[self.n] = val
        self._heapify_up(self.n)
        self.n += 1

    def pop(self):
        if self.n == 0:
            raise Exception("empty heap")
        res = self.a[0]
        self.n -= 1
        if self.n > 0:
            self.a[0] = self.a[self.n]
            self.a[self.n] = 0
            self._heapify_down(0)
        return res


n, x, y = map(int, input().split())
heap = MinHeap()
visited = {}
heap.push((0, n))
result = -1
while result == -1:
    cost, current = heap.pop()
    if current not in visited:
        visited[current] = cost
        if current == 1:
            result = cost + x
        else:
            if current - 1 not in visited:
                heap.push((cost + x, current - 1))
            if (
                current % 2 == 0
                and current // 2 not in visited
                and y < (current // 2) * x
            ):
                heap.push((cost + y, current // 2))
            if current + 1 not in visited:
                heap.push((cost + x, current + 1))
print(result)
