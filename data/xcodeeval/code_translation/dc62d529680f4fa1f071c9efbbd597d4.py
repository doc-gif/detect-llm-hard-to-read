# http://codeforces.com/contest/771/problem/D
"""
DP-solution.

For each state (v, k, x, v_is_last_letter) we trial a step along the v, k and x
axes and check that
dp[future_state] = min(dp[future_state], dp[state] + cost_of_move)
Hence this implicitly reults in the one with least cost.

V, K, X are arrays that contain the number of occurences of v, k, x at the i'th
index of s.
"""


def cost_of_move(state, ss_ind):
    """
    eg. ss = s[0:K.index(k+1)]
    Note: ss includes the i+1'th occurence of letter I. We hence want
    ss = s[0:ss_ind-1]
    And then we cound the number of occurences of V, K, X in this substring.

    However, we don't need ss now - this info is contained in lists V, K, X.
    """

    curr_v, curr_k, curr_x = state
    cost = sum([max(0, V[ss_ind-1] - curr_v), max(0, K[ss_ind-1] - curr_k),
                max(0, X[ss_ind-1] - curr_x)])
    return cost


if __name__ == "__main__":

    n = int(input())
    s = input()

    V = [s[0:i].count('V') for i in range(n+1)]
    K = [s[0:i].count('K') for i in range(n+1)]
    X = [(i - V[i] - K[i]) for i in range(n+1)]

    # Initialising
    n_v, n_k, n_x = V[n], K[n], X[n]

    dp = [[[[float('Inf') for vtype in range(2)] for x in range(n_x+1)]
           for k in range(n_k+1)] for v in range(n_v+1)]
    dp[0][0][0][0] = 0

    for v in range(n_v + 1):
        for k in range(n_k + 1):
            for x in range(n_x + 1):
                for vtype in range(2):
                    orig = dp[v][k][x][vtype]
                    if v < n_v:
                        dp[v+1][k][x][1] = min(dp[v+1][k][x][vtype],
                                               orig + cost_of_move([v, k, x], V.index(v+1)))
                    if k < n_k and vtype == 0:
                        dp[v][k+1][x][0] = min(dp[v][k+1][x][0],
                                               orig + cost_of_move([v, k, x], K.index(k+1)))
                    if x < n_x:
                        dp[v][k][x+1][0] = min(dp[v][k][x+1][0],
                                               orig + cost_of_move([v, k, x], X.index(x+1)))
    print(min(dp[n_v][n_k][n_x]))
