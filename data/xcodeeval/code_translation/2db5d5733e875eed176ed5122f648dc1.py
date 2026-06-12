n = int(input())

def getFactors(x):

    factors = []
    for i in range(1, int(n**0.5) + 1):
       if x % i == 0:
           factors.append(i)
    
    return factors

f = getFactors(n)
b = int( n // f[-1])
a = int( n // b)
print( a, b)

