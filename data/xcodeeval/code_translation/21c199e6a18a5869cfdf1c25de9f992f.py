import math
import sys
m=998244353
input=sys.stdin.readline

fibo=[1,1]
for i in range(200002):
    fibo.append(fibo[-1]+fibo[-2])
    fibo[-1]%=m

n=int(input())
deno=1<<n
inv=pow(deno,m-2,m)
ans=(fibo[n-1]*inv)%m
print(ans)
    
            
    
        

    
    
        
    

    
    


