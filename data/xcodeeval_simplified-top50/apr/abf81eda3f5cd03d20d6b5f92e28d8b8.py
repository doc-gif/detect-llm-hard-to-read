input_str = input()


def can_match(pattern, target):
    if len(pattern) != len(target):
        return False
    if "X" in target:
        for digit in range(10):
            if can_match(pattern, target.replace("X", str(digit))):
                return True
        return False
    for i in range(len(pattern)):
        if pattern[i] == target[i] or target[i] == "_":
            continue
        else:
            return False
    return True


if len(input_str) <= 4:
    x = 0
    answer = 0
    while len(str(x)) <= len(input_str):
        if can_match(str(x), input_str):
            answer += 1
        x += 25
    print(answer)
    exit(0)


def count_prefix(prefix):
    if prefix[0] == "0":
        return 0
    answer = 1
    if prefix[0] == "_":
        answer = 9
    for i in range(1, len(prefix)):
        if prefix[i] == "_":
            answer *= 10
    return answer


def count_suffix(suffix):
    answer = 0
    for ending in ["00", "25", "50"]:
        if can_match(ending, suffix):
            answer += 1
    return answer


def count_matches(template):
    if "X" in template:
        answer = 0
        for digit in range(10):
            answer += count_matches(template.replace("X", str(digit)))
        return answer
    if input_str[0] == "0":
        return 0
    prefix = template[0 : len(template) - 2]
    suffix = template[len(template) - 2 : len(template)]
    return count_prefix(prefix) * count_suffix(suffix)


print(count_matches(input_str))
