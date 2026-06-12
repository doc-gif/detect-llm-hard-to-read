def can_equal(s, t):
    for i in range(len(s)):
        for j in range(i):
            if s[i] == s[j] == 'X' and t[i].isdigit() and t[j].isdigit() and t[i] != t[j]:
                return False
    return all(c == d or c in '_X' or d in '_X' for c,d in zip(s, t))

s = input()
if len(s) == 1: exit(print(+(s<'1'or':'<s)))
if s[0] == '0': exit(print(0))
try:
    s.index('_'); s.index('X')
    exit(print(+(int(s)%25<1)))
except ValueError: pass
if len(s) == 1: exit(print(1))

if s[-1] not in '05_X': exit(print(0))
elif s[-2] not in '0257_X' or s[-1] not in '05_X': exit(print(0))

if len(s) == 2:
    if s == '__':
        exit(print(3))
    elif s == 'XX':
        exit(print(0))
    elif s[0] in '_X':
        if s[1] == '0':
            exit(print(1))
        elif s[1] == '5':
            exit(print(2))
        elif not s[1].isdigit():
            exit(print(3))
        else:
            exit(print(0)) # redundant
    else:
        exit(print(+(int(s)%25<1))) # redundant


SUFFIXES = ['00'] if s[-2:] == 'XX' else ['00','25','50','75']

ways = 0
for t in SUFFIXES:
    if not can_equal(s[-2:], t): continue
    X = int(t[s[-2:].index('X')]) if 'X' in s[-2:] else 'X'
    S = ''.join(str(X) if c == 'X' else c for c in s)
    if not S[-1].isdigit(): S = S[:-1] + t[-1]
    if not S[-2].isdigit(): S = S[:-2] + t[-2] + S[-1]
    if S[0] == 'X' and X == 0 or S[0] == '0': continue
    w = 10**S.count('_')
    if S[0] == '_': w -= w//10
    if 'X' in S: w *= 10
    ways += w
    # print(f'{w} ways for suffix {t}')
print(ways)