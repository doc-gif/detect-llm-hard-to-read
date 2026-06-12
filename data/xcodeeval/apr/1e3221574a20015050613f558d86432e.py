import sys
import math
input = sys.stdin.readline

############ ---- Input Functions ---- ############
def inp():
    return(int(input()))
def inlt():
    return(list(map(int,input().split())))
def insr():
    s = input()
    return(list(s[:len(s) - 1]))
def invr():
    return(map(int,input().split()))

q = inlt()
a = q[0]
b = q[1]

def primeFactors(n):
    l = []
    i = 2
    n1 = n
    while(n1 > 1):
        while((n1 % i) == 0):
            l.append(i)
            n1 = n1 // i

        i = i + 1
    return l

p = primeFactors(a)
q = primeFactors(b)

def count(x,l):
    ct = 0
    for i in l:
        if(i == x):
            ct = ct + 1
    return ct

a1 = count(2,p)
b1 = count(3,p)
c1 = count(5,p)

a2 = count(2,q)
b2 = count(3,q)
c2 = count(5,q)

k = a // (2**a1 * 3**b1 * 5**c1)
j = b // (2**a2 * 3**b2 * 5**c2)

if(k == j):
    sum = 0
    sum = sum + abs(c1 - c2)
    sum = sum + abs(b1 - b2)
    sum = sum + abs(a1-a2)
    print(sum)



else:
    print(-1)