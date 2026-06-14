def get_power(data, exponent):
    low = 0
    high = data
    while low <= high:
        mid = (low + high) // 2
        power_value = mid**exponent
        if power_value < data:
            low = mid + 1
        elif power_value == data:
            return mid
        else:
            high = mid - 1
    return low - 1
def process_case():
    data = int(input())
    square_root = get_power(data, 2)
    cube_root = get_power(data, 3)
    sixth_root = get_power(data, 6)
    result = square_root + cube_root - sixth_root
    print(result)
def main():
    n = int(input())
    for _ in range(n):
        process_case()
if __name__ == "__main__":
    main()