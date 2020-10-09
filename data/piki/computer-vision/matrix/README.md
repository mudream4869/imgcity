# Matrix

幾個重要的 Matrix。

## Camera Matrix

一個相機 (Pinhole) 表示成像的資訊的矩陣。

## Fundemantal Matrix

兩台相機拍攝空間中的點可以找到 $F$ 使以下等式成立：

$x\_1Fx\_2 = 0$

期中 $x\_i$ 是 點在相機(Pinhole camera) 上的投影點。

## Homography Matrix 

兩台相機拍同一平面上的點可以找到 $H$ 使以下等式成立：

$x\_1 = H x\_2$

期中 $x\_i$ 是 點在相機(Pinhole camera) 上的投影點。
