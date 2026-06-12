n=int(input())
if(n%2==1 and n!=1):
    print (n*(n-1)*(n-2))
elif(n==2):
    print(2)
elif(n==1):
    print(1)
elif(n%2==0 and n!=2):
    if(n%3==0):
        print (max(((n-3)*(n-1)*(n-2)),(n*(n-1)*(n-2)//2)))
    else:
        print (max((n*(n-1)*(n-3)),(n*(n-1)*(n-2)//2)))