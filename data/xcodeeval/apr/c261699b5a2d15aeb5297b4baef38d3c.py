# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""

"""
Solution to coin-exchange problem, in which 2 parameters are given:
    - amount of money
    - array of coin values
"""

def solveCombinations(amount, coins):
    comb = [0] * (amount+1)
    comb[0] = 1
    for c in coins:
        for i, val in enumerate(comb):
            if i >= c:
                comb[i] += comb[i - c]
    return comb[-1]

def solveMinCoins(amount, coins):
    minNum = [amount+1] * (amount+1)
    minNum[0] = 0   # sem moedas para 0 dinheiros
    # print(minNum)
    for i in range(1, amount+1):
        for c in coins:
            if c <= i:
                minNum[i] = min(minNum[i - c] + 1, minNum[i])
                # print(minNum)
            else:
                break
    # print(minNum)
    return minNum[-1]

coin, amount = map(int, input().split())

print(solveMinCoins(amount , range( 1, coin+1 ) ))