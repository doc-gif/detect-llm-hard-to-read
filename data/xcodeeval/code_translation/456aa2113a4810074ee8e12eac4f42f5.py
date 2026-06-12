def getPow(data,a):
    left = 0
    right = data
    while left <= right:
        mid = (left+right)//2
        if (mid**a)<data:
            left = mid + 1
        elif (mid**a)==data:
            return mid
        else:
            right = mid - 1
    return left-1

def tack():
    data = int(input())
    squ = getPow(data,2)
    cube = getPow(data,3)
    six = getPow(data,6)
    ans = squ + cube - six
    print(ans)


def main():
    n = int(input())
    for x in range(n):
        tack()


main()
