a=input()
b=input()
c=input()
xcount=0
ocount=0
for t in list(a):
    if t is "0":
        ocount+=1
    if t is "X":
        xcount+=1
for t in list(b):
    if t is "0":
        ocount+=1
    if t is "X":
        xcount+=1
for t in list(c):
    if t is "0":
        ocount+=1
    if t is "X":
        xcount+=1
if xcount - ocount > 1 or ocount > xcount:
    print("illegal")
elif (a.find("XXX") != -1 or b.find("XXX") != -1 or c.find("XXX") != -1 or (a[:1]+b[:1]+c[:1]).find("XXX") != -1 or (a[1:2]+b[1:2]+c[1:2]).find("XXX") != -1 or (a[-1]+b[-1]+c[-1]).find("XXX")!=-1 or (a[:1]+b[1:2]+c[-1]).find("XXX") != -1 or (a[-1]+b[1:2]+c[:1]).find("XXX") != -1) and (a.find("000") != -1 or b.find("000") != -1 or c.find("000") != -1 or (a[:1]+b[:1]+c[:1]).find("000") != -1 or (a[1:2]+b[1:2]+c[1:2]).find("000") != -1 or (a[-1]+b[-1]+c[-1]).find("000")!=-1 or(a[:1]+b[1:2]+c[-1]).find("000") != -1 or (a[-1]+b[1:2]+c[:1]).find("000") != -1):
    print("illegal")
elif a.find("XXX") != -1 or b.find("XXX") != -1 or c.find("XXX") != -1 or (a[:1]+b[:1]+c[:1]).find("XXX") != -1 or (a[1:2]+b[1:2]+c[1:2]).find("XXX") != -1 or (a[-1]+b[-1]+c[-1]).find("XXX")!=-1:
    print("the first player won")
elif a.find("000") != -1 or b.find("000") != -1 or c.find("000") != -1 or (a[:1]+b[:1]+c[:1]).find("000") != -1 or (a[1:2]+b[1:2]+c[1:2]).find("000") != -1 or (a[-1]+b[-1]+c[-1]).find("000")!=-1:
    print("the second player won")
elif (a[:1]+b[1:2]+c[-1]).find("XXX") != -1 or (a[-1]+b[1:2]+c[:1]).find("XXX") != -1:
    print("the first player won")
elif (a[:1]+b[1:2]+c[-1]).find("000") != -1 or (a[-1]+b[1:2]+c[:1]).find("000") != -1:
    print("the second player won")
elif xcount>ocount and xcount!=5:
    print("second")
elif xcount==count:
    print("first")
else:
    print("draw")