# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 20:11:35 2018
 
@author: Himanshu Gwalani
 
"""
n,a,x,b,y = map(int,input().split())
l = [a]
if a == n:
    a = 1
else:
    a+=1
while a!=x:
    l.append(a)
    a+=1
    if a == n+1:
        a = 1
l.append(x)
ll = [y]
while b<=y:
    ll.append(b)
    b-=1
    if b==0:
        b = n
flag = False
#print(l)
#print(ll)
for i in range(n):
    if i+1 in l and i+1 in ll:
        flag = True
        break
if flag:
    print("YES")
else:
    print("NO")