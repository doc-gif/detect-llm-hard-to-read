read = lambda: map(int, input().split())
n, v, e = read()
adj = [[] for _ in range(n + 1)]
As = [0] + list(read())
Bs = [0] + list(read())
ans = []

for _ in range(e):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)


def flow(a, b, d):
    As[a] -= d
    As[b] += d
    ans.append((a, b, d));

def augment(path, e, d):
    if e:
        dd = min(d, As[path[e - 1]], v - As[path[e]])
        flow(path[e - 1], path[e], dd)
        augment(path, e - 1, d)
        if d > dd:
            flow(path[e - 1], path[e], d - dd);
    
def adjust(s):
    pre = [0] * (n + 1)
    pre[s] = -1
    stk = [s]
    e = 0
    while len(stk):
        p = stk[-1]
        del stk[-1]
        if As[p] < Bs[p]:
            e = p
            break
        for to in adj[p]:
            if not pre[to]:
                pre[to] = p
                stk.append(to)
        
    if not e:
        raise Exception
    path = []
    while e > 0:
        path.insert(0, e)
        e = pre[e]
    augment(path, len(path) - 1, min(Bs[path[-1]] - As[path[-1]], As[s] - Bs[s])) 

try:
    while True:
        check = False
        for i in range(1, n + 1):
            if As[i] > Bs[i]:
                adjust(i)
                check = True
        if not check: 
            break
    for i in range(1, n + 1):
        if As[i] != Bs[i]:
            raise Exception
    print(len(ans))
    for tp in ans:
        print(*tp)
except Exception:
    print("NO")
