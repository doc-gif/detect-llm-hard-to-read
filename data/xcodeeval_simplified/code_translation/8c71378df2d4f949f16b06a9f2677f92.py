memo = {}
n = int(input())
cards = input().split()
def cards_match(card1, card2):
    return card1[0] == card2[0] or card1[1] == card2[1]
def dfs(index, top1, top2, top3):
    state = (index, top1, top2, top3)
    if state in memo:
        return memo[state]
    if index < 0:
        result = cards_match(top1, top2) and cards_match(top1, top3)
    else:
        result = False
        if cards_match(top1, cards[index]):
            result = result or dfs(index - 1, top2, top3, top1)
        if cards_match(top1, top2):
            result = result or dfs(index - 1, top1, top3, cards[index])
    memo[state] = result
    return result
def can_clear():
    if n == 1:
        return True
    if n == 2:
        return cards_match(cards[1], cards[0])
    return dfs(n - 4, cards[-1], cards[-2], cards[-3])
print("YES" if can_clear() else "NO")