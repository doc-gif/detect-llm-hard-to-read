from queue import Queue
n, x = map(int, input().split())
queue = Queue()
queue.put((x, 0))
visited = set()
while not queue.empty():
    current, steps = queue.get()
    if current >= 10 ** (n - 1):
        print(steps)
        break
    for digit_char in str(current):
        digit = int(digit_char)
        if digit not in (0, 1):
            new_value = digit * current
            if new_value not in visited:
                visited.add(new_value)
                queue.put((new_value, steps + 1))
else:
    print(-1)