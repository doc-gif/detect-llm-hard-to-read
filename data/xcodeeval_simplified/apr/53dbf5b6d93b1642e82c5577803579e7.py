n = int(input())
lookup = {}
for i in range(n):
    row = list(map(int, input().split()))
    for j in range(n):
        lookup[row[j]] = (i, j)
best_rook = [0, 0]
best_bishop = [0, 0]
best_knight = [0, 0]
for i in range(1, n**2):
    x_diff = abs(lookup[i][0] - lookup[i + 1][0])
    y_diff = abs(lookup[i][1] - lookup[i + 1][1])
    if x_diff == 0 or y_diff == 0:
        best_rook[0] += 1
    else:
        best_rook[0] += 2
    if x_diff == y_diff:
        best_bishop[0] += 1
    elif (x_diff - y_diff) % 2 == 0:
        best_bishop[0] += 2
    else:
        best_bishop[0] += 1000
    if {x_diff, y_diff} == {1, 2}:
        best_knight[0] += 1
    elif x_diff**2 + y_diff**2 in [4, 16, 20, 10, 18]:
        best_knight[0] += 2
    elif (
        x_diff**2 + y_diff**2 == 2
        and lookup[i] not in [(0, 0), (n - 1, 0), (0, n - 1), (n - 1, n - 1)]
        and lookup[i + 1] not in [(0, 0), (n - 1, 0), (0, n - 1), (n - 1, n - 1)]
    ):
        best_knight[0] += 2
    elif {x_diff, y_diff} in [
        {5, 0},
        {3, 0},
        {1, 0},
        {6, 1},
        {4, 1},
        {5, 2},
        {3, 2},
        {6, 3},
        {4, 3},
        {5, 4},
    ]:
        best_knight[0] += 3
    else:
        best_knight[0] += 1000
    best_rook[0] = min(best_rook[0], best_bishop[0] + 1, best_knight[0] + 1)
    best_bishop[0] = min(best_rook[0] + 1, best_bishop[0], best_knight[0] + 1)
    best_knight[0] = min(best_rook[0] + 1, best_bishop[0] + 1, best_knight[0])
best_values = (best_rook[0], best_bishop[0], best_knight[0])
if min(best_values) == best_values[0]:
    print(best_rook[0], best_rook[1])
elif min(best_values) == best_values[1]:
    print(best_bishop[0], best_bishop[1])
else:
    print(best_knight[0], best_knight[1])
