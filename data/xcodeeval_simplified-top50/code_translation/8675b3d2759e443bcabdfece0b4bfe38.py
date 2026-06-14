import itertools
import sys
def read_line():
    return sys.stdin.readline().strip()
def read_numbers():
    return list(map(int, read_line().split()))
def read_n_lines(n):
    return [int(read_line()) for _ in range(n)]
def can_form_expression(permutations):
    for a, b, c, d in permutations:
        if a + b == c + d or a == b + c + d:
            return True
    return False
if __name__ == "__main__":
    numbers = read_numbers()
    permutations = itertools.permutations(numbers)
    print("YES" if can_form_expression(permutations) else "NO")