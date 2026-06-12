first = int(input())
numbers = [first]
seen_one_count = 0
while True:
    if first == 1:
        seen_one_count += 1
    if seen_one_count == 2:
        break
    first += 1
    while first % 10 == 0:
        first //= 10
    if first not in numbers:
        numbers.append(first)
print(len(numbers))