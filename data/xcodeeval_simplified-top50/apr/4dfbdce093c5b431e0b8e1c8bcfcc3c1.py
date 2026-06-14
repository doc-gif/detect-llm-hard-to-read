def DFS(x):
    for i in range(x):
        if Seen[i]:
            continue
        if Rem[i] >= C[x]:
            if Rem[i] == C[x] and len(Children[i]) == 0:
                continue
            Rem[i] -= C[x]
            Parent[x] = i
            Children[i].append(x)
            return True
    for i in range(x):
        if Seen[i]:
            continue
        Y = []
        Seen[i] = True
        for child in Children[i]:
            Parent[child] = -1
            Rem[i] += C[child]
            if DFS(child):
                continue
            Parent[child] = i
            Rem[i] -= C[child]
            Y.append(child)
        Seen[i] = False
        Children[i] = Y
        if Rem[i] >= C[x]:
            if Rem[i] == C[x] and len(Children[i]) == 0:
                continue
            Rem[i] -= C[x]
            Children[i].append(x)
            Parent[x] = i
            return True
    return False


n = int(input())
C = list(map(int, input().split()))
Rem = [-1] * n
Parent = [-1] * n
Children = []
Seen = [False] * n
C.sort(reverse=True)
if C[0] != n or 2 in C:
    print("NO")
else:
    for i in range(n):
        Rem[i] = C[i] - 1
        Children.append([])
    Parent[0] = 0
    Ans = "YES"
    for i in range(1, n):
        if not DFS(i):
            Ans = "NO"
            break
    for i in range(n):
        if Rem[i] != 0 and C[i] != 1:
            Ans = "NO"
            break
    print(Ans)
