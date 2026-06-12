n = int(input())
xs = [int(elm) for elm in input().split(" ")] 

def calc_min_diff(xs):
    if n == 1:
        return 1

    min_cur_diffs = []
    twice_flags = []
    for i in range(n):
        cur_diffs = [abs(xs[j] - xs[i]) for j in range(n) if xs[j] != xs[i] and i != j]
        #print("cur_diffs", cur_diffs)
        #print("xs", xs)
        if len(cur_diffs) == 0:
            #print("out1")
            return 1

        min_cur_diff = min(cur_diffs)
        
        twice_flag = False
        for cur_diff in cur_diffs:
            #if cur_diff % min_cur_diff != 0:
            #print(cur_diff, min_cur_diff)
            if cur_diff == min_cur_diff:
                pass
            elif cur_diff == min_cur_diff * 2:
                twice_flag = True
            else:
                #print("out2")
                return -1
        min_cur_diffs.append(min_cur_diff)
        twice_flags.append(twice_flag)
    
    
    min_diff = min(min_cur_diffs)
    for min_cur_diff, twice_flag in zip(min_cur_diffs, twice_flags):
        if twice_flag:
            if min_cur_diff != min_diff:
                #print("out3")
                return -1
        else:
            if min_cur_diff in [min_diff, min_diff*2]:
                pass
            else:
                #print("out4")
                return -1
    
    if not twice_flag and min_diff % 2 == 0:
        ret = min_diff // 2
    else:
        ret = min_diff
    return ret

out = calc_min_diff(xs)
print(out)