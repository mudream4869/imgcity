# Count on Totient Function

到這麼多COT題目，也來跟風(X

## 問題

給你一個n( $n < 10^{10}$ )，問是否存在 $x$ 使得 $\phi(x)=n$ 。題目會有多筆詢問。

## 題解

以下 $d(n)$ 表n的因數個數。

首先可以把 $\phi(x)$ 展開

$$
\phi(x) = p_1^{\alpha_1-1}p_2^{\alpha_2-1}...p_r^{\alpha_r-1}(p_1-1)(p_2-1)...(p_r-1)
$$

假如有解，那麼必然存在

$$
(p_1-1)(p_2-1)...(p_r-1) | n
$$


我們可以試著去枚舉 $(p_1-1)(p_2-1)...(p_r-1)$ 。
可以觀察到 $(p_i-1)|n$ ，所以可以先從 $n$ 的因數下手：

1. 因數分解 
2. **BFS**遍歷

所以我們可以得到一個集合：

$$
A = \{ d \ | \ d|n \ , d+1 \in Prime \ \}
$$

可以順便注意到 $|A| \leq d(n)$ ，這可以保證時空複雜度

然後再由A生成一個集合

$$
B = \{ a_1a_2..a_k \ | \ k \in \mathbb{N} \ , a_i \in A \  , \ a_1a_2..a_k|n \ \}
$$

同樣的， $|B| \leq d(n)$ 。

接下來就對 $B$ 裡面的元素做枚舉 $b \in B$ ，
去檢查 $\frac{n}{b}$ 的因數分解。
假如把 $\frac{n}{b}$ 分解後得到 $q_1^{\beta_1}q_2^{\beta_2}...$ 
並且 $b=(q_1-1)(q_2-1)...$ ，那麼還原 $n=q_1^{\beta_1}q_2^{\beta_2}...(q_1-1)(q_2-1)...$ 就是一解

```c++
#include<cstdio>
#include<cstdlib>
#include<set>
#include<map>
#include<vector>
using namespace std;
typedef long long int int64;
typedef set<int64>::iterator siit;
bool seive[100001] = {0};
vector<int64> primes;
bool isprime(int64 a){
	if(a < 100000) return seive[a] == false;
	for(int64 lx = 2;lx*lx <= a;lx++)
		if(a%lx == 0)
			return false;
	return true;
}
vector<pair<int64,int> > getdrc(int64 inp){
	vector<pair<int64,int> > ret;
	for(int lx = 0;lx < primes.size() and primes[lx] <= inp; lx++){
		int ecnt = 0;
		while(inp%primes[lx] == 0)
			inp /= primes[lx], ecnt++;
		if(ecnt)
			ret.push_back(pair<int64,int>(primes[lx], ecnt));
	}
	if(inp > 1)
		ret.push_back(pair<int64,int>(inp,1));
	return ret;
}
set<int64> getdivs(int64 inp){
	set<int64> divs;
	vector<pair<int64,int> > drc = getdrc(inp);
	divs.insert(1);
	for(int lx = 0;lx < drc.size();lx++){
		set<int64> si;
		int64 drc0 = drc[lx].first;
		int drc1 = drc[lx].second;
		for(siit it = divs.begin(); it != divs.end(); it++){
			int64 ee = 1;
			for(int64 xx = 0; xx <= drc1; xx++, ee *= drc0)
				si.insert((*it)*ee);
		}
		divs.clear();
		for(siit it = si.begin(); it != si.end(); it++)
			divs.insert(*it);
	}
	return divs;
}

int main(){
	int64 inp;
	seive[1] = true;
	for(int lx = 2;lx < 100000;lx++){
		if(seive[lx] == false){
			primes.push_back((int64)lx);
			for(int ly = 2;ly*lx < 100000;ly++)
				seive[lx*ly] = true;
		}
	}
	while(1){
		scanf("%lld", &inp);
		if(inp == 0) break;
		set<int64> divs = getdivs(inp);	
		//printf("divisores: ");
		/*for(siit it = divs.begin(); it != divs.end(); it++)
			printf("%lld ", *it);
		printf("\n");*/

		vector<int64> Aset;
		for(siit it = divs.begin(); it != divs.end(); it++)
			if(isprime((*it)+1))
				Aset.push_back(*it);

		/*printf("Aset: ");
		for(int lx = 0;lx < Aset.size(); lx++){
			printf("%lld ", Aset[lx]);
		}
		printf("\n");*/
		set<int64> Tset; Tset.insert(1);
		for(int lx = 0;lx < Aset.size();lx++){
			set<int64> TTset;
			for(siit it = Tset.begin(); it != Tset.end();it++){
				TTset.insert(*it);
				if(inp%((*it)*Aset[lx]) == 0)
					TTset.insert((*it)*Aset[lx]);
			}
			Tset.clear(); Tset.insert(1);
			for(siit it = TTset.begin(); it != TTset.end(); it++)
				Tset.insert(*it);
		}
		/*printf("Tset: ");
		for(siit it = Tset.begin(); it != Tset.end(); it++)
			printf("%lld ", *it);
		printf("\n");*/
		// N/T part
		bool ok = false;
		int64 N = inp;
		for(siit it = Tset.begin();it != Tset.end() and not ok; it++){
			int64 T = *it;
			//printf("prc on %lld\n", *it);
			// assert T | N
			vector<pair<int64,int> > ddrc = getdrc(N/T);
			//printf("N/T = %lld, drc size = %d\n", N/T, (int) ddrc.size());
			int64 mut = 1;
			for(int lx = 0;lx < ddrc.size();lx++){
				mut *= (ddrc[lx].first-1);
			}

			if(T%mut != 0)
				continue;
			
			T /= mut;
			// Check is T = phi(square free) or not
			// if q in ddrc, then p-1 should not divide T now.
			set<int64> inddrc;
			for(int lx = 0;lx < ddrc.size();lx++)
				inddrc.insert(ddrc[lx].first);

			set<int64> gen; gen.insert(1);
			for(int lx = 0;lx < Aset.size();lx++){
				if(inddrc.count(Aset[lx]+1))
					continue;
				set<int64> tmp;
				for(siit it = gen.begin(); it != gen.end(); it++){
					tmp.insert(*it);
					if(T%((*it)*Aset[lx]) == 0)
						tmp.insert((*it)*Aset[lx]);
				}
				gen.clear(); gen.insert(1);
				for(siit it = tmp.begin(); it != tmp.end(); it++)
					gen.insert(*it);
			}
			if(gen.count(T))
				ok = true;
		}
		puts(ok ? "Yes":"No");
	}
	return 0;
}
```

**BFS code**頗長，不過其實有**DFS**做法(而且超短，不需要建立A集合和B集合)。