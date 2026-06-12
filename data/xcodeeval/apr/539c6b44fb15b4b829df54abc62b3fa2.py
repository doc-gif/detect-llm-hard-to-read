#import sys
#sys.stdin = open('in', 'r')
#n = int(input())
#a = [int(x) for x in input().split()]
class minheap:
    def __init__(self, n):
        self.a = [0 for i in range(n)]
        self.n = 0

    def __init__(self):
        self.a = []
        self.n = 0

    def load(self, initial):
        self.a = [] + initial
        self.n = len(self.a)
        for i in range((self.n-2) // 2, -1, -1):
            self.hdown(i)

    def hup(self, ind):
        if ind > 0:
            parent = (ind - 1) // 2
            if self.a[parent] > self.a[ind]:
                tmp = self.a[ind]
                self.a[ind] = self.a[parent]
                self.a[parent] = tmp
                self.hup(parent)

    def hdown(self, ind):
        l = ind*2 + 1
        r = ind*2 + 2
        newind = ind
        if l < self.n and self.a[newind] > self.a[l]:
            newind = l
        if r < self.n and self.a[newind] > self.a[r]:
            newind = r
        if newind != ind:
            tmp = self.a[ind]
            self.a[ind] = self.a[newind]
            self.a[newind] = tmp
            self.hdown(newind)

    def push(self, v):
        if self.n == len(self.a):
            self.a.append(v)
        else:
            self.a[self.n] = v
        self.hup(self.n)
        self.n += 1
        
    def pop(self):
        if self.n > 0:
            res = self.a[0]
            self.n -= 1
            if self.n > 0:
                self.a[0] = self.a[self.n]
                self.a[self.n] = 0
                self.hdown(0)
            return res
        else:
            raise "empty heap"

n,x,y = map(int, input().split())

h = minheap()
d = {}
h.push((0, n))

r = -1
while r == -1:
    xh,nh = h.pop()
    if nh not in d:
        d[nh] = xh
        if nh == 1:
            r = xh + x
        else:
            if (nh - 1) not in d:
                h.push((xh + x, nh - 1))
            if nh & 1 == 0 and (nh // 2) not in d and y < (nh//2)*x:
                h.push((xh + y, nh // 2))
            if (nh + 1) not in d:
                h.push((xh + x, nh + 1))
            
            

print(r)
