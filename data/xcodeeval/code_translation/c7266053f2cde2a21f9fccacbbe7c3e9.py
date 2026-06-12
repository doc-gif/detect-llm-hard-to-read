n = int(input())
letters = list(input())
answer = n
for i in range(1, n):
    if letters[:i] == letters[i:2*i]:
        answer = min(answer, n - i + 1)
print(answer)