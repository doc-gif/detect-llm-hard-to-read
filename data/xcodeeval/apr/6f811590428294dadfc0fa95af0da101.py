import itertools
import heapq
import collections
import math
import sys


input = sys.stdin.readline


############ ---- Input Functions ---- ############
def inp():
    return (int(input()))


def inlt():
    return (list(map(int, input().split())))


def insr():
    s = input()
    return (list(s[:len(s) - 1]))


def invr():
    return (map(int, input().split()))


def inis():
    return (input().split())


def stlt():
    return list(map(str, input().split()))


###################################################

# # Code to find top 3 elements and their counts
# # using most_common
#
# arr = [1, 3, 4, 1, 2, 1, 1, 3, 4, 3, 5, 1, 2, 5, 3, 4, 5]
# counter = Counter(arr)
# top_three = counter.most_common()
# print(sorted(top_three))
#
#
# # Python code to find 3 largest and 4 smallest
# # elements of a list.
#
# grades = [110, 25, 38, 49, 20, 95, 33, 87, 80, 90, 110]
# print(heapq.nlargest(3, grades))
# print(heapq.nsmallest(4, grades))

########################################################################
#-----------------------------Functions--------------------------------#
########################################################################

def SieveOfEratosthenes(n):
    prime = [True for i in range(n + 1)]
    p = 2
    l = []
    while (p * p <= n):
        if (prime[p] == True):
            for i in range(p * p, n + 1, p):
                prime[i] = False
        p += 1
    for p in range(2, n + 1):
        if prime[p]:
            l.append(p)
    return l


def isPrime(n):
    prime_flag = 0

    if n > 1:
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                prime_flag = 1
                break
        if prime_flag == 0:
            return True
        else:
            return False
    else:
        return False


def gcdofarray(a):
    x = 0
    for p in a:
        x = math.gcd(x, p)
    return x


# method to print the divisors
def printDivisors(n):
    # Note that this loop runs till square root
    i = 1
    ans = []
    while i <= math.sqrt(n):

        if (n % i == 0):

            # If divisors are equal, print only one
            if (n / i == i):
                ans.append(i)
            else:
                # Otherwise print both
                ans.append(i)
                ans.append(n // i)
        i = i + 1
    ans.sort()
    return ans


def CountDivisors(n):
    # Note that this loop runs till square root
    i = 1
    ans = []
    while i <= math.sqrt(n):

        if (n % i == 0):

            # If divisors are equal, print only one
            if (n / i == i):
                ans.append(i)
            else:
                # Otherwise print both
                ans.append(i)
                ans.append(n // i)
        i = i + 1
    ans.sort()
    return len(ans)


def binaryToDecimal(n):
    return int(n, 2)


def countTriplets(a, n):
    s = set()
    for i in range(n):
        s.add(a[i])
    count = 0
    for i in range(n):
        for j in range(i + 1, n, 1):
            xr = a[i] ^ a[j]
            if xr in s and xr != a[i] and xr != a[j]:
                count += 1
    return int(count // 3)


def generate_twin_prime(n):
    a = 0
    for i in range(1, n + 1):
        j = i + 2
        if isPrime(i) and isPrime(j):
            if 2 ^ (i ^ j) == 0:
                a += 1
    return a


def smallestDivisor(n):
    if (n % 2 == 0):
        return 2
    i = 3
    while (i * i <= n):
        if (n % i == 0):
            return i
        i += 2
    return n


def countOdd(L, R):
    N = (R - L) // 2

    # if either R or L is odd
    if (R % 2 != 0 or L % 2 != 0):
        N += 1

    return N


def isPalindrome(s):
    return s == s[::-1]


def sufsum(test_list):
    test_list.reverse()
    res = [sum(test_list[: i + 1]) for i in range(len(test_list))]
    return res


def prsum(lst):
    return (list(itertools.accumulate(lst)))


def badachotabadachota(nums):
    nums.sort()
    i = 0
    j = len(nums) - 1
    ans = []
    cc = 0
    while len(ans) != len(nums):
        if cc % 2 == 0:
            ans.append(nums[j])
            j -= 1
        else:
            ans.append(nums[i])
            i += 1
        cc += 1
    return ans

    
# ########################################################################
# #-----------------------------Code Here--------------------------------#
# ########################################################################

for _ in range(inp()):
    # n = inp()
    # u = inlt()
    # s = inlt()
    # d = {}
    # ans = []
    # for i in range(n):
    #     if u[i] in d:
    #         d[u[i]].append(s[i])
    #     else:
    #         d[u[i]] = []
    #         d[u[i]].append(s[i])
    # print(d)
    n = inp()
    if n == 1:
        print(1)
    else:
        print(n ** 2 - 1)