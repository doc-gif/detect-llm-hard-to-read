import logging
import sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
def solve(first_line, input_lines):
    m = 0
    x = first_line[1]
    for i in range(len(input_lines) - 1):
        s = input_lines[i] - input_lines[i + 1] - x
        if s > m:
            m = s
    return m
def main():
    first_line = list(map(int, input().split()))
    line = list(map(int, input().split()))
    print(solve(first_line, line))
def log(*message):
    logging.debug(message)
if __name__ == "__main__":
    main()