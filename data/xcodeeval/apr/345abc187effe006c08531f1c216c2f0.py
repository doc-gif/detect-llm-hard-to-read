import sys

def solve():
    n, = rv()
    works = 0
    lastworks = -1
    guesses = list()
    for i in range(n):
        a, b, c, = rv()
        acopy = a
        charcount = [0] * 10
        for x in range(4):
            charcount[acopy % 10] += 1
            acopy //= 10
        guesses.append((tolist(a), b, c, charcount))

    for i in range(1, 10000):
        if different(i):
            l = tolist(i)
            icopy = i
            charcount = [0] * 10
            for x in range(4):
                charcount[icopy % 10] += 1
                icopy //= 10
            count = 0
            for guess in guesses:
                bulls, cows = 0, 0
                for j in range(4):
                    if l[j] == guess[0][j]: bulls += 1
                for j in range(10):
                    if charcount[j] > 0 and guess[3][j] > 0: cows+=1
                cows -= bulls


                if bulls == guess[1] and cows == guess[2]:
                    count += 1
            if count == n:
                works += 1
                lastworks = i
    if works == 0:
        print("Incorrect data")
    elif works == 1:
        print(lastworks)
    else:
        print("Need more data")

def tolist(i):
    il = list()
    while i > 0:
        il.append(i % 10)
        i //= 10
    while len(il) < 4: il.append(0)
    return il[::-1]

def different(i):
    count = [0] * 10
    for x in range(4):
        count[i % 10] += 1
        i //= 10
    for val in count:
        if val > 1: return False
    return True


def prt(l): return print(''.join(l))
def rv(): return map(int, input().split())
def rl(n): return [list(map(int, input().split())) for _ in range(n)]
if sys.hexversion == 50594544 : sys.stdin = open("test.txt")
solve()