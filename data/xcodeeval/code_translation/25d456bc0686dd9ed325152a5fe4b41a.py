n=int(input())
k=int(input())
A=int(input())
B=int(input())

mans=0
if(k==1):
    print((n - 1) * A)
else:
    while(n!=1):
        # print("HJey")
        ans = 0;
        if (n % k == 0) :
            ans = n / k;
            mans+= min((n - ans) * A, B)
            n=int(n/k)
        else:
            x=(n-n%k)
            if(x==0):
               mans+=((n-1)*A)
               n=1;
            else:
                mans += ((n - x) * A)
                n = x

    print(int(mans))