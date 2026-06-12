n = int(input())
query = list(map(int, input().split()))
grades = [0, 0, 0, 0]
def solution(grades, n):
    for x in query:
        grades[x - 2] += 1
    ave = (grades[0] * 2 + grades[1] * 3 + grades[2] * 4 + grades[3] * 5) / n
    if ave >= 4.5:
        return 0
    temp = (grades[0] * 3) / n + ave
    if temp >= 4.5:
        return int((4.5 - ave) * n / 3 + 0.99)
    tempn = temp + (grades[1] * 2) / n
    if tempn >= 4.5:
        return grades[0] + int((4.5 - temp) * n / 2 + 0.99)
    return grades[1] + grades[0] + int((4.5 - tempn) * n + 0.99)
print(solution(grades, n))