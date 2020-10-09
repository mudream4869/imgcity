## 動態存取第k大

動態第k大是個實在是有點麻煩的東西，因為`set`裏面並沒有提供類似的操作，像是`nth_element()`之類的東西．

### 線段樹

假如可以離線處理，這算是一個不錯的選擇，先把資料離散化，然後按照順序排好．

```cpp
#define MAX 100005
int tree[4*MAX];
int base;
void init(int n){
    base = (1<<(int)(ceil(log2(n+2)))) -1;
    for(int lx = 0;lx < 4*MAX;lx++)
        tree[lx] = 0;
    return;
}
void touch(int a){
    int prc = a + base + 2;
    tree[prc]++;
    for(prc>>=1;prc;prc>>=1)
        tree[prc] = tree[prc*2] + tree[prc*2 + 1];
    return;
}
int qry(int a, int b){
    int ret = 0;
    for(a += base + 1, b += base+3;
        a^b^1;a>>=1, b>>=1){
        if(~a&1) ret += tree[a^1];
        if(b&1) ret += tree[b^1];
    }
    return ret;
}
```

如此`qry`函數便可以知道 $[a, b]$ 之間有多少的元素，進而用二分搜實作出`kth_element`

### gnu pbds tree

今天逛codeforce看到[Codeforce:Algorithm Gym :: Data structures](http://codeforces.com/blog/entry/15729)

```cpp
#include<bits/stdc++.h>
#include<ext/pb_ds/assoc_container.hpp>
#include<ext/pb_ds/tree_policy.hpp>
using namespace __gnu_pbds;
using namespace std;
template <typename T>
using ordered_set = tree<T, null_type, less<T>, rb_tree_tag, tree_order_statistics_node_update>;

int main(){
	  ordered_set<int>  s;
	  s.insert(1); 
	  s.insert(3);
	  cout << s.order_of_key(2) << endl; // the number of elements in the s less than 2
	  cout << *s.find_by_order(0) << endl; // print the 0-th smallest number in s(0-based)
    return 0;
}
```