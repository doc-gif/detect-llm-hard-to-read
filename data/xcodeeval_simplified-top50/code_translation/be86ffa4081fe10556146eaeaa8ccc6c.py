n, budget = map(int, input().split())
numbers = list(map(int, input().split()))
even_count = 0
odd_count = 0
cuts = []
current_sum = 0
answer = 0
for i in range(n):
    if numbers[i] % 2:
        odd_count += 1
    else:
        even_count += 1
    if even_count == odd_count and i < n - 1:
        cuts.append(abs(numbers[i + 1] - numbers[i]))
        even_count = 0
        odd_count = 0
cuts.sort()
for cost in cuts:
    answer += 1
    current_sum += cost
    if current_sum > budget:
        answer -= 1
        print(answer)
        exit(0)
print(answer)