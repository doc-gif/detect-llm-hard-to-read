def lucky(x):
    s = str(x)
    return s.count("4") + s.count("7") == len(s)
def Gen_lucky(n):
    if len(n) == 1:
        if n < "4":
            return 0
        if n < "7":
            return 1
        return 2
    s = str(n)
    if s[0] < "4":
        return 0
    if s[0] == "4":
        return Gen_lucky(s[1:])
    if s[0] < "7":
        return 2 ** (len(s) - 1)
    if s[0] == "7":
        return 2 ** (len(s) - 1) + Gen_lucky(s[1:])
    else:
        return 2 ** len(s)
def Form(X, k):
    if k == 0:
        return X
    for i in range(len(X)):
        if k >= F[len(X) - i - 1]:
            h = k // F[len(X) - i - 1]
            r = k % F[len(X) - i - 1]
            G = list(X[i + 1 :])
            G.remove(X[i + h])
            G = [X[i]] + G
            return Form(X[:i] + [X[i + h]] + G, r)
F = [1]
p = 1
i = 1
while p <= 10**15:
    p *= i
    F.append(p)
    i += 1
n, k = map(int, input().split())
if n <= 14:
    if k > F[n]:
        print(-1)
    else:
        permutation = Form(list(range(1, n + 1)), k - 1)
        count = 0
        for i in range(n):
            if lucky(i + 1) and lucky(permutation[i]):
                count += 1
        print(count)
else:
    permutation = Form(list(range(n - 14, n + 1)), k - 1)
    prefix_str = str(n - 15)
    count = 0
    for i in range(1, len(prefix_str)):
        count += 2**i
    count += Gen_lucky(prefix_str)
    for i in range(n - 14, n + 1):
        if lucky(permutation[i - n + 14]) and lucky(i):
            count += 1
    print(count)