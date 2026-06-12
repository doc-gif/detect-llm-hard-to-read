def mp():  return map(int,input().split())
def lt():  return list(map(int,input().split()))
def pt(x):  print(x)
def ip():  return input()
def it():  return int(input())
def sl(x):  return [t for t in x]
def spl(x): return x.split()
def aj(liste, item): liste.append(item)
def bin(x):  return "{0:b}".format(x)
def printlist(l): print(''.join([str(x) for x in l]))
def listring(l): return ''.join([str(x) for x in l])

n,k = mp()
if k >= n//2:
    print((n*(n-1))//2)
    exit()
result = 0
for i in range(k):
    result += (2*(n-1-2*i)-1)
print(result)
    
        
        