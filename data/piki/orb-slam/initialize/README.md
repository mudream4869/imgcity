# ORBSLAM2 : 初始化

## ORB

先把前一個 Frame 和當前 Frame 的 Matching 找出來。

```
// Find correspondences
ORBmatcher matcher(0.9,true);
int nmatches = matcher.SearchForInitialization(
                   mInitialFrame, mCurrentFrame, mvbPrevMatched, mvIniMatches, 100);
```

`0.9` 是 pyramid 縮放倍數， `true` 是方向。

```
ORBmatcher::ORBmatcher(float nnratio, bool checkOri):
    mfNNratio(nnratio), mbCheckOrientation(checkOri){
}
```

## 兩種模型的可能性

按照場景所抓的 Feature 的不同，可以有不同的模型，平行計算這兩個模型的分數。

* [Homography 模型](/piki/computer-vision/matrix/)
* [Fundemantal 模型](/piki/computer-vision/matrix/)

```
thread threadH(&Initializer::FindHomography, this, ref(vbMatchesInliersH), ref(SH), ref(H));
thread threadF(&Initializer::FindFundamental, this, ref(vbMatchesInliersF), ref(SF), ref(F));
```
