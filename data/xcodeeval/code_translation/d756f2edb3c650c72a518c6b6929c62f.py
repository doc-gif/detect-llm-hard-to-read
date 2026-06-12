def lint(n):    #to find length of an integer
    h = int(n)
    i= 0
    while(h>0):
          h= int(h/10)
          i=i+1
    len =i
    return len


k =int(input())
list = [1]
n=1
y=1
for y in range (1,k):
        n = n+1;
        p= lint(n)
        for i in range(p,0,-1):
                e= 10**(i-1)
                x = int(n/e)
                z= x%10 
                list.append(z)


        y = y+p
print(list[k-1])

