n = int(input())

l = [0, 0, 0, 0, 0]

for i in range(n):

    a, b = map(int, input().split())

    for j in range(6):

        if a == j: l[j-1] += 1

        if b == j: l[j-1] += 1

if l.count(2) !=5: print("WIN")

else: print("FAIL")





# Made By Mostafa_Khaled