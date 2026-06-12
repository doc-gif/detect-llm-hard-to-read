n = int(input())
a = [int(x) for x in input().split()]
b = [int(y) for y in input().split()]
alice_score = bob_score = 0
for i in range(n):
    if a[i] > b[i]:
        alice_score += 1
    elif a[i] < b[i]:
        bob_score += 1
if alice_score == 0:
    print(-1)
else:
    print(bob_score // alice_score + 1)