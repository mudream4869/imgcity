# Codeforce 542 D. Superhero's Job

頗好玩的一題。

給定 $ 1 \leq n \leq 10^{12}$ ，求 $J(x) = n$ 的解的個數，其中

$$ 
x = p_1^{\alpha_1}p_2^{\alpha_2} \dots
$$

$$
J(x) = (1 + p_1^{\alpha_1})(1 + p_2^{\alpha_2}) \dots
$$

時限: `2000ms`

主要就是枚舉出**合理**的因數，然後dfs或dp，因為是要求解的個數，所以用dp統計。

## 解法

### 合理的因數： 必須是 $p^\alpha+1$ ，其中 $p$ 是質數。
	
這就直接開 $O(\sqrt d \log d)$ 反正最差也是本身是質數。
  
### dp

用這方式： $dp[prime][divisor]$ ，這裡面的 $prime \in P$ 就是出現在合理因數裡的質數，一個嚴謹的定義是：

$$
	P = \{p \ | \ p^a = n \ for \ some \ a \in \mathbb{N} \} 
$$

狀態轉移就會是：

$$
	dp[next \ prime][divisor \times prime^a] += dp[prime][divisor] \ if \ prime^a \ | \ n
$$

## 實作

其實在code時快爆炸了，原本寫dfs，最大的測資一直刷不過(`3???ms`)，看了Tutorial才知道要用dp統計QQ

Code:

```cpp
#include <cstdio>
#include <cstdlib>
#include <algorithm>
#include <vector>
#include <set>
#include <map>

using namespace std;

typedef long long int int64;

typedef pair<int64, int64> pii;

int ans = 0;

vector<int64> primes;
bool seive[1000001] = {1};

vector<int64> get_div(int64 inp){
    set<int64> _ret;
    for(int64 lx = 1;lx*lx <= inp;lx++)
        if(inp%lx == 0)
            _ret.insert(lx), _ret.insert(inp/lx);
    
    vector<int64> ret;
    for(auto& it : _ret)
        ret.push_back(it);
    
    return ret;
}

typedef pair<int64,int> pi64i;

pi64i check(int64 inp){
    for(int lx = 0;lx < primes.size() and primes[lx]*primes[lx] <= inp;lx++){
        int64 p = primes[lx]; int c = 0;
        if(inp%p == 0){
            while(inp%p == 0) inp/=p, c++;
            return inp == 1 ? pi64i(p,c) : pi64i(1, 0);
        }
    }
    return pi64i(inp, 1);
}

int main(){
    int64 inp; scanf("%lld", &inp);
    for(int lx = 2;lx <= 1000000;lx++)
        if(seive[lx] == 0){
            primes.push_back(lx);
            for(int ly = 2;ly*lx <= 1000000;ly++)
                seive[ly*lx] = 1;
        }
    
    
    auto divs_tmp = get_div(inp);
    map<int64,int> _pset;
    for(int64 val: divs_tmp){
        auto get_pc = check(val-1);
        if(val > 2 and get_pc.first >= 2){
            _pset[get_pc.first] = max(_pset[get_pc.first], get_pc.second);
        }
    }
    
    map<int64,int> dp[2];
    int now = 0; dp[0][inp] = 1;
    for(auto it = _pset.begin(); it != _pset.end(); it++){
        auto& pc = *it;
        int64 pp = pc.first;
        dp[now^1] = dp[now];
        for(int cc = 1; cc <= pc.second; cc++, pp*=pc.first){
            for(auto it = dp[now].begin();it != dp[now].end(); it++){
                if(it->first%(pp+1) == 0){
                    dp[now^1][it->first/(pp+1)] += it->second; 
                }
            }
        }
        now^=1;
    }
    printf("%d\n", dp[now][1]);
    return 0;
}

```