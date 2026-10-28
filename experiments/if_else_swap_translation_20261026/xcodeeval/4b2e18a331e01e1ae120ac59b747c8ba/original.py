#n is the base and k is the result, need to find min x s.t. f(x)=k, length is the length of n
import math
def find(n,k,length):
    if k<n:
        return [k]
    else:
        MAX=0
        index=1
        
        for i in range(1,length+1):
            temp=k%(10**i)
            if temp>=n:
                break
            else:
                if temp>=10**(i-1):
                    MAX=temp
                    index=i
                 
        res=k-MAX
        #empty+=[MAX]
        res=res//(10**index)
        #print(MAX,res,n,k,index)
        return find(n,res,length)+[MAX]
                
            
        
        
        

n=int(input())
k=int(input())
length=int(math.log(n-1,10))+1
ANS=find(n,k,length)[::-1]
ans=0
temp=1

for i in range(len(ANS)):
    ans+=ANS[i]*temp
    temp*=n
#print(ANS)    
print(ans)    
    
            
        
        
        
    