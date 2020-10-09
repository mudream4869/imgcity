# 一行的Python3

因為某些原因，最近開始喜歡上**一行Python解問題**了！

## A+B problem

事情的開端就是這題，一開始我突然想到，直接用一行就好了

```python
print(int(input()) + int(input()))
```

由於input順序不需考量，所以上面這樣是好的，然後就突發奇想想把題目都盡量壓在一行內解決。像是給3個數字，然後由大印到小也是很輕鬆。

```python
print([int(input()), int(input()), int(input())].sorted(reversed = True))
```

不過，我很快的就遇到一個小難題：

> 給三個數字，判斷是否有按照由小到大

這比較麻煩的地方是

* 元素輸入順序需要是正確的
* 需要重複用到輸入的陣列（命名）

第一個想了一下，事實上不是什麼問題，只需要用`map(int, map(input, [""]*3))`
就可以做到了，主要是第二個，需要把取到的陣列存起來，然後做下面的比較

```python
if x[0] < x[1] < x[2] :
```

假如只是if的話那還好，我們可以寫

```python
["No", "Yes"][x[0] < x[1] < x[2]]
```

也就是說，我們需要暫時幫輸入字串取名字

## lambda

之後，我想起`python`裡面的Lambda可以做到，用lambda讓輸入陣列暫時有名稱

```python
print((lambda x : ["No", "Yes"][x[0] < x[1] < x[2]])(...))
```

這讓我爽殺題殺了一陣子，可是當我遇到一個問題時卻又卡住了

## 3n+1 Problem

3n+1問題需要用到`while`迴圈

```python
step = 0
while n > 1:
    if n&1 : n >>= 1
    else : n = 3*n + 1
    step += 1
```

改成遞迴後，我們面臨到：我們需要幫遞迴函數取名字

```python
f = lambda x : f([x>>1, 3*n+1][x&1]) + 1 if x > 1 else 0
print(f(int(input())))
```

可是，這就需要用到兩行了！

## Y combinator

我們可以把`f = lambda x : ...f...`改成
`lambda f : lambda x : ... f ...`

所以現在問題是給一個g，求g的不動點(g(x) = x，要把x挖出來)，在網路上翻了一下，發現Y combinator可以做到！

[Y combinator](https://rosettacode.org/wiki/Y_combinator#Python)

所以可以直接這樣寫：

```python
print(((lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args))))(lambda f : lambda x : f([x>>1, 3*n+1][x&1]) + 1 if x > 1 else 0))(int(input()))
```