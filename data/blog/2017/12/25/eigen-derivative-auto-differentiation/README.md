# eigen-derivative : 偏微分工具

## 簡介

這大概是為了期末專題弄出來的，由於本來要實作的 Interior Point Method (以下簡稱 IPM ) 需要不少微分的部分，假如傳進去的函數參數本身可以做微分，那麼 IPM 函數介面可以做的很漂亮。

### Interior Point Method 是甚麼？

我們時常可以碰到在某些條件下，需要最佳化的問題，簡單寫可以寫作：

$ \min_{x\in R^n} f(x) $

$ g_i(x) \geq 0 \ \forall \ i \in [1, m]$

IPM 是 使用了 barrier function 和高斯牛頓法來找到局部最佳解。由於本篇重點並非是 IPM ，所以便不在這裡深入。

之後若有關於 IPM 的解說，會放在**文件區**。

### 自動微分用在上面的好處？

假如沒有自動微分，那需要實作

* $f$, $\nabla f$, $\mathbf{H}(f)$
* $G$, $\nabla G$, $\mathbf{H}(G)$ 

後，傳 function pointer 進去。$\mathbf{H}$ 是 Hessian Matrix，需要二次微分。 

假如有實作自動微分，那就可以包裝成只有f, G 這兩個函數。

## eigen-derivative

不多說，先上 [Github Repo](https://github.com/mudream4869/eigen-derivative)

計算向量基於 Eigen。

### 微分方式

使用 Forward accumulation 方法。

### 編譯、引用

函數宣告在 Derivative.h ，實作 Derivative.cpp，典型的實作宣告分割。

### Helloworld

裡面相關的函數和類別都定義在 Eigen namespace 底下。直接上一個簡單的案例。

$f(x, y) = x^2 + xy + y^2$，求 $\frac{\partial f}{\partial x}(1, 2)$

```
Eigen::Derivative x = Derivative::Variable(0),  //第0個變數
                  y = Derivative::Variable(1);  //第1個變數

auto f = x*x + x*y + y*y; //運算子重載

// 計算 df/dx (1, 2) 的值
Eigen::VectorXd vec(2); 
vec << 1, 2;
std::cout << f.diffPartial(0)(vec) << std::endl;
```

### Example

在 repo 底下，有幾個用到微分的[範例](https://github.com/mudream4869/eigen-derivative/tree/master/examples)，像是高斯牛頓法，LM法，還有我實作的IPM。最後 IPM 可以包裝成這樣：

舉的例子是：$\min x+y \ , \ x^2 + y^2 \geq 1 \ , \ x \geq 0 \ , \ y \geq 0$

```
using Eigen::Derivative;
using Eigen::VectorXd;
Derivative par_x = Derivative::Variable(0),
           par_y = Derivative::Variable(1);
Derivative obj_f = par_x + par_y;

Derivative con_h1 = par_x*par_x + par_y*par_y - 1,
           con_h2 = par_x,
           con_h3 = par_y;

// IPM 需要一個不錯的初始值，不過可以不符合條件（g）。
VectorXd x(2);
x << 1, 1;
std::cout << "x initial as " << x.transpose() << std::endl;
std::cout << Derivative_IPM(obj_f, {con_h1, con_h2, con_h3}, x).transpose() << std::endl;
```

### 之後

之後可能會把一些 Reduce 的演算法寫進去、$f : R^n \rightarrow R^m$。