n=int(input())
n=n*2
arr=[int(x) for x in input().split()]
arr=sorted(arr)
x=arr[n-1]
for i in range(0,n):
    for j in range(i+1,n):
        # i,j 选中的single
        a,h,q=0,0,0
        while h<n:
            if h==i or h == j:
                pass

            else:
                if q%2==0:
                    a-=arr[h]
                else:
                    a+=arr[h]
                q+=1
            h+=1
        # print(a)    
        x=min(x,a)
print(x)