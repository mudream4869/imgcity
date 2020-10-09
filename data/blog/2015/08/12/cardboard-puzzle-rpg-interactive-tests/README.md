# 解謎RPG互動方式測試

有點好奇有沒有辦法單單只靠Google Cardboard的Trigger和Gaze做到一定程度的RPG互動。

## 一個想法

大致上先測試了個想法：

* Triggered時，可以和被注視的物品 **對話**
* 假如Triggered時視線是接近水平線，那就切換成走路模式。
* 假如在走路時Trigger，那就停下來。

基本上做到移動和對話就可以完成大部份解謎遊戲可以做到的事，像是拿取物品、和NPC對話...等，選擇要使用的物品可以用Menu做到，`Google Cardboard SDK`有提供和GUI互動。

## 問題與可能解決辦法

測試時發現些問題：

* 磁鐵感應似乎不太靈敏：不知道是不是我用的手機的問題，Trigger有時就是沒辦法觸發
* 移動仍是不方便：嘛，這算是預料之中。可能可以改成偵測 **Press** 事件，不過這就似乎要依賴靈敏的磁力感應了，有在Github上看到[這個](https://github.com/JScott/cardboard-controls/blob/master/CardboardControl/Scripts/ParsedMagnetData.cs)
* 暈眩：弄個鼻子嗎？[Source](http://www.purdue.edu/newsroom/releases/2015/Q1/virtual-nose-may-reduce-simulator-sickness-in-video-games.html)

## 測試品影片

<iframe width="420" height="315" src="https://www.youtube.com/embed/u5iYq3rmOYo" frameborder="0" allowfullscreen></iframe>