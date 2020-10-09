# SITCON 2015

去年是有參加過SITCON的Workshop(第三天的golang和第四天的)

今年是第一次參加SITCON年會呢，

~~一大早就爬起來~~睡過頭爬起來，才急忙跑去搭捷運QQ

SITCON在南港展覽館站有安排專車送到人文社會科學館，頗貼心誒XD

一整車都是HACKER，有種莫名的親切感 (X

## 09:10~10:00 Evolution of The Internet 互聯網的演進

第一講就是介紹 **Evolution of The Internet 互聯網的演進** ，真的很適合來開場，從網路從哪裡來，介紹網路的使用演變。第一批Hacker是怎麼在資源甚少的情況下實做出網路。是個很有趣的議題。

## 10:10~11:00 We Hack the World

介紹各種Hacker，記錄一下其中一個頗有趣的Idea:

### 通訊軟體加密問題
		
>  Richard Matthew Stallman：傳三個密文，要得到明文，需要三個密文還原。

以下提供一個可能可行的想法 (?

$\Sigma 密文byte = 明文byte$

這樣安全性基本上可行，因為每個byte對到{0, 1}機率基本上不會太差(偏)

實做上應該可以這樣(假設訊息是`bool msg[len];`，正要加密的`index`是`ptr`)：

*  x $\leftarrow$ RandomShuffle{0, 1, 2}
* 亂數決定前兩個訊息的當前的byte，

```cpp
enc[x[0]][ptr] = rand()%2;  
enc[x[1]][ptr] = rand()%2;
enc[x[2]][ptr] = msg[ptr]^enc[x[0]][ptr]^enc[x[1]][ptr];
//以cpp實做要注意rand()分佈不好，建議用STL裏面提供的其他亂數分佈。
```

如此，三條訊息機率就對稱了。
不過，這似乎還得估計一下明文單字出現在密文裏面的機率

## 11:10~11:50 初探機器學習: 教電腦如何看手勢

Arbiter 大概介紹了一下機器學習，和 **Quadratic Programming**
之前都不太清楚這東西怎麼實現的，今天好像看到了一些輪廓，大概分兩Part

* 硬體部分：
    1. 訊號放大器（用於放大肌肉訊號）
    2. ADC（Analog-to-digital converter）
    
* 軟體部分：
		1. Numpy (FFT)
    2. sclkit-learn
    
主要操作就是先把訊號用FFT轉成各個Frequence的強弱，對應到各個維度，然後用`sclkit-learn`

## 13:00~14:20 座談會：「學生參與校務系統開發」、「校園 Open Data、Open API」

主要是校務系統的part由學生開發的討論，學生開發常常會碰到學校不給資料，因為敏感性之類

`$\Rightarrow$` 學生想辦法自己爬資料，給學校公務人員看，引起注意才有機會。

## 短講們

後來都在R1喏，R3擠滿人OaO

### 14:20~14:30 第一次查課程評價就上手

使用Flask、PTT爬蟲、Elasticsearch做出的課程評價查詢系統

* telnet資料太麻煩 $\Rightarrow$ 使用網頁版PTT爬
* 資料庫單一Table支援多層資料，很方便

### 14:30~14:40 ws育慈 - 東海岸拓荒記：SITCON推廣甘苦談

花蓮sitcon，感覺推廣起來頗辛苦>__>

### 14:50 - 15:00 克莉絲汀 - Project Squirrel臺大開發者社群

[InfoPlat](http://infoplat.me/recruit/)

介紹InfoPlat計劃

### 15:00~15:10 郭峰瑞(Ray) - 亞斯人，程式腦─泛自閉症與程設

### 點心時間

排隊吃點心就沒聽到啦XD

點心真好吃 /OwO/

## 16:20~17:00 Google Code-In 開源，從小開始

一個Google舉辦的一個給14~17歲活動，只是後面有點累了，全睡掉了 >__>

## Lightning talk

一些有趣的輕講＠＠


一天下來，看到好多神奇的東西XD，只是還是不太敢和其他人交流，感覺其他人都好強好耀眼>__>