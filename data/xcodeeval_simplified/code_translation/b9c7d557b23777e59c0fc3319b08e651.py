l, r = map(int, input().split())
numbers = []
def generate_lucky_numbers(n):
    numbers.append(n)
    if n > 10 * r:
        return
    generate_lucky_numbers(10 * n + 4)
    generate_lucky_numbers(10 * n + 7)
generate_lucky_numbers(0)
numbers.sort()
def prefix_sum(limit):
    total = 0
    for i in range(1, len(numbers)):
        current = numbers[i]
        previous = numbers[i - 1]
        total += current * (min(current, limit) - min(previous, limit))
    return total
print(prefix_sum(r) - prefix_sum(l - 1))