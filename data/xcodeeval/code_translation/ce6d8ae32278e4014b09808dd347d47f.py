def main(args):
    n=int(input())
    a=1
    for i in range(n):
        a+=i*4
    print(a)

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))