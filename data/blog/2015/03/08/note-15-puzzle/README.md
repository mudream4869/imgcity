# 15-puzzle

上週的AI課最後提到了8-puzzle，突然想起TIOJ也有一題：[15-puzzle](http://tioj.ck.tp.edu.tw/problems/1573)

基本上8-puzzle和15-puzzle是不同層級的XD，8-puzzle只有 $8! = 40320$ 種狀態，搜一搜就過了，可是15-puzzle若是用bfs，則可能會需要儲存 $15! = 1307674368000$ 種狀態。

第一次寫這種需要漸漸優化的暴搜題 .\_. 來筆記一下

## IDA*

第一個想法是：為了避免儲存過多狀態，需要用**dfs**來模擬**bfs**，逐步增加可遞迴深度。 
不過這會遇到一個問題：要如何判斷無解？假如是用步數來判斷，大概會TLE。

所以到網路上查了一下：還真的有**充要條件**

## Is 15-puzzle Solvable？

給定一個盤面(空格在右下角)，判斷是否有解。

把數字們排成一行，去算他的逆序數對，假如是奇數，那就無解。反之有解。

不過把這加上去後，還是TLE，看來還是得優化。

## 剪枝

### 剪枝一：避免返回狀態

首先一個明顯要剪掉就是回到上一個狀態。
這個剪下去好很多，可是還是不夠。

### 剪枝二：估計步數下界

可以弄一個步數下界：`func()` 然後判斷當前深度加上步數下界是否超過深度限制。 
步數的估計可以把每個數字要移動的漢明頓距離加總，是個不錯的估計。

## AC Code

```cpp
#include <cstdio>
#include <cstdlib>
#include <algorithm>

using namespace std;

int tb[4][4];
int x, y;

int iabs(int a){
    return max(a, -a);
}

int func(){
    int step_cnt = 0;
    for(int lx = 0;lx < 4;lx++)
        for(int ly = 0;ly < 4;ly++){
            if(tb[lx][ly] == 16) continue;
            int v = tb[lx][ly]-1;
            step_cnt += iabs(v%4 - ly) + iabs(v/4 - lx);
        }
    return step_cnt;
}

bool dfs(int h, int mh, int pre_d){
    if(h == mh){
        for(int lx = 0;lx < 4;lx++)
            for(int ly = 0;ly < 4;ly++)
                if(lx*4 + ly != tb[lx][ly]-1)
                    return false;
        return true;
    }
    if(func() + h > mh)
        return false;
    int dx[4] = {1, 0, 0, -1};
    int dy[4] = {0, 1, -1, 0};
    for(int d = 0;d < 4;d++){
        if(pre_d + d == 3) continue;
        int tx = x, ty = y;
        int nx = x + dx[d], ny = y + dy[d];
        if(nx < 0 or nx > 3 or ny < 0 or ny > 3)
            continue;
        swap(tb[x][y], tb[nx][ny]);
        x = nx, y = ny;
        if(dfs(h+1, mh, d)) return true;
        x = tx, y = ty;
        swap(tb[x][y], tb[nx][ny]);
    }
    return false;
}

int main(){
    for(int lx = 0;lx < 4;lx++)
        for(int ly = 0;ly < 4;ly++){
            scanf("%d", &tb[lx][ly]);
            if(tb[lx][ly] == 0){
                tb[lx][ly] = 16;
                x = lx, y = ly;
            }
        }
    int inv_cnt = 0;
    for(int lx = 0;lx < 16;lx++)
        for(int ly = lx+1;ly < 16;ly++){
            int a = tb[lx%4][lx/4], b = tb[ly%4][ly/4];
            if(a == 16 or b == 16) continue;
            inv_cnt += a > b;
        }
    if(inv_cnt%2 == y%2){
        puts("-1");
        return 0;
    }
    int s = func(); while(!dfs(0, s, -1)) s++;
    printf("%d\n", s);
    return 0;
} 
```