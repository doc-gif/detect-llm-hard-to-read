x=int(input())
b=[str(i) for i in input().split()]
# print(b)
hh=b[0]	
mm=b[1]
if hh[0]=="0":
	hh=hh[1:]
	hh=int(hh)
if mm[0]=="0":
	mm=mm[1:]
	mm=int(mm)

# print(hh,mm)

nh=hh
nm=mm
f=0
y=0
while(f==0):
	nh=str(nh)
	nm=str(nm)	
	if '7' in nh or '7' in nm:
		f=1
		break
	nh=int(nh)
	nm=int(nm)
	if x>nm:
		d= x-nm
		if nm==0:
			nm=23
		else:
			nm-=1
		nm= 60-d
	else:
		nm-=x
	y+=1

print(y)












'''


'''
	