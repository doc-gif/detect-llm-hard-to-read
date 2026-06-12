n = input()[::-1]
c0 = n.count('0')
c2 = n.count('2')
c5 = n.count('5')
c7 = n.count('7')
s = 1e9
if c0 > 1:
    i = n.find('0')
    j = n.find('0', i + 1)
    s = min(s, i + j - 1)
if c2 and c5:
    i = n.find('2')
    j = n.find('5')
    r = j + i - 1 + (j > i)
    i, j = sorted([i, j])
    m = n[:i] + n[i + 1: j] + n[j + 1:]
    if not (m and m[-1] == '0'):
        s = min(s, r)
if c5 and c0:
    i = n.find('5')
    j = n.find('0')
    s = min(s, j + i - 1 + (j > i))
if c7 and c5:
    i = n.find('7')
    j = n.find('5')
    r = j + i - 1 + (j > i)
    i, j = sorted([i, j])
    m = n[:i] + n[i + 1: j] + n[j + 1:]
    if not (m and m[-1] == '0'):
        s = min(s, r)
print(-1 if s == 1e9 else s)
