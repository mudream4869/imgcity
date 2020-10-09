# 因式分解一個有限域的多項式

是在前幾天的代導課，老師上完Berlekamp's Algorithm後，就說把它刻出來就可以加分XD．那就來寫吧，反正這比賽時也刻東西刻習慣了（誒

其實在寫的時候還頗驚訝，之前在看正整數的分解目前尚未有多項式時間的分解法（印象中最目前好的是Number Field Seive?），可是在一個有限域的多項式竟然可以有多項式時間（對於要分解的多項式的degree），有限域也未免太強（條件）了．

總之這裡就不細題Berlekamp's Algorithm細節了，給個Wiki（[Wiki: Berlekamp's Algorithm](http://en.wikipedia.org/wiki/Berlekamp's_algorithm)）

實做起來還真有點麻煩，除了F[x]的代數，還需要計算一個矩陣的Null Space(把一個矩陣當作線性變換後的Null Space)，光是把矩陣弄成 **echelon form** ，就是一些時間的coding+debug．之後再輸出Basis．

後面就是一些 $F[x]$ 的代數操作，把operator寫好，用c++寫也是可以很漂亮的（可是常數可能就要哭泣了）．

獻醜一下，有限域用 $Z_p$ 實做，總覺得Coding Style有點爛掉，看看笑笑就好：
[FactPolyFF.zip](https://drive.google.com/file/d/0B2iNVzqlGaGIbWxRd29Ec1lqWFU/view?usp=sharing)


然後主要的 **Factorization** Code:
`poly` 的 `r` 是最高項次 + 1， `set_r()` 會把 `r` 調整好
`an[lx]` 是系數
`make_monic()` 會把多項式轉（乘上一個數）成首一多項式，並且回傳原本的首項系數．
`除法/` 回傳 `(商，餘數)`
`diff()` 會微分多項式

順便把**Square free**的分解也寫進去了，完整一點．

```cpp
std::vector<std::pair<poly,int> > fact(poly pa){
    // Factorization pa
    // Return : vector<pair<poly,int> >
    std::vector<std::pair<poly,int> > ret;
     
    if(pa.r == 1 and pa.an[0] == 0){
        fprintf(stderr, "Error : Try to fact 0.\n");
        return ret;
    }
    
    int deg = pa.r-1, p = pa.p;
     
    int fst = pa.make_monic();
    
    if(fst != 1){
        poly poly_fst(p); 
        poly_fst.an[0] = fst;
        ret.push_back(std::pair<poly,int>(fst,1));
    }
    
    int gmat[1000] = {0}, nullset[1000] = {0}, nullsetcount;

    for(int lx = 0;lx < deg;lx++){
        poly test(p);
        test.r = lx*p + 1, test.an[lx*p] = 1;
        std::pair<poly,poly> getresid = test/pa;
        for(int ly = 0;ly < getresid.second.r;ly++)
            gmat[ly*deg + lx] = getresid.second.an[ly];
    }
    for(int lx = 0;lx < deg;lx++)
        gmat[lx*deg + lx] = (gmat[lx*deg + lx] + p-1)%p;

    nullsetcount = GetNullSpace(gmat, deg, deg, p, nullset);
    std::vector<poly> prc; prc.push_back(pa);
    for(int lx = 0;lx < nullsetcount;lx++){
        std::vector<poly> tmp;
        for(int ly = 0;ly < prc.size();ly++){
            poly hh = prc[ly];
            poly testg(p); testg.r = deg;
            for(int lz = 0;lz < deg;lz++)
                testg.an[lz] = nullset[lx*deg + lz];
            testg.set_r();
            for(int lz = 0;lz < p;lz++){
                testg.an[0] = (testg.an[0] + 1)%p;
                poly getgcd = gcd(hh, testg);
                
                if(getgcd.r > 1){
                    tmp.push_back(getgcd);
                }
            }
        }
        prc = tmp;
    }
         
    for(int lx = 0;lx < prc.size();lx++){
        poly hh = prc[lx];
        poly diff_hh;
        int nn = 1;
        for(;;){
            diff_hh = diff(hh);
            if(not diff_hh.is_zero())
                break;
            for(int lx = 0;lx < hh.r;lx+=p)
                hh.an[lx/p] = hh.an[lx];
            nn *= p;
            hh.r = (hh.r - 1)/p + 1;
        }
        std::pair<poly, poly> get_pair = hh/gcd(hh, diff_hh);         
        ret.push_back(std::pair<poly, int>(get_pair.first, nn*(hh.r-1)/(get_pair.first.r-1)));
    }

    return ret; 
}
```