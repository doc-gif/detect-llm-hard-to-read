n=int(input())
w=input()
n=str(n)
t=0
p=[0]*len(n)
if n=='0':
    if w=='0':
        print('OK')
    else:
        print('WRONG_ANSWER')
else:
    if '1' in n:
        t=1
    else:
        if '2' in n:
            t=2
        else:
            if '3' in n:
                t=3
            else:
                if '4' in n:
                    t = 4
                else:
                    if '5' in n:
                        t = 5
                    else:
                        if '6' in n:
                            t = 6
                        else:
                            if '7' in n:
                                t = 7
                            else:
                                if '8' in n:
                                    t = 8
                                else:
                                    t=9
    s=str(t)
    for i in range (0,10):
        if i==t:
            s=s+str(i)*(n.count(str(i))-1)
        else:
            s = s + str(i) * (n.count(str(i)))
    if s==w:
        print('OK')
    else:
        print('WRONG_ANSWER')