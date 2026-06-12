
from sys import *
from heapq import *
from collections import defaultdict
from itertools import permutations
import os, sys
from io import IOBase, BytesIO
M=10**9+7
def graph_as_tree_1_root():
    n=int(input())
    dict=defaultdict(list)
    for _ in range(n-1):
        x,y=list(map(int,input().split()))
        dict[x].append(y)
        dict[y].append(x)
    tree=[[1]]
    temp=[1]
    vall=0
    seen=set([i for i in range(2,n+1)])
    lol=[]
    while len(seen)>0:
        #print(seen)
        lol=list(seen)
        tt=[]
        for x in temp:
            aa=[]
            for val in dict[x]:
                if val in seen:
                    aa+=[val]
                    seen.remove(val)
            dict[x]=aa
            tt+=aa
        tree.append(tt)
        temp=tt
        vall+=1
    for x in lol:
        dict[x]=[]
    
    print(tree,dict)
def pow(a,b):
    res=1
    while b>0:
        if b&1:
            res*=a
        a*=a
        b>>=1
    return res
def powmod(a,b,m):
    res=1
    while b>0:
        if b&1:
            res=((res*a)%m)
        a*=a
        b>>=1
    return res
def inv(a,m):
    return powmod(a,m-2,m)
def alldivisors(n) : 
    list = []  
    arr=[]
    for i in range(1, int(sqrt(n) + 1)) :
        if (n % i == 0) : 
            if (n / i == i) : 
                arr+=[i]
            else :
                arr+=[i]
                list.append(n//i)  
    arr+=list[::-1]
    return arr
def primefactorisation(n):
    potentional_p = 3
    itog_list = defaultdict(int)
    if n % 2 == 0:
        itog_list[2] = 0
    while n % 2 == 0:
        n = n // 2
        itog_list[2] += 1
    while n - 1:
        if potentional_p > (n**0.5):
            itog_list[n] += 1
            return itog_list
        while n % potentional_p == 0:
            n = n // potentional_p
            itog_list[potentional_p] += 1
        potentional_p += 2
    return itog_list



def main():
    n,m=list(map(int,input().split()))
    val=((1<<m)-1)%M
    
    val=powmod(val,n,M)
    print(val)








BUFSIZE = 8192
class FastIO(BytesIO):
    newlines = 0
 
    def __init__(self, file):
        self._file = file
        self._fd = file.fileno()
        self.writable = "x" in file.mode or "w" in file.mode
        self.write = super(FastIO, self).write if self.writable else None
 
    def _fill(self):
        s = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
        self.seek((self.tell(), self.seek(0,2), super(FastIO, self).write(s))[0])
        return s
 
    def read(self):
        while self._fill(): pass
        return super(FastIO,self).read()
 
    def readline(self):
        while self.newlines == 0:
            s = self._fill(); self.newlines = s.count(b"\n") + (not s)
        self.newlines -= 1
        return super(FastIO, self).readline()
 
    def flush(self):
        if self.writable:
            os.write(self._fd, self.getvalue())
            self.truncate(0), self.seek(0)
 
class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s:self.buffer.write(s.encode('ascii'))
        self.read = lambda:self.buffer.read().decode('ascii')
        self.readline = lambda:self.buffer.readline().decode('ascii')
 
sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip('\r\n')
 
if __name__ == '__main__':
    main()
#threading.Thread(target=main).start()






