input()
sek=input().split("W")
s=[]
for i in sek:
	 if i!="": s.append(i)
print(len(s))
for i in s:
	if i!="": print(len(i), end=" ")
