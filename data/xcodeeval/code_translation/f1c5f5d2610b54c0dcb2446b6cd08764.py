
def isAtLeastHalf(k, n):
    V = 0
    P = 0
    if n%2 == 0:
        least = (n//2)
    else:    
        least = (n//2)+1
    res = False
    while(n > 0 and k > 0):
        #print('n=',n, ' k=', k)
        if n>=k:
            V += k
            n -= k
        else:
            V += n
            n=0
        temp = (n//10)
        P += temp
        n -= temp
        if (V>= least):
            res = True
            break
    #print('Partial', V,P, res)        
    return res

def searchMiniumCandies(n, l, r, res = -1):
    #print(n,' l=',l,' r=',r,res)
    if r >= l:
        mid = l + (r - l)//2
        if isAtLeastHalf(mid, n):
            res = mid
            #print('TRUE', l, mid-1)
            return searchMiniumCandies(n, l, mid-1, res )
        else:
            #print('False')

            return searchMiniumCandies(n, mid+1, r, res )
    else:
        #print('retornando', res)
        return res

n = int(input())
print(searchMiniumCandies(n, 0,n))                