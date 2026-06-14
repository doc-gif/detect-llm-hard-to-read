n = input()
b = input()
if len(n) < len(b):
    print("need tree")
elif len(n) > len(b):
    if b in n:
        print("automaton")
    else:
        is_subsequence = False
        unique_b_chars = list(set(b))
        n_index = 0
        b_index = 0
        matched_count = 0
        while matched_count < len(b):
            for i in range(n_index, len(n)):
                if b[b_index] == n[i]:
                    n_index = i + 1
                    b_index += 1
                    matched_count += 1
                    if i == len(n) - 1 and matched_count != len(b):
                        matched_count = len(n)
                    break
                if matched_count == len(b):
                    break
        if matched_count == len(b):
            print("automaton")
        else:
            has_enough_chars = True
            for char in unique_b_chars:
                n_count = n.count(char)
                b_count = b.count(char)
                if n_count >= b_count and b_count != 0:
                    continue
                else:
                    has_enough_chars = False
                    break
            if not has_enough_chars:
                print("need tree")
            else:
                print("both")
elif len(n) == len(b):
    has_enough_chars = True
    unique_b_chars = list(set(b))
    for char in unique_b_chars:
        n_count = n.count(char)
        b_count = b.count(char)
        if n_count >= b_count and b_count != 0:
            continue
        else:
            has_enough_chars = False
            break
    if not has_enough_chars:
        print("need tree")
    else:
        print("array")
