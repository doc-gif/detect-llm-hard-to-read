l1 = list(map(int, input().split()))
l2 = list(map(int, input().split()))
l3 = list(map(int, input().split()))
l4 = list(map(int, input().split()))
count = 0
if l1[3] == 1 and (
    l1[0] == 1 or l1[1] == 1 or l1[2] == 1 or l2[0] == 1 or l3[1] == 1 or l4[2] == 1
):
    count = 1
elif l2[3] == 1 and (
    l1[2] == 1 or l2[0] == 1 or l2[1] == 1 or l2[2] == 1 or l3[0] == 1 or l4[1] == 1
):
    count = 1
elif l3[3] == 1 and (
    l1[1] == 1 or l2[2] == 1 or l3[0] == 1 or l3[1] == 1 or l3[2] == 1 or l4[0] == 1
):
    count = 1
elif l4[3] == 1 and (
    l1[0] == 1 or l2[1] == 1 or l3[2] == 1 or l4[0] == 1 or l4[1] == 1 or l4[2] == 1
):
    count = 1
print("YES" if count == 1 else "NO")