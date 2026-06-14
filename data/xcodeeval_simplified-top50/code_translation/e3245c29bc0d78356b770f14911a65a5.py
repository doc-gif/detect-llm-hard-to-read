import functools
import logging
import os
import sys
import time
logger = logging.getLogger()
reader = sys.stdin
is_judge = os.getenv("ONLINE_JUDGE") is not None
def timeit(func):
    def timed(*args, **kwargs):
        if is_judge:
            return func(*args, **kwargs)
        ts = time.time()
        rv = func(*args, **kwargs)
        te = time.time()
        logger.debug("performance %r %2.2fms", func.__name__, (te - ts) * 1000)
        return rv
    return timed
def contains_subsequence(arr, seq):
    seq_len = len(seq)
    if seq_len == 0:
        return True
    i = 0
    for item in arr:
        if item == seq[i]:
            i += 1
            if i == seq_len:
                break
    return i == seq_len
def main():
    line = reader.readline()
    if contains_subsequence(line, "hello"):
        print("YES")
    else:
        print("NO")
def setup():
    global logger, reader
    if is_judge:
        logger.setLevel(logging.WARNING)
    else:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("{asctime}s - {message}", style="{")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        reader = open("input.txt")
if __name__ == "__main__":
    line = input()
    if contains_subsequence(line, "hello"):
        print("YES")
    else:
        print("NO")