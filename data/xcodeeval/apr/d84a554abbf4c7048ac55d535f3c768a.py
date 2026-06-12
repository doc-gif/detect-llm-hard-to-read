import math

n    = int(input())

if n == 1:
    print()
else:    
    edge = [list(map(int, input().split())) for _ in range(n-1) ]
    g    = {}

    for x, y in edge:
        if x not in g:
            g[x] = []
        if y not in g:
            g[y] = []
        
        g[x].append(y)
        g[y].append(x)

    def find_center(g): 
        d    = {}
        d[1] = 0
        Q    = [(1, 0)]

        while len(Q) > 0:
            u, dis = Q.pop(0)
    
            for v in g[u]:
                if v not in d:
                    d[v] = dis +1
                    Q.append((v, d[v]))    
        
        max_length = -1
        s = None 

        for u, dis in d.items():
            if dis > max_length:
                max_length = dis
                s = u
      
        d   = {}
        pre = {}
        d[s] = 0
        Q = [(s, 0)]

        while len(Q) > 0:
            u, dis = Q.pop(0)
    
            for v in g[u]:
                if v not in d:
                    pre[v] = u
                    d[v]   = dis +1
                    Q.append((v, d[v]))    
        
        max_length = -1
        e = None 

        for u, dis in d.items():
            if dis > max_length:
                max_length = dis
                e = u
    
        route = [e]
        while pre[route[-1]] != s:
            route.append(pre[route[-1]])
    
        return route[len(route) // 2]

    root = find_center(g)
    p    = {}
    size = {}
    Q    = [root]
    p[root] = -1

    i = 0
    while i < len(Q):
        u = Q[i]
    
        for v in g[u]:
            if p[u] == v: continue
            p[v] = u
            Q.append(v)
        i+=1    
        
    for u in Q[::-1]:
        size[u] = 1
    
        for v in g[u]:
            if p[u] == v:
                continue
            size[u] += size[v]

    gr    = [(u, size[u]) for u in g[root]]
    gr    = sorted(gr, key=lambda x:x[1])
    thres = math.ceil((n-1) / 3) 
    sum_  = 0

    gr1 = []
    gr2 = []
    i = 0
    
    while sum_ < thres:
        gr1.append(gr[i][0])
        sum_ += gr[i][1]
        i+=1
    
    while i < len(gr):
        gr2.append(gr[i][0])
        i+=1
    
    def asign(u, W, ew):
        if size[u] == 1:
            return
    
        cur = 0
        for v in g[u]:
            if v == p[u]: continue
        
            first = W[cur]
            ew.append((u, v, first))
        
            W_  = [x - first for x in W[cur+1: cur+size[v]]]
            asign(v, W_, ew)
        
            cur+=size[v]

    a, b = 0, 0
    for x in gr1:
        a += size[x]
    
    for x in gr2:
        b += size[x]
    
    arr_1 = [x for x in range(1, a+1)] 
    arr_2 = [i*(a+1) for i in range(1, b+1)]    
    ew    = []

    cur = 0
    for u in gr1:
        first = arr_1[cur]
        ew.append((root, u, first))
        W_    = [x - first for x in arr_1[cur+1:cur+size[u]]]
    
        cur += size[u]
        #print(u, W_)
        asign(u, W_, ew)
    
    cur = 0
    for u in gr2:
        first = arr_2[cur]
        ew.append((root, u, first))
        W_    = [x - first for x in arr_2[cur+1:cur+size[u]]]
    
        cur += size[u]
        #print(u, W_)
        asign(u, W_, ew)
   
    for u, v, w in ew:
        print('{} {} {}'.format(u, v, w))