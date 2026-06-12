import string
import re

values={str(d): d for d in range(10) }
for ch in string.ascii_uppercase:
    values[ch] = ord(ch) - 55

def convert(s, i):
    x=0
    for ch in s:
        d = values[ch]
        if d>=i:
            return None
        x = i*x+d
    return x

match=re.match('0*(\w+):0*(\w+)',input().strip())
a,b=match.groups([1, 2])

ans = []
for i in range(2, 60):
    h = convert(a, i)
    m = convert(b, i)
    if h == None or m == None:
        continue
    if h < 24 and m < 60:
        ans.append(i)

if len(ans) == 0:
    print(0)
elif len(a) + len(b) == 2:
    print(-1)
else:
    print(*ans)