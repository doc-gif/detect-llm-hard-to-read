s=input()
k=[]
if len(s)==1:
    if s=='_' or s=='X'or s=='0':print(1)
    else:print(0)
else:
    if s[0]=='0':print(0);exit()
    if s[-2]+s[-1]in ['25','50','75','00','XX','X_','_X','__', '2_','5_','7_','2X','5X','7X','X5','X0','_5','_0','0X','0_']and len(s)>2:k.append(1)
    elif s[-2]+s[-1]in ['25','50','75','XX','X_','_X','__', '2_','5_','7_','2X','5X','7X','X5','X0','_5','_0','0X','0_']:k.append(1)
    else:print(0);exit()
    
    if s[-2]=='0'and s[-1]=='_':
        s=s[:len(s)-2]+'  '
    elif s[-2]=='0'and s[-1]=='X':
        if s[0]=='X':print(0);exit()
        else:s=s.replace('X',' ')
    
    if s[-1]=='X' and s[-2]=='X':
        if len(s)>2 and s[0]!='X':
            k.append(1);s=s.replace('X',' ')
        else:print(0);exit()
    elif s[-1]=='X':
        if s[-2]in['2','5','7']:k.append(1);s=s.replace('X',' ')
        elif s[-2]=='_':
            if len(s)>2 and s[0]!='X':
                k.append(4)
                s=s[:len(s)-2]+'  '
                s=s.replace('X',' ')
            else:
                s=s[:len(s)-2]+'  '
                k.append(3)
                s=s.replace('X',' ')
    elif s[-1]=='_':
        if s[-2]in['2','5','7']:k.append(1);s=s[:len(s)-1]+' '
        elif s[-2]=='_' or s[-2]=='X':
            if s[-2]=='_':
                if len(s)>2:
                    k.append(4)
                    s=s[:len(s)-2]+'  '
                else:
                    k.append(3)
                    s=s[:len(s)-2]+'  '
            elif s[-2]=='X':
                if len(s)>2 and s[0]!='X':
                    k.append(4)
                    s=s[:len(s)-2]+'  '
                    s=s.replace('X',' ')
                else:
                    k.append(3)
                    s=s[:len(s)-2]+'  '
                    s=s.replace('X',' ')
    if s[-2]=='_':
        if s[-1]=='0'and len(s)<3:k.append(1)
        else:k.append(2)
        s=s[:len(s)-2]+'  '
    elif s[-2]=='X':
        s=s.replace('X',' ')
        if s[-1]=='0'and len(s)<3:k.append(1)
        else:k.append(2)
    for i in range(len(s)):
        ss=s[i]
        if ss=='_'and i!=0:k.append(10)
        elif ss=='_'and i==0:k.append(9)
        elif ss=='X'and i==0:k.append(9);s=s.replace('X',' ')
        elif ss=='X'and i!=0:k.append(10);s=s.replace('X',' ')
    if len(k)>0:
        print(eval('*'.join([str(i)for i in k])))
    else:print(0)
                
                
        
