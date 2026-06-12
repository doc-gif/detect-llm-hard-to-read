import sys

def digitsNum(x, base):
    ret = 0
    while x>0:
        ret += 1
        x //= base
    return ret

n, m= sys.stdin.read().split()

base = int(max(max(n), max(m)))+1
n = int(n, base)
m = int(m, base)

print(digitsNum(n+m, base))