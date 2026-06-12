

sx,sy,sl,sr = input().split();
x = int(sx);
y = int(sy);
l = int(sl);
r = int(sr);


qx = [];

now = 1;
while(now <= r):
    qx.append(now);
    now*=x;    

qy = [];
now = 1;
while(now <= r):
    qy.append(now);
    now*=y;

q = [];
for i in qx:
    for j in qy:
        if(l<=i+j and i+j<=r):
            q.append(i+j);

q.sort();
c = [];
# print(q);
lenq = len(q);
ans = 0;
if(lenq > 0):
    ans = r-q[lenq-1];
else:
    ans = r-l+1;
for i in range(0,lenq):
    if(i==0):
        ans=max(ans,q[i]-l);
    else:
        ans=max(ans,q[i]-q[i-1]-1);

print(ans);
