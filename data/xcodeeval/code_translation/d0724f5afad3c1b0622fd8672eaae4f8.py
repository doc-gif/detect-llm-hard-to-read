#Finaly

num=input()

if(ord(num[0])>=ord('5') and num[0]!='9'):
    ans=chr((9-(ord(num[0])-ord('0')))+ord('0'))
else:
    ans=num[0]


for i in range(1,len(num)):
    if ord(num[i])>=ord('5'):
        ans+=chr((9-(ord(num[i])-ord('0')))+ord('0'))
    else:
         ans+=num[i]
        
        
print(ans)
