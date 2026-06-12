#inspired by throwawayatcoder
from collections import *
import sys  

# "". join(strings)  
    
def ri():
    return int(input())
 
def rl():
    return list(map(int, input().split()))
    

t=ri()
for _ in range(t):
    n,k,l=rl()
    dd=rl()
    p = list(range(k+1))+ list(range(k))[::-1]

    def get_depth(t,i):

        return dd[i] + p[t%(2*k)]

    # def getDepth2(t, i):
    #     m = t % (2 * k)
    #     tide = min(m, 2 * k - m)
    #     depth = dd[i] + tide
    #     return depth
    
    # for z in range(n):
    #     for T in range(2*k):
    #         print (get_depth(T,z)-getDepth2(T, z))
    

    def canWinFromThere(t,i):
        if i==n:
            return True
        if get_depth(t,i)>l:
            return False
        
            
        for wait in range(2*k):
            if get_depth(t+wait, i)>l:
                break
            
            if canWinFromThere(t+wait+1,i+1):
                return True
        return False

    for u in range(2*k):
        if canWinFromThere(u,0): 
            print("Yes")
            break
    else:
        print("No")

                


