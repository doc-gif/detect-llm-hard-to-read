n, m, i, j, a, b = map(int, input().split())
INF = 10000000000
path1 = path2 = path3 = path4 = INF
temp1 = temp2 = temp3 = temp4 = 0
if (i - 1) % a == 0 and (j - 1) % b == 0:
    path1 = (i - 1) // a
    path_1 = (j - 1) // b
    if (path1 % 2 == 0 and path_1 % 2 == 0) or (path1 % 2 != 0 and path_1 % 2 != 0):
        path1 = max(path1, path_1)
        temp1 = 1
    else:
        path1 = INF
        temp1 = 0
if (i - 1) % a == 0 and (m - j) % b == 0:
    path2 = (i - 1) // a
    path_2 = (m - j) // b
    if (path2 % 2 == 0 and path_2 % 2 == 0) or (path2 % 2 != 0 and path_2 % 2 != 0):
        path2 = max(path2, path_2)
        temp2 = 1
    else:
        path2 = INF
        temp2 = 0
if (n - i) % a == 0 and (j - 1) % b == 0:
    path3 = (n - i) // a
    path_3 = (j - 1) // b
    if (path3 % 2 == 0 and path_3 % 2 == 0) or (path3 % 2 != 0 and path_3 % 2 != 0):
        path3 = max(path3, path_3)
        temp3 = 1
    else:
        path3 = 10000000000000
        temp3 = 0
if (n - i) % a == 0 and (m - j) % b == 0:
    path4 = (n - i) // a
    path_4 = (m - j) // b
    if (path4 % 2 == 0 and path_4 % 2 == 0) or (path4 % 2 != 0 and path_4 % 2 != 0):
        path4 = max(path4, path_4)
        temp4 = 1
    else:
        path4 = 1900000000000
        temp4 = 0
mini = min(path1, path2, path3, path4)
if ((i + a > n and i - a < 1) or (j + b > m and j - b < 1)) and mini != 0:
    print("Poor Inna and pony!")
elif temp1 == 0 and temp2 == 0 and temp3 == 0 and temp4 == 0:
    print("Poor Inna and pony!")
else:
    print(int(min(path1, path2, path3, path4)))