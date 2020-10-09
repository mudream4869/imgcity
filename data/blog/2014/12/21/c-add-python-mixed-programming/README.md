# C和Python混和編程

昨天我心血來潮，看看有沒有辦法讓`C`像`Python`一樣把其他Python檔案`Import`進來，並且呼叫使用他們的函數，這不難查，很快就查到大量的範例。可是真的把一些範例寫上去後就碰到一些詭異的事情。

不過標題這麼下，看來還是不能只寫遇到的錯誤，先從頭開始講吧：

## 如何使用

很簡單，只要

```cpp
#include<python.h>
```

Mac是

```cpp
#include<Python/Python.h>
```

Mac編譯時需要多下`-framework Python`參數

然後這是我找到的原始範例：

```cpp
#include <Python/Python.h>
 
int main(){
    Py_Initialize();
    
    PyObject* pModule = PyImport_ImportModule("test2");
    PyObject* pFunc = PyObject_GetAttrString(pModule, "MakeCall");
    //some code
    return 0;
}
```

## 路徑設置

這的de很久，我一直`Runtime Error`在pFunc那行，忍不住去PyObject_Print一下`pModule`，發現他竟然是`<nil>`！！？？連引入都不成功？

查了一下，發現是需要設置路徑

```cpp
PySys_SetPath(".");
```

## 傳遞函數指標

這個找超久，網路上都沒啥範例，只好自己拼拼湊湊出一個啦．

大概是先建立一個`PyMethod`，裏面填寫要傳遞的`Function Pointer`，然後用`BuildValue`做成`Tuple`就好了。

以下是完整範例:)

```python
def MakeCall(func):
    func()
    return 1
```

```cpp
#include <Python/Python.h>
#include <stdio.h>
int counter = 0;
static PyObject* func(PyObject* a, PyObject* b){
    counter += 1;
    printf("%d\n", counter);
    return Py_None;
}
 
int main(){
    Py_Initialize();
    PySys_SetPath(".");
    
    PyObject* pModule = PyImport_ImportModule("test2");
    PyObject* pFunc = PyObject_GetAttrString(pModule, "MakeCall");
 
    PyMethodDef *callback = new PyMethodDef;
    
    callback->ml_name = "func";
    callback->ml_meth = func;
    callback->ml_flags = 1;
    
    PyObject* pcb = PyCFunction_New(callback, NULL);
    PyObject* pArg = Py_BuildValue("(O)", pcb);
    
    PyObject_CallObject(pFunc, pArg);
     
    printf("call ok, counter = %d\n", counter);
    Py_Finalize();
    return 0;
}
```