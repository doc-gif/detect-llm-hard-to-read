import sys
lines = sys.stdin.readlines()
n = int(lines[0].strip())
query = []
for i in range(1, n+1):
    (a, b, c) = lines[i].strip().split(" ")
    query.append((a, int(b), int(c)))
def compare(i):
    digits = str(i)
    digits = "0" *(4-len(digits)) + digits
    if len(set(list(digits))) != 4: return False
    for q in query:
        (a, b, c) = q
        m, n = 0, 0
        for i in range(4):
            if a[i] == digits[i]: m += 1
        for l in a:
            if l in digits: n += 1
        n -= m
        if m != b or n != c:
            return False
    return True
res = 0
count = 0
for i in range(123, 9877):
    if compare(i): count += 1; res = i
    if count >= 2: break
if count == 0: print("Incorrect data")
elif count == 1:
    digits = str(res)
    digits = "0" *(4-len(digits)) + digits
    print(digits)
else: print("Need more data")
