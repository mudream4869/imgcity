# ZKW 線段樹

```
struct BST{
    vector<int> tree;
    int base;
    BST(const vector<int>& arr){
        base = (1<<(int)(ceil(log2((int)arr.size() + 4)))) - 1;
        tree = vector<int>(base*2 + 2, 0);
        for(int lx = 0;lx < arr.size();lx++) tree[base+2+lx] = arr[lx];
        for(int lx = base;lx;lx--) tree[lx] = max(tree[lx*2], tree[lx*2+1]);
        return;
    }
    
    void modify(int p, int val){
        p+=base+2; tree[p] = val;
        for(p>>=1;p;p>>=1)
            tree[p] = max(tree[p*2], tree[p*2+1]);
        return;
    }
 
    int query(int a, int b){
        assert(a <= b);
        int ret = 0;
        for(a+=base+1, b+=base+3;a^b^1;a>>=1, b>>=1){
            if(~a&1) ret = max(ret, tree[a^1]);
            if(b&1) ret = max(ret, tree[b^1]);
        }
        return ret;
    }
};
```
