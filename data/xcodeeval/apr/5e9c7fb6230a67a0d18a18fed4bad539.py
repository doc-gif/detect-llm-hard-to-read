import sys
import collections

infile = sys.stdin.buffer
def gs()  : return infile.readline().rstrip()
def gi()  : return int(gs())
def gss() : return gs().split()
def gis() : return [int(x) for x in gss()]

MOD = 10 ** 9 + 7
INF = 10 ** 12
N = 10 ** 5

def main(infn="") :
    global infile
    infile = open(infn,"r") if infn else open(sys.argv[1],"r") if len(sys.argv) > 1 else sys.stdin
    ######################################################################
    n,m = gis()
    dp = [0 for _ in range(n+1)]
    dp[1] = 1
    h = collections.defaultdict(collections.Counter)
    cumul = 0
    prev = dp[1]
    for u in range(2, len(dp)):
        dp[u] += prev
        dp[u] += dp[1]
        dp[u] %= m
        for k in h[u]:
            cumul += h[u][k] * dp[k]
            cumul %= m
        dp[u] += cumul
        dp[u] %= m
        prev += dp[u]
        prev %= m

        v,c = u<<1, 2
        h[u + 1][1] +=1
        while(v < len(dp)):
            h[v][c]+=1#.append(c)
            h[v][c-1] -=1 #.append(-(c-1))
            v += u
            c += 1
    print (dp[-1])

    ######################################################################
if __name__ == '__main__' :
    main()