import sys
lines = sys.stdin.readlines()
n = int(lines[0].strip())
queries = []
for i in range(1, n + 1):
    a, b, c = lines[i].strip().split(" ")
    queries.append((a, int(b), int(c)))
def compare(candidate):
    digits = str(candidate).zfill(4)
    if len(set(digits)) != 4:
        return False
    for a, b, c in queries:
        m = sum(1 for i in range(4) if a[i] == digits[i])
        n = sum(1 for ch in a if ch in digits) - m
        if m != b or n != c:
            return False
    return True
result = 0
count = 0
for i in range(123, 9877):
    if compare(i):
        count += 1
        result = i
    if count >= 2:
        break
if count == 0:
    print("Incorrect data")
elif count == 1:
    print(str(result).zfill(4))
else:
    print("Need more data")