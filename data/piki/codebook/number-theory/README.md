# 數論

## 質數

### 質數表

```
const int MAX = 1000000;
vector<bool> isprime(MAX, true);
vector<int> primes;
isprime[0] = false;
isprime[1] = false;
for(int lx = 2;lx < MAX;lx++) {
  if(isprime[lx]) {
    primes.push_back(lx);
    for(int ly = 2;ly*lx < MAX;ly++) {
      isprime[ly*lx] = false;
    }
  }
}
```
