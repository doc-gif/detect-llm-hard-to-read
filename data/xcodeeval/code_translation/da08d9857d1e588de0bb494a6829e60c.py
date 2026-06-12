def bintodec(s):
    num=0
    mod=1000003
    p=2
    k=0
    for i in range(len(s)-1,-1,-1):
        num+= int(s[i])*(p**k)
        k+=1
        num=num%mod
    return num%mod
    

dic={'>':'1000' , '<' : '1001' , '+' : '1010' , '-' :'1011' , '.':'1100' ,',':'1101','[':'1110',']':'1111'}
s= input()
ans=''
mod=1000003
for i in range(len(s)):
    ans+=dic[s[i]]
print(bintodec(ans))