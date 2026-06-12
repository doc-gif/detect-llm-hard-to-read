from math import factorial
a = int(input())
print(factorial(a)//factorial(a-5)//120*a*(a-1)*(a-2)*(a-3)*(a-4))
