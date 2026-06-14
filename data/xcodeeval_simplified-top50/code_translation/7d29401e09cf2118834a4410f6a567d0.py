n, m = map(int, input().split())
a = list(map(int, input().split()))
import bisect
first_half_size = n // 2
first_half_sums = []
second_half_sums = []
def generate_first_half_sums(idx, current_sum=0):
    if idx == first_half_size:
        first_half_sums.append(current_sum)
    else:
        generate_first_half_sums(idx + 1, (current_sum + a[idx]) % m)
        generate_first_half_sums(idx + 1, current_sum)
def generate_second_half_sums(idx, current_sum=0):
    if idx == n:
        second_half_sums.append(current_sum)
    else:
        generate_second_half_sums(idx + 1, (current_sum + a[idx]) % m)
        generate_second_half_sums(idx + 1, current_sum)
generate_first_half_sums(0)
generate_second_half_sums(first_half_size)
first_half_unique_sorted = sorted(set(first_half_sums))
max_sum = 0
for second_sum in second_half_sums:
    complement_idx = bisect.bisect_left(first_half_unique_sorted, m - second_sum)
    candidate_sum = first_half_unique_sorted[complement_idx - 1] + second_sum
    if max_sum < candidate_sum:
        max_sum = candidate_sum
print(max_sum)