# 我的第一個Online Judge

是這樣的，在開學期間左右，培訓班的助教要我們每隊生出三題，
生完題目後照理應該是OK了，可是我覺得還沒有，因為我突然想要開始寫Online Judge XDD
不過當時倒是還沒有去實踐，因為如何製作Online Judge，對我來說完全沒有概念

於是，我去翻了一些資料，像是

## Sqlite3

因為是第一個Online Judge，所以打算只先實驗性的用他來當作資料庫
這是之前試的: Sqlite in C

## 執行安全性

這是最重要的一塊，前端的server其次，judge端的安全性最為重要，
因為別人會丟他們自己的code，在系統裡執行。

這一部分我是去翻這: 
[Online Judge 是如何解决判题端安全性问题的？](http://www.zhihu.com/question/23067497)

這裡面大概有些不錯的方法，像是沙盒之類。

## 其他OJ

- [TIOJ](https://github.com/joshua5201/tioj)
- [pzread的judge](https://github.com/pzread/judge)

大概看了一些OJ的實作後，便開始著手寫judge端了!!
光是流程就有點多:
(以下步驟基本上沒有考慮到效率，基本上目標是功能性。)

1. 從資料庫讀取尚未處理的Submit的第一筆(其實這會讓Judge表現的像Stack)
2. 把程式碼和測試資料(只有in)拷貝到測試區域
3. `fork` 執行程式，parent用while做限時功能
4. 比對 test.out 和 正確的out
5. 將結果寫回資料庫

然後前端是用`python`的`tornado`寫，輸入資料基本上只擋長度，SQL指令用參數式，基本上不會有SQL Injection問題。

這只能說是把流程寫好，但最重要的judge端安全還沒寫

所以去找了幾個Sandbox，然後發現這應該頗好操作

## EasySandbox

- [EasySandbox](https://github.com/daveho/EasySandbox)
- [SECCOMP as a Sandboxing Solution ?](http://justanothergeek.chdir.org/2010/03/seccomp-as-sandboxing-solution/)

主要用`prctl` + `LD_PRELOAD`做成

1. 只有辦法做`read`, `write`, `sigreturn`, `_exit` Syscall
2. 有實作`malloc`和`free`

看了一下他的Code，一開始的輸出

```
<<entering SECCOMP mode>>
```

似乎無法避免，不過這不成問題

要讓程式在Sandbox裡跑，基本上只要寫

```c
char* argv[] = {"./t123.out", (char*)0};
char* envs[] = {"LD_PRELOAD=./EasySandbox.so", (char*)0};
execve("./t123.out", argv, envs);
```

加個`chroot`就頗ok惹

## Compiler TLE

```c
#include"/dev/random"
```

需要對編譯器做限時，要不然就等著Judge呵呵吧XD

把這些完成後，就是:

[Unsafe Online Judge](https://bitbucket.org/mudream/usoj)

這大概只能算是第一階段。