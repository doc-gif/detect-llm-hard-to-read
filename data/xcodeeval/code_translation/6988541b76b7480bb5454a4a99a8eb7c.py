from sys import stdin, stdout
from math import ceil

def read_input():
    n = int(stdin.readline())
    m = int(stdin.readline())

    max_on_bench = 0
    sum = 0
    for _ in range(n):
        a = int(stdin.readline())
        if a > max_on_bench:
            max_on_bench = a
        sum += a

    return n, m, max_on_bench, sum

if __name__ == "__main__":
    n, m, max_on_bench, sum = read_input()
    largest = max_on_bench + m
    smallest = max(ceil((sum + m) / n), max_on_bench)
    print('{x} {y}'.format(x=smallest, y=largest))
