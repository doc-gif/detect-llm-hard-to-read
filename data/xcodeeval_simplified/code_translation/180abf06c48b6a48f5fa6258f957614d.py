input()
numbers = list(map(int, input().split()))
for i in range(len(numbers)):
    for j in range(i + 1, len(numbers)):
        if numbers[j] > numbers[i]:
            numbers[i], numbers[j] = numbers[j], numbers[i]
total = 0
for i in range(0, len(numbers) - 1, 2):
    total += abs(numbers[i] - numbers[i + 1])
print(total)