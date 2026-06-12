from queue import Queue as Q
n, x = map(int, input().split())
q = Q()
q.put((x, 0))
was = set()
while not q.empty():
    r = q.get()
    if r[0] >= 10**(n-1):
        print(r[1])
        break
    else:
        for i in str(r[0]):
            if i not in [0, 1]:
                new = int(i)*r[0]
                if new not in was:
                    was.add(new)
                    q.put((new, r[1]+1))
else:
    print(-1)
