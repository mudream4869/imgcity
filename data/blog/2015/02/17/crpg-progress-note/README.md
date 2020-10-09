# CRPG 進度筆記

最近弄了很多東西進去，寫一寫當作備忘好了。之後大概要調整架構＋新增功能＋弄一些小的測試用遊戲。

大致有幾個重要的更新：

## 跨 Windows 和 Mac OX

這就是刻crpg主要原因之一，終於處理好了！

### OpenGL, OpenAL, Python API

主要問題大概是：

* 編譯參數
* 引用標頭檔
* 編譯用環境

在Mac OX底下，編譯和引用這三個就跟喝一杯開水一樣簡單，可是在Windows底下光是安裝`Glut`就超麻煩，還好，有人寫了一個類似Linux的終端機的：[MSYS2](http://msys2.github.io)用`pacman`指令就可以把需要的Package安裝好。需要注意的是，`MSYS2`底下分兩種`g++`編譯器，一個是`usr\bin\g++`，這是給`MSYS2`自己用的，可以用

```c++
#include<cstdio>
int main(){
#ifdef _WIN32
    printf("win32\n");
#endif
    return 0;
}
```

測試，會發現並沒有出現`win32`。另外一個需要用pacman安裝`mingw-w64-g++`(可能更長)，這編譯出來才會是給Windows用的。

安裝的對應關鍵字：

* Glut -> freeglut
* OpenAL -> openal
* Python API -> python

可以這樣找

```bash
$ pacman -Sl | grep keyword
```

然後安裝

```bash
$ pacman -S package_name
```

## 讀取目錄下的檔案

當初沒有寫這個，本來是要使用者自己把清單寫在一個目錄底下的檔案，仔細想想不太合理，就決定要把這部分處理好。原本是想直接用[Boost:File System](http://www.boost.org/doc/libs/1_57_0/libs/filesystem/doc/index.htm)，但想到只是要實做羅列檔案，就用一個大Library，cost好像有點高。所以決定自己弄一個：

```c++
// For GetFileUnderDir header
#ifdef __APPLE__
#include <sys/types.h>
#include <dirent.h>
#elif __WIN32
#include <windows.h>
#endif
// ------
std::vector<std::string> GetFileUnderDir(const char* dir_name){
    std::vector<std::string> ret;

#ifdef __APPLE__
    DIR* dp = opendir(dir_name);
    struct dirent* ep; 
    if(dp != NULL){
        while((ep = readdir(dp))){
            if(strcmp(ep->d_name, ".") == 0 or
               strcmp(ep->d_name, "..") == 0) continue;
            ret.push_back(std::string(ep->d_name));
        }
        closedir(dp);
    }else{
        fprintf(stderr, "Couldn't open the directory\n");
        exit(1);
    }
#elif __WIN32
    
    WIN32_FIND_DATA data;
    HANDLE hFind;
    char d_dir_name[100];
    sprintf(d_dir_name, "%s/*", dir_name);
    hFind = FindFirstFile(d_dir_name, &data);
    if (hFind == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "Couldn't open the directory\n");
        exit(1);
    } 
    else{
        do{
            if(strcmp(data.cFileName, ".") == 0 or 
               strcmp(data.cFileName, "..") == 0) continue;
            ret.push_back(std::string(data.cFileName));
        }while(FindNextFile(hFind, &data));
        FindClose(hFind);
    }
#endif
    return ret;
}
```

## 紅線問題

在圖片邊緣會有模糊的紅線，發現是在讀取Image時，設定Texture處裡部分不好。
**class Image** 在讀取Tile時要把`GL_TEXTURE_MIN_FILTER`, `GL_TEXTURE_MAX_FILTER` 設成 `GL_NEAREST`即可。

## Env過於神通廣大

這是初期在處理公共變數的餘毒，有這種東西，有點不科學：

```c++ Env
struct StrCompare{
    bool operator() (const char* str1, const char* str2) const{
        return std::strcmp(str1, str2) < 0;
    }
};
typedef std::map<const char*, void* , StrCompare> Env;
```

一個 `map: string -> void*`裏面包有太多髒東西。

大致把一部份`instance`放在`class`裏的`static`就清理好了，整理好後，code變乾淨許多，不再有一堆奇奇怪怪的pointer存取。

## Component

參考自[Component - Decoupling Pattern](http://gameprogrammingpatterns.com/component.html)

在準備寫**Hero**的腳本控制時發現和**Event**腳本控制重複太多地方，於是用Component的方法把共同的地方接出來，很快就處理好了。像是`MoverComponent`:

```cpp
class MoverComponent{
public:
    MoverComponent(Object* _obj);
    void TickEvent(int delta_time);
    void Update();
//...
private:
//...    
    Object* obj;
};
```

在Event裏，會呼叫`new MoverComponent(this)`，借由操縱MoverComponent間接操作Event裏的status。當然Event是繼承自Object。這時也順便發現Hero也需要相同的Component，讓腳本可以操作他。

## 尚未處理的重要Issue

目前還有一些重要Issue，有必要處理掉

### BSD講完第一次話就Crash

這毫無頭緒._. [Issue:#14](https://github.com/mudream4869/crpg/issues/14)

### 讀取ogg或mp3

目前的引擎只可以讀取wav，這有點傷，因為wav檔沒經過壓縮，通常有點大，一個遊戲少說二三十的音效和音樂下來就差很多。

### 資源控管

目前有很多new出來的東西都沒delete掉，考慮用`shared_ptr`解決。