n=int(input())
z=[]
q=0
for i in range(n):
	v=int(input())
	q+=v
	z.append(v)
	

def subsetsum(array,num):

    if num == 0 or num < 1:
        return None
    elif len(array) == 0:
        return None
    else:
        if array[0] == num:
            return [array[0]]
        else:
            with_v = subsetsum(array[1:],(num - array[0])) 
            if with_v:
                return [array[0]] + with_v
            else:
                return subsetsum(array[1:],num)
def can_rotate(arr, i=0, cur=0):
    cur %= 360

    if i >= len(arr):
        return cur == 0

    return can_rotate(arr, i+1, cur + arr[i]) or \
            can_rotate(arr, i+1, cur - arr[i])
if (can_rotate(z)):
	print("YES")
else:
	print("NO")


