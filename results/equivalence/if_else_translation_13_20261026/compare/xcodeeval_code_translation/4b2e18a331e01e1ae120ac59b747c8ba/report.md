# xcodeeval_code_translation/4b2e18a331e01e1ae120ac59b747c8ba

- item: xcodeeval_code_translation/4b2e18a331e01e1ae120ac59b747c8ba
- transform: if_else_swap (L4)
- behavior: match
- model: codellama/CodeLlama-7b-hf
- thresholds: {'p67': 0.6813, 'p80_saved': 1.3238}

| 指標 | 変換前 | 変換後 | 差分 |
|---|---|---|---|
| loc | 47 | 47 | +0 |
| total_tokens | 318 | 320 | +2 |
| mean_entropy | 1.153 | 1.159 | +0.006 |
| ppl | 3.410 | 3.557 | +0.147 |
| su_count_p67 | 46 | 47 | +1 |
| su_count_p80_saved | 43 | 43 | +0 |
| lm_cc_p67 | 48.600 | 48.400 | -0.200 |
| lm_cc_p80_saved | 46.000 | 43.400 | -2.600 |

行は元コードの順。`|` = その行の前に SU 境界、maxH = 行内の最大エントロピー。

| 元 | 境界p67 | 境界p80_saved | 変換前 | maxH | 新 | 境界p67 | 境界p80_saved | 変換後 | maxH | region |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | \| | \| | `#n is the base and k is the result, need to find min x s.t. f(x)=k, length is the length of n` | 5.86 | 1 | \| | \| | `#n is the base and k is the result, need to find min x s.t. f(x)=k, length is the length of n` | 5.86 | before |
| 2 | \| | \| | `import math` | 2.39 | 2 | \| | \| | `import math` | 2.39 | before |
| 3 | \| | \| | `def find(n,k,length):` | 4.70 | 3 | \| | \| | `def find(n,k,length):` | 4.70 | before |
| 4 | \| | \| | `    if k<n:` | 3.75 | 4 | \| | \| | `    if not (k<n):` | 3.75 | if_header |
| 5 | \| | \| | `        return [k]` | 2.39 | 23 | \| | \| | `        return [k]` | 1.46 | then_body |
| 6 | \| | \| | `    else:` | 3.32 | 22 | \| | \| | `    else:` | 1.71 | between |
| 7 | \| | \| | `        MAX=0` | 4.27 | 5 | \| | \| | `        MAX=0` | 2.63 | else_body |
| 8 | \| | \| | `        index=1` | 3.60 | 6 | \| | \| | `        index=1` | 2.99 | else_body |
| 9 |  |  |  | 0.15 | 7 |  |  |  | 0.24 | else_body |
| 10 | \| | \| | `        for i in range(1,length+1):` | 2.23 | 8 | \| | \| | `        for i in range(1,length+1):` | 2.15 | else_body |
| 11 | \| | \| | `            temp=k%(10**i)` | 3.37 | 9 | \| | \| | `            temp=k%(10**i)` | 2.86 | else_body |
| 12 | \| | \| | `            if temp>=n:` | 2.07 | 10 | \| | \| | `            if temp>=n:` | 2.42 | else_body |
| 13 | \| | \| | `                break` | 2.38 | 11 | \| | \| | `                break` | 2.11 | else_body |
| 14 | \| | \| | `            else:` | 1.79 | 12 | \| | \| | `            else:` | 1.87 | else_body |
| 15 | \| | \| | `                if temp>=10**(i-1):` | 1.51 | 13 | \| | \| | `                if temp>=10**(i-1):` | 1.55 | else_body |
| 16 | \| | \| | `                    MAX=temp` | 2.11 | 14 | \| | \| | `                    MAX=temp` | 2.07 | else_body |
| 17 |  |  | `                    index=i` | 0.62 | 15 | \| |  | `                    index=i` | 0.69 | else_body |
| 18 | \| | \| |  | 1.71 | 16 | \| | \| |  | 1.72 | else_body |
| 19 | \| | \| | `        res=k-MAX` | 3.86 | 17 | \| | \| | `        res=k-MAX` | 3.47 | else_body |
| 20 | \| | \| | `        #empty+=[MAX]` | 4.59 | 18 | \| | \| | `        #empty+=[MAX]` | 4.62 | else_body |
| 21 | \| | \| | `        res=res//(10**index)` | 3.23 | 19 | \| | \| | `        res=res//(10**index)` | 2.83 | else_body |
| 22 | \| | \| | `        #print(MAX,res,n,k,index)` | 2.65 | 20 | \| | \| | `        #print(MAX,res,n,k,index)` | 2.57 | else_body |
| 23 | \| | \| | `        return find(n,res,length)+[MAX]` | 2.54 | 21 | \| | \| | `        return find(n,res,length)+[MAX]` | 2.21 | else_body |
| 24 | \| | \| |  | 2.37 | 24 | \| | \| |  | 2.49 | after |
| 25 | \| | \| |  | 2.98 | 25 | \| | \| |  | 2.98 | after |
| 26 | \| | \| |  | 2.96 | 26 | \| | \| |  | 2.98 | after |
| 27 | \| | \| |  | 2.85 | 27 | \| | \| |  | 2.86 | after |
| 28 | \| | \| |  | 2.79 | 28 | \| | \| |  | 2.80 | after |
| 29 | \| | \| |  | 2.65 | 29 | \| | \| |  | 2.67 | after |
| 30 | \| | \| | `n=int(input())` | 2.76 | 30 | \| | \| | `n=int(input())` | 2.71 | after |
| 31 | \| |  | `k=int(input())` | 1.21 | 31 | \| |  | `k=int(input())` | 1.18 | after |
| 32 | \| | \| | `length=int(math.log(n-1,10))+1` | 3.12 | 32 | \| | \| | `length=int(math.log(n-1,10))+1` | 3.09 | after |
| 33 | \| | \| | `ANS=find(n,k,length)[::-1]` | 2.95 | 33 | \| | \| | `ANS=find(n,k,length)[::-1]` | 2.99 | after |
| 34 | \| | \| | `ans=0` | 2.39 | 34 | \| | \| | `ans=0` | 2.52 | after |
| 35 | \| | \| | `temp=1` | 1.76 | 35 | \| | \| | `temp=1` | 1.84 | after |
| 36 | \| | \| |  | 1.35 | 36 | \| | \| |  | 1.50 | after |
| 37 | \| |  | `for i in range(len(ANS)):` | 1.04 | 37 | \| |  | `for i in range(len(ANS)):` | 1.11 | after |
| 38 | \| | \| | `    ans+=ANS[i]*temp` | 1.77 | 38 | \| | \| | `    ans+=ANS[i]*temp` | 1.84 | after |
| 39 | \| |  | `    temp*=n` | 0.68 | 39 | \| |  | `    temp*=n` | 0.70 | after |
| 40 | \| | \| | `#print(ANS)    ` | 2.17 | 40 | \| | \| | `#print(ANS)    ` | 2.17 | after |
| 41 | \| | \| | `print(ans)    ` | 1.45 | 41 | \| | \| | `print(ans)    ` | 1.52 | after |
| 42 | \| | \| |  | 2.16 | 42 | \| | \| |  | 2.15 | after |
| 43 | \| | \| |  | 2.14 | 43 | \| | \| |  | 2.13 | after |
| 44 | \| | \| |  | 2.04 | 44 | \| | \| |  | 2.07 | after |
| 45 | \| | \| |  | 1.66 | 45 | \| | \| |  | 1.62 | after |
| 46 | \| | \| |  | 1.39 | 46 | \| | \| |  | 1.34 | after |
| 47 | \| | \| |  | 1.51 | 47 | \| | \| |  | 1.55 | after |
