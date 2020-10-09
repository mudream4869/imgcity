# 2017 Google Code Jam

兩年前參加過，但在 Round1 就被刷掉了，今年用 Python 喇Round1 題目竟然過了，可惜 Round2 還是沒過。

## Qualification 

只把 A small-big, B small-big, C small 做完

### A : Oversized Pancake Flipper

給一串01序列和正整數$K$，每次操作只能翻動連續$K$個bit，問最少幾部有辦法把01序列都變成1，不可能則輸出`IMPOSSIBLE`。

思路：因為在同個地方連續翻動等如沒有翻動，所以從頭到尾一個一個翻，看有沒有辦法把`0`變成`1`。

複雜度： $O(LK)$(直接做) 或 $O(L \log L)$ (線段樹維護) 或 $O(L)$ (Queue)

```
#include <cstdlib>
#include <cstdio>

using namespace std;

int main(){
    int k; scanf("%d", &k);
    for(int case_num = 1; case_num <= k;case_num++){
        char str[2000]; int k;
        int b[2000];
        int len;
        scanf("%s %d", str, &k);
        for(len = 0;str[len];len++)
            b[len] = (str[len] == '-');
        
        int step = 0;
        for(int i = 0;i + k-1 < len;i++){
            if(b[i]){
                step++;
                for(int lx = i;lx < i+k;lx++)
                    b[lx] ^= 1;
            }
        }

        bool unsolve = false;
        for(int lx = 0;lx < len and not unsolve;lx++)
            unsolve = b[lx];
    
        printf("Case #%d: ", case_num);
        if(unsolve)
            puts("IMPOSSIBLE");
        else
            printf("%d\n", step);
    }
    return 0;
}

```

### B : Tidy Numbers

給定$N$，找到最大的正整數$K$使得$K \leq N$，並且K的位數數字按位數遞減。

思路：對 $a_n \times 10^k$ 用數位dp的方式想就好了。


```
def solve(n, ptr, und, pre = 0):

    if ptr == 0:
        for i in range(9, und-1, -1):
            if i > n:
                continue
            return pre*10 + i
        return -1

    for i in range(9, und-1, -1):
        if i * 10**ptr > n:
            continue
        ans = solve(n - i*10**ptr, ptr-1, i)
        if ans != -1:
            return pre * 10**(ptr+1) + i * 10**ptr + ans

    return -1


k = int(input())

for case_num in range(1, k+1):
    str_n = input()
    n = int(str_n)
    
    ans = solve(n, len(str_n) - 1, 0)

    print("Case #%d: %d" % (case_num, ans))

```

### C : Bathroom Stalls

有一堆長度為正整數的線段，每次操作會拿出其中最長的線段，並且剪成兩半。其中一段的長度會是 $\left[ \frac{L-1}{2}\right]$，$L$ 是原本線段的長度。

思路：維護 「長度對應到數量 的 map」 即可。

code for small : 

```
#include <cstdio>
#include <cstdlib>
#include <queue>

using namespace std;

int main(){
    
    int k; scanf("%d", &k);

    for(int case_num = 1;case_num <= k;case_num++){

        priority_queue<int> prc;
        
        int n, k; scanf("%d %d", &n, &k);

        prc.push(n);

        for(int lx = 1;lx < k;lx++){
            int t = prc.top()-1;
            prc.pop();
            prc.push(t/2);
            prc.push(t-t/2);
        }

        int t = prc.top()-1;
        printf("Case #%d: %d %d\n", case_num, t-t/2, t/2);
    }

    return 0;
}

```

## Round1 C

### A : Ample Syrup

給定 $(R_i, H_i)$ ，如何取出其中$K$個並且排序，使得

$$ R\_{s\_1} \geq R\_{s\_2} \geq R\_{s\_3} \dots \geq R\_{s\_k} $$
 
並且

$$ \pi R\_{s\_1}^2 + \sum 2 \pi R\_{s\_i}H\_{s\_i} $$

最大。

思路：枚舉「第一個$(R, H)$」，其餘按照 $R_iH_i$ 排序取前$K-1$大

```
import math

T = int(input())

for t in range(1, T+1):
    n, k = map(int, input().split())
    arr = []
    for i in range(n):
        r, h = map(int, input().split())
        arr.append((r, h))

    ans = 0
    for i in range(n):
        R, H = arr[i]
        varr = [p[0]*p[1] for j, p in enumerate(arr) if p[0] <= R and j != i]
        varr = sorted(varr, reverse=True)[:k-1]
        ans = max(ans, R**2 + 2*R*H + 2*sum(varr))

    print("Case #%d:" % t, ans*math.pi)
```

