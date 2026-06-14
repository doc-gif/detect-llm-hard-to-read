def cost_of_move(state, ss_ind):
    curr_v, curr_k, curr_x = state
    cost = (
        max(0, V[ss_ind - 1] - curr_v)
        + max(0, K[ss_ind - 1] - curr_k)
        + max(0, X[ss_ind - 1] - curr_x)
    )
    return cost
if __name__ == "__main__":
    n = int(input())
    s = input()
    V = [s[:i].count("V") for i in range(n + 1)]
    K = [s[:i].count("K") for i in range(n + 1)]
    X = [i - V[i] - K[i] for i in range(n + 1)]
    n_v, n_k, n_x = V[n], K[n], X[n]
    INF = float("Inf")
    dp = [
        [[[INF for _ in range(2)] for _ in range(n_x + 1)] for _ in range(n_k + 1)]
        for _ in range(n_v + 1)
    ]
    dp[0][0][0][0] = 0
    for v in range(n_v + 1):
        for k in range(n_k + 1):
            for x in range(n_x + 1):
                for vtype in range(2):
                    curr = dp[v][k][x][vtype]
                    if v < n_v:
                        idx = V.index(v + 1)
                        dp[v + 1][k][x][1] = min(
                            dp[v + 1][k][x][1], curr + cost_of_move([v, k, x], idx)
                        )
                    if k < n_k and vtype == 0:
                        idx = K.index(k + 1)
                        dp[v][k + 1][x][0] = min(
                            dp[v][k + 1][x][0], curr + cost_of_move([v, k, x], idx)
                        )
                    if x < n_x:
                        idx = X.index(x + 1)
                        dp[v][k][x + 1][0] = min(
                            dp[v][k][x + 1][0], curr + cost_of_move([v, k, x], idx)
                        )
    print(min(dp[n_v][n_k][n_x]))