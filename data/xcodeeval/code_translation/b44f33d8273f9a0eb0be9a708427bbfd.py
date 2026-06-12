def sum_digit(a):
    k=a
    dem=0
    while k>0:
        x=k%10
        dem+=x
        k=int(k/10)
    return (dem)
ch=input()
n=int(ch)
ch=str(n)
if len(ch)>1:
    n1=str(int(ch[0])-1)
    if n1=='0':
        n1=''
    for i in range(len(ch)-1):
        n1+='9'
    x=int(n1)
    y=n-x
    print (sum_digit(x)+sum_digit(y)) 
else:
    print (n)