def solve(n):
    return "Mahmoud" if n % 2 == 0 else "Ehab"
def driver():
    n = int(input())
    print(solve(n))
if __name__ == "__main__":
    driver()