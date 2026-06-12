import sys
def solve():
    n, k = map(int, input().split())
    a = [int(i) - 1 for i in input().split()]
    unique_kinds = len(set(a))
    if unique_kinds <= k:
        print(unique_kinds)
        return
    books = [False] * n
    have = 0
    cost = 0
    for i, current_book in enumerate(a):
        if books[current_book]:
            continue
        if have < k:
            books[current_book] = True
            cost += 1
            have += 1
        else:
            to_remove = -1
            farthest_next_use = -1
            for book_id in range(n):
                if books[book_id]:
                    if book_id not in a[i + 1 :]:
                        to_remove = book_id
                        break
                    next_use = a[i + 1 :].index(book_id)
                    if farthest_next_use < next_use:
                        farthest_next_use = next_use
                        to_remove = book_id
            assert to_remove != -1
            books[to_remove] = False
            books[current_book] = True
            cost += 1
    print(cost)
if __name__ == "__main__":
    solve()