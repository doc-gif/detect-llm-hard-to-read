def get_line():
    return list(map(int, input().split()))
def calculate_sum(s):
    return s.count("+") - s.count("-")
def calculate_sum_with_unknown(s, unknown_count):
    known_sum = s.count("1") - s.count("0")
    return known_sum - (unknown_count - len(s))
def main():
    send = input()
    recv = input()
    needed_sum = calculate_sum(send)
    received_sum = calculate_sum(recv)
    if "?" not in recv:
        print(1 if needed_sum == received_sum else 0)
        return
    unknown_count = recv.count("?")
    favorable = 0
    for i in range(2**unknown_count):
        current_sum = (
            calculate_sum_with_unknown(bin(i)[2:], unknown_count) + received_sum
        )
        if current_sum == needed_sum:
            favorable += 1
    print(favorable / (2**unknown_count))
main()