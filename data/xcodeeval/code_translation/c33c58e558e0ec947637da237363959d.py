a,b,c,d=input(),input(),input(),input()
a=len(a)-2
b=len(b)-2
c=len(c)-2
d=len(d)-2
e=False
if 2*a<=c and 2*a<=b and 2*a<=d or a>=2*c and a>=2*b and a>=2*d: e='A'
if 2*b<=a and 2*b<=c and 2*b<=d or b>=2*a and b>=2*c and b>=2*d:
    if e==False:
        e='B'
    else:
        e='C'
if 2*c<=a and 2*c<=b and 2*c<=d or c>=2*a and c>=2*b and c>=2*d:
    if e==False:
        e='C'
    else:
        e='C'
if 2*d<=a and 2*d<=b and 2*d<=c or d>=2*a and d>=2*b and d>=2*c:
    if e==False:
        e='D'
    else:
        e='C'
if e==False: e='C'
print(e)