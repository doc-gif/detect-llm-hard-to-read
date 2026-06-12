# Asad Alwadi (RAND DEEB) ;)
num = list(input())
carry = 0
ans = []
for i in range(0,len(num)):
    if(num[i] == '1' or carry):
        ans.append('1')

    else:
        if(num[i] == '0'):
            ans.append('0')
        else:
            ans.append('1')
            carry = 1
ans = "".join(ans)
print(int(ans,2))