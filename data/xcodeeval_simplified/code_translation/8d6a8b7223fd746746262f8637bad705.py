class letter:
    def __init__(self, char, value):
        self.char = char
        self.value = value
    def __lt__(self, other):
        return self.value < other.value
n = int(input())
s = input()
values = list(map(int, input().split()))
candi = [[] for _ in range(n // 2)]
ans = 0
for i, val in enumerate(values):
    idx = min(i, n - i - 1)
    candi[idx].append(letter(s[i], val))
    ans += val
for i in range(n // 2):
    candi[i].sort()
ti = [0] * 26
sum_pairs = 0
for i in range(n // 2):
    if candi[i][0].char == candi[i][1].char:
        ans -= candi[i][0].value
        ti[ord(candi[i][0].char) - ord("a")] += 1
        sum_pairs += 1
mx = 0
p = 0
for i in range(26):
    if ti[i] > mx:
        mx = ti[i]
        p = i
b = []
for i in range(n // 2):
    c0 = ord(candi[i][0].char) - ord("a")
    c1 = ord(candi[i][1].char) - ord("a")
    if c0 != p and c1 != p and candi[i][0].char != candi[i][1].char:
        b.append(candi[i][0])
b.sort()
i = 0
while mx * 2 > sum_pairs:
    sum_pairs += 1
    ans -= b[i].value
    i += 1
print(ans)