n=input()
b=input()
if len(n)<len(b):
    print("need tree")
elif len(n)>len(b):
    if b in n:
        print("automaton")
    else:
        f=0
        c=list(set(b))
        d=0
        e=0
        count=0
        while count<len(b):
            for i in range(d,len(n)):
                if b[e]==n[i]:
                    d=i+1
                    e+=1
                    count+=1
                    if i==len(n)-1 and count!=len(b):
                        count=len(n)
                    break
                if count==len(b):
                    break
        if count==len(b):
            print("automaton")
        else:
            for i in range(len(c)):
                d=n.count(c[i])
                e=b.count(c[i])
                if d>=e and e!=0:
                    continue
                else:
                    f=1
                    break
            if f==1:
                print("need tree")
            else:
                print("both")
elif len(n)==len(b):
    f=0
    c=list(set(b))
    for i in range(len(c)):
        d=n.count(c[i])
        e=b.count(c[i])
        if d>=e and e!=0:
            continue
        else:
            f=1
            break
    if f==1:
        print("need tree")
    else:
        print("array")