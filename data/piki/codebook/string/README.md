# 字串

## KMP

```
int count(char* p, char* t) {
  int len_p = strlen(p), len_t = strlen(t);
  vector<int> pre(len_p, 0);
  for(int lx = 1;lx < len_p;lx++) {
    pre[lx] = pre[lx-1];
    while(pre[lx] and p[pre[lx]] != p[lx])
      pre[lx] = pre[pre[lx]-1];
    if(p[pre[lx]] == p[lx])
      pre[lx]++;
  }
  int ret = 0;
  for(int tab_p = 0, it_p = 0;tab_p + len_p <= len_t;) {
    if(p[it_p] == t[tab_p + it_p]) {
      it_p++;
      if(it_p == len_p) {
        ret++;
        tab_p += it_p-pre[it_p-1];
        it_p = pre[it_p-1];
      }
    } else {
      tab_p += it_p ? (it_p-pre[it_p-1]):1;
      it_p = it_p ? pre[it_p-1]:0;
    }
  }
  return ret;
}
```
