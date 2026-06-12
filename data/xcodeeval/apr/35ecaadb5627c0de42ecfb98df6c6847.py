input = raw_input
n, m = map(int, input().split(" "))

if n >= 2 and m >= 2:
    c = [2 for i in range(n+1)]
    t = [2 for i in range(n+1)]
    y = [2 for i in range(n+1)]
    #t = c.copy()
    #y = c.copy()
    #c[2] = 2
    #t[2] = 2
    #y[2] = 2

    #T = [[0 for i in range(m+1)] for i in range(n+1)]
    T2 = [2 for i in range(n+1)]
    for i in range(3, n+1):
        c[i] = c[i-1] + y[i-1]
        #t[i] = t[i-1]
        y[i] = c[i-1]

        #C[i][2] = 2
        #T[i][2] = c[i] + y[i] - 2
        T2[i] = c[i] + y[i] - 2
        #Y[i][2] = t[i] = 2

        
    #C = [[2 for i in range(m+1)] for i in range(n+1)]
    Cn = [2 for i in range(m+1)]
    #Tn2 = T[n][2] = T2[n]
    #T = [[Tn2 for i in range(m+1)] for i in range(n+1) ]
    Tn = [T2[n] for i in range(m+1)]
    #Y = C.copy()
    #Yn = Cn.copy()
    Yn = [2 for i in range(m+1)]
    #T[2][2] = c[2] + y[2] - 2
    #Y[2][2] = t[2]


    for j in range(3, m+1):
        #if n == 2 and j == 3:
        #    Cn[j] = Yn[j-1] + Cn[j-1]
        #    Yn[j] =  Yn[j-1] + Cn[j-1]

        #else:
        if True:
            #C[n][j] = C[n][2] = 2
            #Cn[j] = Cn[2] = 2
            #T[n][j] = T[n][2]
            #Tn[j] = Tn[2]
            #Y[n][j] =  Y[n][j-1] + C[n][j-1]
            Cn[j] = Yn[j-1] + Cn[j-1]
            Yn[j] = Cn[j-1]
            #print(Yn[j])

    #out = C[n][m] + Y[n][m] + T[n][m]

    #for j in range(m+1):
    #    print(j, Cn[j], Tn[j], Yn[j])

    out = Cn[m] + Yn[m] + Tn[m]

elif n == 1 and m == 1:
    out = 2
else:
    n = max(n, m)
    b1 = [0 for i in range(n+1)]
    b2 = [0 for i in range(n+1)]
    w1 = [0 for i in range(n+1)]
    w2 = [0 for i in range(n+1)]
    #b2 = b1.copy()
    #w1 = b1.copy()
    #w2 = b1.copy()
    b1[1] = 1
    w1[1] = 1

    for i in range(2, n+1):
        b1[i] = w1[i-1] + w2[i-1]
        b2[i] = b1[i-1]
        w1[i] = b1[i-1] + b2[i-1]
        w2[i] = w1[i-1]
    out = b1[n] + b2[n] + w1[n] + w2[n]

print(out)