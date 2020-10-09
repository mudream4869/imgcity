# 區間相異元素個數

最近又看了一些東西，決定來整理一下。

首先是完整的問題定義：

給一個數列和一堆區間查詢，每次要回答區間內有多少相異元素個數。

## 離線處理

最一開始的作法（也算是最容易實作，但能憑空想出真的是天才）是莫式算法。

### 莫式算法（Mo's algorithm）

莫式算法是用來對付不具區間加法性質的問題。

首先我們考慮一個問題的化減：假如我們知道 $[l, r]$ 的結果，我們有沒有辦法$O(1)$或 $O(lgN)$ 知道 $[l, r+1]$ （或 $[l+1, r]$ 、$[l-1,r]$、$[l, r-1]$）

這是可以達成的，我們只需要維護一個陣列，然後好好維護**值對應到個數**，就可以了。

所以假如我們要從 $[l\_1, r\_1]$  推到 $[l\_2, r\_2]$，我們只需要 $O(|l\_1-l\_2|+|r\_1-r\_2|)$ ，即兩點的曼哈頓距離。所以現在我們要先解決一個問題：給定平面上一堆點，我們要按照什麼順序拜訪他們，讓曼哈頓距離總和**不錯小**。

第一個想法是：因為拜訪是一條線，所以這問題的下界就是平面上的生成樹，可以證明是$O(N\sqrt N)$，那要做這些點的生成樹嘛？不，這太可怕了([ref1](http://wyfcyx.logdown.com/posts/231702-summary-planar-manhattan-distance-minimum-spanning-tree-is-o-nlogn-algorithm))，事實上，有個簡易可行的方法可以達到$O(N\sqrt N)$：

按照 $[\frac{左界}{\sqrt{N}}]$ , $右界$ 排序後的順序拜訪，即可獲得$O(N\sqrt{N})$的複雜度，雖然不會是最小，但只差常數級別。

### 線段樹

主要想法是從原本的區間和線段樹來的：我們希望在區間出現第二個相同的數時，那個位置是$0$。
所以把查詢區間按照左界排好，當我們要從查詢$[l, ?]$到$[l+1, ?]時，我們去把和$l$相同數字的下一個位置從$0$更新成$1$

舉例：

數列: 5 1 4 1 2

要查詢 $[1, ?]$類時

線段樹: 1 1 1 0 1

要查詢 $[2, ?]$類時

線段樹: 1 1 1 0 1

要查詢 $[3, ?]$類時

線段樹: 1 1 1 1 1

複雜度會是 $O(N\log{N})$

這裏推薦一個題目：[SPOJ DQUERY](http://www.spoj.com/problems/DQUERY/en/)

## 在線處理

### 持久化線段樹

可以發現離線處理的線段樹前後只差1個位置的變化，所以可以把他升級成持久化線段樹。

```cpp
#include <cstdio>
#include <cstdlib>
#include <algorithm>
#include <vector>
#include <map>
#include <set>

using namespace std;

struct node{
    int l, r, val;
    node *ln, *rn;
    node(int _l, int _r, int _v = 0, node* _ln = nullptr, node* _rn = nullptr){
        val = _v, l = _l, r = _r;
        ln = _ln, rn = _rn;
        return;
    }
    ~node(){
        if(ln != nullptr) delete ln;
        if(rn != nullptr) delete rn;
        return;
    }
    void Update(){
        val = 0;
        if(ln != nullptr) val += ln->val;
        if(rn != nullptr) val += rn->val;
        return;
    }
};

node* Cp(node* a){return new node(a->l, a->r, a->val, a->ln, a->rn);}

node* Build(int l, int r){
    if(l == r) return new node(l, r);
    int md = (l+r)>>1;
    return new node(l, r, 0, Build(l, md), Build(md+1, r));
}

void Update(node* nd, int p, int v){
    if(nd->l == nd->r and nd->l == p){nd->val = v; return;}
    int md = (nd->l+nd->r)>>1;
    if(p<=md) Update(nd->ln, p, v);
    else Update(nd->rn, p, v);
    nd->Update();
    return;
}

node* CUpdate(node* nd, int p, int v){
    nd = Cp(nd);
    if(nd->l == nd->r and nd->l == p){nd->val = v; return nd;}
    int md = (nd->l+nd->r)>>1;
    if(p<=md) nd->ln = CUpdate(nd->ln, p, v);
    else nd->rn = CUpdate(nd->rn, p, v);
    nd->Update();
    return nd;
}

int Query(node* nd, int l, int r){
    int ret = 0;
    if(nd->l == l and nd->r == r) return nd->val;
    int md = (nd->l+nd->r)>>1;
    if(r<=md) return Query(nd->ln, l, r);
    else if(l <= md) return Query(nd->ln, l, md) + Query(nd->rn, md+1, r);
    else return Query(nd->rn, l, r);
}

void Print(node* nd){
    if(nd->l == nd->r){ printf("%d ", nd->val); return; }
    Print(nd->ln);
    Print(nd->rn);
    return;
}

int arr[30000];
int nxt[30000];
node* nd[30000];

int main(){
    int n; scanf("%d", &n);
    for(int lx = 0;lx < n;lx++) scanf("%d", arr+lx);
    map<int,int> poi, ptr;
    for(int lx = 0;lx < n;lx++) nxt[lx] = n;
    for(int lx = 0;lx < n;lx++){
        if(ptr.count(arr[lx]))
            nxt[ptr[arr[lx]]] = lx;
        ptr[arr[lx]] = lx;
        if(poi.count(arr[lx]) == 0)
            poi[arr[lx]] = poi.size();
        arr[lx] = poi[arr[lx]];
    }
    nd[0] = Build(0, n-1);
    bool vis[30000] = {0};
    for(int lx = 0;lx < n;lx++){
        if(vis[arr[lx]]) continue;
        vis[arr[lx]] = 1;
        Update(nd[0], lx, 1);
    }
    for(int lx = 1;lx < n;lx++){
        if(nxt[lx-1] == n) nd[lx] = nd[lx-1];
        else nd[lx] = CUpdate(nd[lx-1], nxt[lx-1], 1);
    }

#ifdef DEBUG
    for(int lx = 0;lx < n;lx++){
        Print(nd[lx]);
        puts("");
    }
#endif

    int q; scanf("%d", &q);
    while(q--){
        int a, b; scanf("%d %d", &a, &b);
        a--, b--;
        printf("%d\n", Query(nd[a], a, b));
    }

    return 0;
}

```

## 總結

| 算法        | 可在線 |複雜度| 量  |
|------------|-------|-----|-----|
| 莫式        | 否    |$O(N\sqrt{N})$| 少  |
| 線段樹      | 否    |$O(N\log{N})$| 中  |
| 持久化線段樹 | 是    |$O(N\log{N})$| 中  |

## 參考資料

* ref1 : [【总结】平面manhattan距离最小生成树的O(nlogn)算法 by wyfcyx](http://wyfcyx.logdown.com/posts/231702-summary-planar-manhattan-distance-minimum-spanning-tree-is-o-nlogn-algorithm)