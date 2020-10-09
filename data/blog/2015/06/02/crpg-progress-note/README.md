# CRPG 進度筆記

CRPG基本上進入收尾，除了加一些新功能，還弄了一些有助於Debug的小工具，之後便會focus在建立**大型測試**上，可以順便把必要支援的事件功能追加上去。

## Alpha版Document

目前應該算是Alpha版吧，目前在Gitbook上準備中，一邊編寫，一邊設計的更方便。

[Document](https://www.gitbook.com/book/mudream4869/crpg-alpha-document/details)

## 主要檔案結構

我調整了一下檔案結構，以利之後開發測試。

```
+ crpg
|-+ src
  |- main.cpp
  |- ...
|-+ testdata
  |-+ 測試資料1
  |-+ 測試資料2
|-+ unittest
  |- ...
```

如此引擎Code就可以和測試資料分離。

## 資源類 Enhencement

### 中文字

[Freeyype中文字](http://mudream.logdown.com/posts/257996/in-opengl-rendering-of-text)

其實是有個Libray，只是覺得有點大有點沒必要，所以自己刻一個，總之，這也OK了。

### 讀取OGG

用`libvorbis`達成。

[Code On Github](https://github.com/mudream4869/crpg/blob/master/src/audioloader/audioloader.cpp)

基本上就是用`libvorbis`讀進來，然後把buffer扔進`OpenAL`

## 功能類 Enhencement

### 自動追蹤主角

這功能大概滿常用的，不過這需要在`Event`裡面增加一個屬性：**觸發頻率**。

## 其他類

### 除錯命名空間

特別幫除錯訊息開了一個命名空間，以利之後整理有意義的除錯訊息

```cpp
namespace Debugger{
    void Init();
    void Print(const char*, ... );
    void Print(std::string);
    void Print(PyObject*);
    void PrintPyErr();
    void CheckPyObject(PyObject*, const char*, ... );
};
```

### 開始邊寫說明

目前大致把格式制定為

```cpp
/** 
 *  @brief: 功能描述
 *  @param: 參數描述
 *  @return: 回傳值描述 
 */
```