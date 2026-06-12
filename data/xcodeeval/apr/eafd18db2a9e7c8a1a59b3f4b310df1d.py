from sys import stdin, gettrace

if gettrace():
    inputi = input
else:
    def input():
        return next(stdin)[:-1]


    def inputi():
        return stdin.buffer.readline()

def tide(k, t):
    t = t%(2*k)
    if t <= k:
        return t
    else:
        return 2*k - t

def solve():
    n,k,l = map(int, inputi().split())
    dd = [int(a) for a in inputi().split()]
    if max(dd) > l:
        print("No")
        return
    t = 0
    def can_finish(t,i):
        if i == n:
            return True
        for t1 in range(t+1, t+2*k):
            if dd[i] + tide(k,t1) > l:
                return False
            else:
                if can_finish(t1, i+1):
                    return True
        return False
    for i in range(2*k):
        if can_finish(i,0):
            print("Yes")
            return
    else:
        print("No")




def main():
    t = int(inputi())
    for _ in range(t):
        solve()


if __name__ == "__main__":
    main()