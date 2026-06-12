# bsdk idhar kya dekhne ko aaya hai, khud kr!!!
# import math
# from itertools import *
# import random
# import calendar
# import datetime
# import webbrowser

n = int(input())
arr = list(map(int, input().split()))
while max(arr) > min(arr):
    index = arr.index(max(arr))
    arr[index] -= min(arr)
print(sum(arr))
