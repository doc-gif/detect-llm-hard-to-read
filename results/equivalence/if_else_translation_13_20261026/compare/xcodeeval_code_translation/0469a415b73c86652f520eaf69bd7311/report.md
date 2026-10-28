# xcodeeval_code_translation/0469a415b73c86652f520eaf69bd7311

- item: xcodeeval_code_translation/0469a415b73c86652f520eaf69bd7311
- transform: if_else_swap (L7)
- behavior: match
- model: codellama/CodeLlama-7b-hf
- thresholds: {'p67': 0.6813, 'p80_saved': 1.3238}

| 指標 | 変換前 | 変換後 | 差分 |
|---|---|---|---|
| loc | 59 | 59 | +0 |
| total_tokens | 438 | 440 | +2 |
| mean_entropy | 0.570 | 0.574 | +0.003 |
| ppl | 1.651 | 1.669 | +0.018 |
| su_count_p67 | 55 | 55 | +0 |
| su_count_p80_saved | 33 | 33 | +0 |
| lm_cc_p67 | 72.800 | 72.800 | +0.000 |
| lm_cc_p80_saved | 39.800 | 40.000 | +0.200 |

行は元コードの順。`|` = その行の前に SU 境界、maxH = 行内の最大エントロピー。

| 元 | 境界p67 | 境界p80_saved | 変換前 | maxH | 新 | 境界p67 | 境界p80_saved | 変換後 | maxH | region |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | \| | \| | `n = int(input())` | 3.54 | 1 | \| | \| | `n = int(input())` | 3.54 | before |
| 2 | \| | \| | `input_string = input()` | 3.54 | 2 | \| | \| | `input_string = input()` | 3.54 | before |
| 3 | \| | \| |  | 3.72 | 3 | \| | \| |  | 3.72 | before |
| 4 | \| | \| | `map = {}` | 5.00 | 4 | \| | \| | `map = {}` | 5.00 | before |
| 5 | \| | \| |  | 2.89 | 5 | \| | \| |  | 2.89 | before |
| 6 | \| | \| | `for i in range(0, len(input_string)):` | 2.48 | 6 | \| | \| | `for i in range(0, len(input_string)):` | 2.48 | before |
| 7 | \| | \| | `    if input_string[i] in map:` | 3.06 | 7 | \| | \| | `    if not (input_string[i] in map):` | 3.06 | if_header |
| 8 | \| |  | `        map[input_string[i]]+=1` | 0.95 | 10 | \| |  | `        map[input_string[i]]+=1` | 1.19 | then_body |
| 9 |  |  | `    else:` | 0.20 | 9 |  |  | `    else:` | 0.32 | between |
| 10 | \| |  | `        map[input_string[i]]=1` | 0.72 | 8 | \| | \| | `        map[input_string[i]]=1` | 1.90 | else_body |
| 11 | \| |  |  | 0.99 | 11 | \| |  |  | 0.94 | after |
| 12 | \| | \| |  | 4.18 | 12 | \| | \| |  | 4.08 | after |
| 13 | \| | \| | `if len(map) == 3:` | 4.08 | 13 | \| | \| | `if len(map) == 3:` | 4.03 | after |
| 14 | \| | \| | `    print("BGR")` | 5.12 | 14 | \| | \| | `    print("BGR")` | 5.08 | after |
| 15 | \| |  |  | 0.98 | 15 | \| |  |  | 1.00 | after |
| 16 | \| |  |  | 1.04 | 16 | \| |  |  | 1.08 | after |
| 17 | \| | \| | `if len(map) == 2:` | 2.10 | 17 | \| | \| | `if len(map) == 2:` | 2.13 | after |
| 18 | \| | \| | `    sum = 0` | 2.92 | 18 | \| | \| | `    sum = 0` | 2.87 | after |
| 19 | \| | \| | `    check = False` | 2.04 | 19 | \| | \| | `    check = False` | 2.06 | after |
| 20 | \| | \| | `    check_key = ""` | 4.72 | 20 | \| | \| | `    check_key = ""` | 4.76 | after |
| 21 | \| | \| | `    other_key = ""` | 1.33 | 21 | \| |  | `    other_key = ""` | 1.23 | after |
| 22 | \| | \| | `    for key in map.keys():` | 1.39 | 22 | \| | \| | `    for key in map.keys():` | 1.38 | after |
| 23 | \| |  | `        sum += map[key]` | 1.06 | 23 | \| |  | `        sum += map[key]` | 1.01 | after |
| 24 |  |  |  | 0.41 | 24 |  |  |  | 0.40 | after |
| 25 | \| | \| | `        if map[key] == 1:` | 1.77 | 25 | \| | \| | `        if map[key] == 1:` | 1.95 | after |
| 26 | \| |  | `            check = True` | 1.00 | 26 | \| |  | `            check = True` | 0.97 | after |
| 27 | \| |  | `            check_key = key` | 0.86 | 27 | \| |  | `            check_key = key` | 0.77 | after |
| 28 | \| |  | `        else:` | 1.28 | 28 | \| |  | `        else:` | 1.24 | after |
| 29 |  |  | `            other_key = key` | 0.52 | 29 |  |  | `            other_key = key` | 0.52 | after |
| 30 | \| |  |  | 0.91 | 30 | \| |  |  | 0.92 | after |
| 31 | \| | \| | `    if sum == 2:` | 1.73 | 31 | \| | \| | `    if sum == 2:` | 1.78 | after |
| 32 | \| | \| | `        if 'G' not in map:` | 1.56 | 32 | \| | \| | `        if 'G' not in map:` | 1.51 | after |
| 33 | \| | \| | `            print("G")` | 2.87 | 33 | \| | \| | `            print("G")` | 2.88 | after |
| 34 | \| |  | `        if 'R' not in map:` | 0.99 | 34 | \| |  | `        if 'R' not in map:` | 0.97 | after |
| 35 |  |  | `            print("R")` | 0.18 | 35 |  |  | `            print("R")` | 0.18 | after |
| 36 | \| |  | `        if 'B' not in map:` | 1.21 | 36 | \| |  | `        if 'B' not in map:` | 1.21 | after |
| 37 |  |  | `            print("B")` | 0.14 | 37 |  |  | `            print("B")` | 0.14 | after |
| 38 | \| | \| | `    else:` | 1.34 | 38 | \| | \| | `    else:` | 1.35 | after |
| 39 | \| |  | `        if check == True:` | 1.21 | 39 | \| |  | `        if check == True:` | 1.28 | after |
| 40 | \| | \| | `            if other_key == "R" and check_key == "G":` | 1.64 | 40 | \| | \| | `            if other_key == "R" and check_key == "G":` | 1.73 | after |
| 41 | \| | \| | `                print("BG")` | 1.78 | 41 | \| | \| | `                print("BG")` | 1.77 | after |
| 42 | \| |  | `            if other_key == "B" and check_key == "G":` | 1.10 | 42 | \| |  | `            if other_key == "B" and check_key == "G":` | 1.09 | after |
| 43 | \| |  | `                print("GR")` | 1.11 | 43 | \| |  | `                print("GR")` | 1.08 | after |
| 44 | \| |  | `            if other_key == "B" and check_key == "R":` | 1.22 | 44 | \| |  | `            if other_key == "B" and check_key == "R":` | 1.21 | after |
| 45 | \| |  | `                print("GR")` | 1.32 | 45 | \| |  | `                print("GR")` | 1.32 | after |
| 46 | \| |  | `            if other_key == "G" and check_key == "R":` | 0.81 | 46 | \| |  | `            if other_key == "G" and check_key == "R":` | 0.81 | after |
| 47 | \| |  | `                print("BR")` | 1.10 | 47 | \| |  | `                print("BR")` | 1.08 | after |
| 48 | \| | \| | `            if other_key == "R" and check_key == "B":` | 1.47 | 48 | \| | \| | `            if other_key == "R" and check_key == "B":` | 1.48 | after |
| 49 | \| | \| | `                print("BG")` | 1.48 | 49 | \| | \| | `                print("BG")` | 1.47 | after |
| 50 | \| | \| | `            if other_key == "G" and check_key == "B":` | 1.48 | 50 | \| | \| | `            if other_key == "G" and check_key == "B":` | 1.48 | after |
| 51 | \| |  | `                print("BR")    ` | 1.27 | 51 | \| |  | `                print("BR")    ` | 1.28 | after |
| 52 | \| | \| | `        else:` | 1.52 | 52 | \| | \| | `        else:` | 1.53 | after |
| 53 | \| | \| | `            print("BGR")` | 3.41 | 53 | \| | \| | `            print("BGR")` | 3.44 | after |
| 54 | \| | \| |  | 1.59 | 54 | \| | \| |  | 1.58 | after |
| 55 | \| | \| | `if len(map) == 1:` | 1.50 | 55 | \| | \| | `if len(map) == 1:` | 1.49 | after |
| 56 | \| | \| | `    for key in map.keys():` | 1.90 | 56 | \| | \| | `    for key in map.keys():` | 1.90 | after |
| 57 | \| |  | `        print(key)` | 1.29 | 57 | \| |  | `        print(key)` | 1.25 | after |
| 58 | \| |  |  | 1.25 | 58 | \| |  |  | 1.26 | after |
| 59 | \| | \| |  | 1.81 | 59 | \| | \| |  | 1.81 | after |
| 60 |  |  |  | - | 60 |  |  |  | - | after |
