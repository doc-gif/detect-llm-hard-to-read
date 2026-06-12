import sys
sys.setrecursionlimit(100000)
 
def _r(): return sys.stdin.buffer.readline()
def rs(): return _r().decode('ascii').strip()
def rn(): return int(_r())
def rnt(): return map(int, _r().split())
def rnl(): return list(rnt())

def solve(s):
    if len(s) == 1:
        return int(s in '0_X')
    def _solve(s):
        if s[0] == '0':
            return 0
        uc = s.count('_')
        xm = 10 if 'X' in s else 1
        return xm*10**uc if s[0] not in 'X_' else xm*10**uc//10*9
    l2 = s[-2:]
    if l2 in ('25', '50', '75', '00'):
        return _solve(s)
    elif l2 == 'XX':
        return _solve(s.replace('X', '0'))
    elif l2 == 'X5':
        return _solve(s.replace('X', '2')) + _solve(s.replace('X', '7'))
    elif l2 == 'X0':
        return _solve(s.replace('X', '5')) + _solve(s.replace('X', '0'))
    elif l2 == '2X' or l2 == '7X':
        return _solve(s.replace('X', '5'))
    elif l2 == '5X' or l2 == '0X':
        return _solve(s.replace('X', '0'))
    elif l2 == '__':
        return _solve(s[:-2] + '25') + _solve(s[:-2] + '50') + _solve(s[:-2] + '75') + _solve(s[:-2] + '00')
    elif l2 == '_5':
        return _solve(s[:-2] + '25') + _solve(s[:-2] + '75')
    elif l2 == '_0':
        return _solve(s[:-2] + '50') + _solve(s[:-2] + '00')
    elif l2 == '2_' or l2 == '7_':
        return _solve(s[:-1] + '5')
    elif l2 == '5_':
        return _solve(s[:-1] + '0')
    elif l2 == '_X' or l2 == 'X_':
        return _solve(s.replace('X', '0')[:-2] + '00') + _solve(s.replace('X', '0')[:-2] + '50') + _solve(s.replace('X', '5')[:-2] + '25') + _solve(s.replace('X', '5')[:-2] + '75')
    return 0

print(solve(rs()))
 
# for _ in range(rn()):
#     n = rn()
#     edges = [rnt() for _ in range(n-1)]
#     print(solve(n, edges))