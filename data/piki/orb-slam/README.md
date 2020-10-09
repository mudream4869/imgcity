# ORB-SLAM

Realtime SLAM.

[Project Page](http://webdiis.unizar.es/~raulmur/orbslam/)

## 安裝執行

使用：

* Virtualbox 虛擬機 
* [Yuyou/ORB\_SLAM2](https://github.com/yuyou/ORB_SLAM2)

環境準備：

* 把 Yuyou/docker 底下的兩個 Dockerfile 翻一翻，就可以知道怎麼安裝了。

## 簡介

一個 Feature-base、Realtime、Monocular並且不需要GPU的SLAM。
ORB是指 ORB Feature，由 FAST 和 BREIF 的改版所組合(Oriented FAST and Rotated BRIEF)。

### 重要概念

* Covisibility Graph, Essential Graph
* Bags of Words Place Recognition

### 區塊

* [初始化](/piki/orb-slam/initialize/)：從無到有，按照抓取的特徵，用 [Homography 模型](/piki/computer-vision/matrix/)或 [Fundemantal 模型](/piki/computer-vision/matrix/)去做 Bundle Adjustment。
* [追蹤](/piki/orb-slam/track/)
* 優化
* 回環檢測

## 半稠密(Semi Dense)重建

這部分官方還只有論文，還沒有釋出的Code，不過可以參考一個 Fork 的 repo : 
[HeYijia/ORB\_SLAM2](https://github.com/HeYijia/ORB_SLAM2)

待補。 

## 參考資料

* [ORBSLAM2]
* [ORB]
* [ORB SLAM中几个重要概念， 翻译自ORBSLAM作者主论文](http://blog.csdn.net/fang_liu_yang/article/details/53488765)
