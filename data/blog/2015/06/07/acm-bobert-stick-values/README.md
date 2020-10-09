# BOBERT - Stick values

第一次好好壓複雜度，然後把題目AC，紀錄一下XD

[原題連結](http://www.spoj.com/problems/BOBERT/)

## 題目

給一個序列 $a\_0 \dots a\_{N-1}$ ，和 $s$ 個棒子，所有棒子的長度和 = $N$，現在我們要用這些棒子蓋滿序列（棒子長度有多長就可以覆蓋多少數字），每個棒子不能互相覆蓋，不能超出界線，不可多用或少用。

現在定義一個棒子的`好棒棒度`是 $L \times(max(a, b)-min(a, b))$ ， $L$ 是長度，$max(a, b)$ 和 $min(a, b)$ 被定義為棒子覆蓋到的數字們最大值和最小值。

請輸出`好棒棒度總和`的最大值。

## 過程

### 第一次

一開始是想對 $s$ 和 $2^s$ 做dp，類似這樣

$$
	dp[s+1][sts|2^i] = max(dp[s][sts]+len \times query())
$$

然後從 $dp[1]$ 滾上去。

query用線段樹實做。

複雜度： $O(S^22^S \log S)$ 
結果：`TLE`

### 第二次

仔細想想沒有必要對 $s$ dp，因為每層接觸到的狀態都是Disjoint的。所以改用`queue`做。

複雜度：$O(S2^S \log S)$
結果：`TLE`

### 第三次

自己先偷偷比對了一下假如query做到 $O(1)$ 的話， $10^5$ 測資似乎會快個 **4** 倍，所以把query改為`sparse table`。

複雜度：$O(S2^S)$
結果：`TLE`

### 第四次

因為複雜度基本上已經很ok了，所以開始檢查一些常數可能有點炸了的地方，發現我`sparse table`發懶直接用`int64`，改一陣。

絕果：`AC`

## Code

```cpp
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <cmath>
#include <algorithm>
#include <queue>

using namespace std;

typedef long long int int64;

typedef vector<int> VI;
typedef vector<VI> VVI;

const int64 INF = 1000000001;

struct maxspt{
    VVI maxarr;
    maxspt(int n, int64* arr){
        int k = (int)log2((double)n+0.2);
        maxarr = VVI(n, VI(k+1));
        for(int lx = 0;lx < n;lx++) maxarr[lx][0] = arr[lx];
        for(int lx = 1;lx <= k;lx++)
            for(int ly = 0;ly+(1<<(lx-1)) < n;ly++)
                maxarr[ly][lx] = max(maxarr[ly][lx-1], maxarr[ly+(1<<(lx-1))][lx-1]);
        return;
    }
    int query(int a, int b){
        int k = (int)(log2(b-a+1.2));
        return max(maxarr[a][k], maxarr[b-(1<<k)+1][k]);
    }
};

struct minspt{
    VVI minarr;
    minspt(int n, int64* arr){
        int k = (int)log2((double)n+0.2);
        minarr = VVI(n, VI(k+1));
        for(int lx = 0;lx < n;lx++) minarr[lx][0] = arr[lx];
        for(int lx = 1;lx <= k;lx++)
            for(int ly = 0;ly+(1<<(lx-1)) < n;ly++)
                minarr[ly][lx] = min(minarr[ly][lx-1], minarr[ly+(1<<(lx-1))][lx-1]);
        return;
    }
    int query(int a, int b){
        int k = (int)(log2(b-a+1.2));
        return min(minarr[a][k], minarr[b-(1<<k)+1][k]);
    }
};

int64 dp[1<<20] = {0};
bool vis[1<<20] = {0};
int64 stl[30];
int64 arr[100000];


int main(){
    int n, s;
    scanf("%d", &n);
    for(int lx = 0;lx < n;lx++) scanf("%lld", arr+lx);

    maxspt maxtb(n, arr);
    minspt mintb(n, arr);

    scanf("%d", &s);
    for(int lx = 0;lx < s;lx++) scanf("%lld", stl+lx);

    queue<int> que;
    que.push(0);
    while(que.size()){
        int sts = que.front(); que.pop();
        int64 len = 0; for(int lx = 0;lx < s;lx++) if(sts&(1<<lx)) len += stl[lx];
        for(int lx = 0;lx < s;lx++){
            if(sts&(1<<lx)) continue;
            int nsts = sts|(1<<lx);
            if(stl[lx]) dp[nsts] = max(dp[nsts], dp[sts] + ((int64)(maxtb.query(len, len+stl[lx]-1) - mintb.query(len, len+stl[lx]-1)))*stl[lx]);
            else dp[nsts] = max(dp[nsts], dp[sts]);
            if(!vis[nsts]){
                que.push(nsts);
                vis[nsts] = 1;
            }
        }
    }
    printf("%lld\n", dp[(1<<s)-1]);
    return 0;
}

```

## NOTE

前後共花了`2:15` QAQ