### B : Parenting Partnering

排程，2個人在一些不同的時段有事，要設法讓2個人每天有12小時被排到，並且時段不被重疊。

思路：把所有區間（有事的時段、沒事的時段）分一分，用 Greedy 就可以了。

```
T = int(input())

for t in range(1, T+1):
    ac, aj = map(int, input().split())
    
    ac_list = sorted([(tuple(map(int, input().split())), 0) for _ in range(ac)])
    aj_list = sorted([(tuple(map(int, input().split())), 1) for _ in range(aj)])
    sum_c = sum(map(lambda x : x[0][1]-x[0][0], ac_list))
    sum_j = sum(map(lambda x : x[0][1]-x[0][0], aj_list))

    all_list = sorted(ac_list + aj_list)
    in_c, in_j, outer = [], [], []
    n = len(all_list)
    for i in range(n):
        if i < n-1:
            cur = all_list[i]
            nex = all_list[i+1]
            dif = nex[0][0]-cur[0][1]
        else:
            cur = all_list[n-1]
            nex = all_list[0]
            dif = nex[0][0]-cur[0][1]+1440
        if cur[1] != nex[1]:
            outer.append(dif)
        else:
            if cur[1] == 0:
                in_c.append(dif)
            else:
                in_j.append(dif)

    ans = len(outer)
    if sum(in_c) + sum_c > 720 or sum_j + sum(in_j) >  720:
        arr, ss = None, 0
        if sum(in_c) + sum_c > 720:
            arr = in_c
            ss = sum_c
        else:
            arr = in_j
            ss = sum_j

        arr.sort(reverse=True)
        val = sum(arr)
        for v in arr:
            ans += 2
            val -= v
            if val + ss <= 720:
                break

    print("Case #%d: %d" %(t, ans))

```

### C : Core Training

Small Data 1 題目 (15/43)：給 $p_1 \dots p_n$, $r$, 使得

1. $\sum a_i = r$
2. $\prod (p_i + a_i)$ 越大越好

思路：因為 $\prod x_i$ 的最大值發生在 $x_1 = \dots = x_n$，所以要盡量抬高 $\min{(p_i + a_i)}$

```
T = int(input())

for t in range(1, T+1):
    n, k = map(int, input().split())
    u = float(input())
    ps = list(map(float, input().split()))

    ps.sort(reverse=True)
    
    acc_p = 1

    for i, p in enumerate(ps):
        if sum(ps[i:])+u >= (n-i)*p:
            acc_p *= ((sum(ps[i:])+u)/(n-i))**(n-i)
            break
        else:
            acc_p *= p

    print("Case #%d:" % t, min(acc_p, 1.0))
```

## Round2 : Distributed Round 1 2017 

因為當時是在星期六晚上，而我正要為隔天的事做準備，所以參加了 Distribute 版的。

畢竟第一次參加，解了一題，也算是個收穫？只是今年又沒拿到 T-shirt 了 😢 。

### pA

給一個數列，數 $a\_i > a\_{i-1}$ 的個數。

思路沒有，就按照編號切。

資料傳輸的部分還在看，這裡 Google 有為各種架構提供範例 Code 。

```
#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include "pancakes.h"
#include "message.h"

using std::min;

typedef long long int int64;

int main(){
    int nc = NumberOfNodes();
    int nid = MyNodeId();
    int64 sz = GetStackSize(); 
    int64 lsz = (sz+nc-2)/(nc-1);

    if(nid == 0){
        int64 ans = 1;
        for(int i = 1;i < nc;i++){
            int64 num = 0;
            int source = Receive(-1);
            for(int j = 0;j < 9;j++){
                char c = GetChar(source);
                num = num*10 + (c-'0');
            }
            ans += num;
        }
        printf("%lld\n", ans);
    }else{
        int64 st = (nid-1)*lsz, ed = min(nid*lsz, sz);
        int64 ret = 0;
        char ch[10];;
        for(int64 i = st;i < ed-1;i++)
            ret += GetStackItem(i) > GetStackItem(i+1);
        if(ed < sz)
            ret += GetStackItem(ed-1) > GetStackItem(ed);

        sprintf(ch, "%09lld", ret);
        for(int i = 0;i < 9;i++)
            PutChar(0, ch[i]);
        Send(0);
    }

    return 0;
}

```