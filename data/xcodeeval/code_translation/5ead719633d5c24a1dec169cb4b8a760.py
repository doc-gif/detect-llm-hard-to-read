import sys

def get_square_literal_map():
    literal_map = {}
    for i in range(1, 44722):
        literal = str(i * i)
        literal_len = len(literal)
        if literal_len not in literal_map:
            literal_map[literal_len] = set()
        literal_map[literal_len].add(literal)
    return literal_map

def is_subsequence(x, y):
    it = iter(y)
    return all(any(c == ch for c in it) for ch in x)

def get(n):
    literal_map = get_square_literal_map()
    n_len = len(n)
    for i in range(n_len, 0, -1):
        for j in literal_map[i]:
            if is_subsequence(j, n):
                return n_len - i
    return -1

def main():
    n = sys.stdin.readline().strip()
    print(get(n))

if __name__ == '__main__':
    sys.exit(main())