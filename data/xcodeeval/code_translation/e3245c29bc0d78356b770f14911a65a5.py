
import functools
import logging
import os
import sys
import time

logger = logging.getLogger()
reader = sys.stdin
is_judge = os.getenv("ONLINE_JUDGE") is not None


def timeit(func):
    @functools.wraps(func)
    def timed(*args, **kwargs):
        if is_judge:
            rv = func(*args, **kwargs)
        else:
            ts = time.time()
            rv = func(*args, **kwargs)
            te = time.time()

            logger.debug("performance %r %2.2fms", func.__name__, (te - ts) * 1000)
        return rv
    return timed

# ----------------------
# -     /SOLUTION      -
# ----------------------


@timeit
def contains_subsequence(arr, seq):
    seq_len = len(seq)

    # Empty sequence
    if seq_len == 0:
        return True

    i = 0
    for item in arr:
        if item == seq[i]:
            i += 1
            if i == seq_len:
                break

    return i == seq_len


@timeit
def main():
    # while line := reader.readline():
    line = reader.readline()
    if contains_subsequence(line, "hello"):
        print("YES")
    else:
        print("NO")


# ----------------------
# -     \SOLUTION      -
# ----------------------


def setup():
    global logger, reader

    if is_judge:
        logger.setLevel(logging.WARNING)
    else:
        # Format logger
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("{asctime}s - {message}", style='{')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        # Stdin from file
        reader = open("input.txt")


if __name__ == '__main__':
    line = input()
    if contains_subsequence(line, "hello"):
        print("YES")
    else:
        print("NO")
    # setup()
    # try:
    #     main()
    # except KeyboardInterrupt:
    #     logger.debug("KeyboardInterrupt")
    # except IOError as e:
    #     logger.error(f"I/O error({e.errno}): {e.strerror}")
