l = list(input().split(':'))
if(int(l[0][::-1]) >= int(l[1])):
    print(int(l[0][::-1]) - int(l[1]))
else:
    m = int(l[1])
    h = int(l[0])
    ans = 0
    while(True):
        m += 1
        ans += 1
        if(m == 60):
            m = 0
            h += 1
            if(h == 24):
                h = 0
                st = "00:00"
            else:
                if(len(str(h)) == 1):
                    st = "0"+str(h)+"00"
                else:
                    st = str(h)+"00"
        else:
            if(len(str(m)) == 1):
                if(len(str(h)) == 1):
                    st = "0"+str(h)+"0"+str(m)
                else:
                    st = str(h)+"0"+str(m)
            else:
                if(len(str(h) == 1)):
                    st = "0"+str(h)+str(m)
                else:
                     st = str(h)+str(m)
        if(st == st[::-1]):
            print(ans)
            break


