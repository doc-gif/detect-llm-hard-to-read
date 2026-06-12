import logging
import copy
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

#def solve(firstLine):
def solve(firstLine, inputLines):
    m = 0
    x = firstLine[1]

    for i in range(len(inputLines)-1):
        s = inputLines[i] - inputLines[i+1] - x

        if s > m:
            m = s
    return m

def main():
    firstLine = input().split()
    firstLine = list(map(int, firstLine))
    line = input().split()
    line = list(map(int, line))
        
    print(solve(firstLine, line))

def log(*message):
    logging.debug(message)
    
if __name__ == "__main__":
    main()
