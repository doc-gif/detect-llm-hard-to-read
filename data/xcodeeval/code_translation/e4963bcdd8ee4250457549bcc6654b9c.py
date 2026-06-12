from sys import stdin
def in_row(ch):
    if ch=='f': return 1
    if ch=='a': return 4
    if ch=='b': return 5
    if ch=='c': return 6
    if ch=='d': return 3
    if ch=='e': return 2
li=input().strip()
n=int(li[0:-1])
s=li[-1]
time=0
tmp=(n-1)//4
time += tmp*3 + tmp*13
tmp=(n-1)%4
if tmp==1 or tmp==3:
    time += 7
time += in_row(s)

print(time)



