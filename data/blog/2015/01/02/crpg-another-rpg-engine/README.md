# RPG引擎 - CRPG

這兩週全在寫一個跨平台的RPG引擎，來記錄一下第一階段所達成的

最近換了mac，想說要是能夠Mac上玩恐怖RPG那該有多好，可是大多經典恐怖RPG都沒有Mac版，可是去翻了一下RPGMaker並沒有支援Mac，覺得非常可惜。想說自己乾脆開發一個專門為恐怖RPG設計的引擎。
先給一下[Github:crpg](https://github.com/mudream4869/crpg)

以下大致說明三個重點：

## 引擎架構

基本上，為了能夠儘量讓RPGMaker無縫接軌，引擎架構很像RPGMaker的腳本，有在改RPGMaker腳本的朋友應該很熟悉以下這幾個物件：

* Scene：主要作為場景的母類別
* Window：遊戲內的視窗

為了能夠有一個大型的`Global Pool`，有一個會把`const char*` map到 `void*`的map:

```c++
struct StrCompare : public std::binary_function<const char*, const char*, bool>{
    public:
        bool operator() (const char* str1, const char* str2) const
            { return std::strcmp(str1, str2) < 0; }
};
typedef std::map<const char*, void* , StrCompare> Env;
```

其他幾個主要物件：

* Event：場景上的事件
* Tile：把Tile圖讀取進來
* Map：把地圖檔讀取進來

## 地圖格式

這是最主要的問題，要能被廣泛接受，並且有現成成熟的編輯器，原先有點擔心這塊，不過竟然已經有一群人做出來了，而且還開源：[TiledMapEditor](http://www.mapeditor.org)，xml格式也很容易讀取。

這裡直接推薦[rapidxml](http://rapidxml.sourceforge.net)。好用又快。

## 事件腳本

這裏我直接用Python，引擎會直接把腳本讀進來，呼叫腳本裡的函數。使用`Function Pointer Callback`達成腳本和遊戲引擎溝通。詳細方式見[C和Python混和編程](http://mudream.logdown.com/posts/247092/c-and-python-mixed-programming)

然後腳本可以這樣寫：

```python
from Event import Event 

class Event1(Event):
    def __init__(self, func):
        Event.__init__(self, func)
        self.config = {
            "event_name" : "event1",
            "image" : "hero.bmp",
            "trigger_condition" : "on chat",
            "solid" : "true",
            "fixed_direction" : "false"
        }
    def Action(self):
        self.global_value["Test1"] += 1
        self.global_flag["Test2"] = True
        self.ShowMsg("Hello~" + str(self.global_value["Test1"]))
        self.DoMove((["Right"],
                     ["Right"],
                     ["Right"]))
        self.WaitForMove()
```

繼承的Event母類別把Callback包裝好了，所以可以直接Call`self.xxx(yyy)`

以上是第一階段較為重要的完成，不過仍然有許多待完成的部分：

## 音效

打算採用`OpenAL`做到

## 遊戲物件

## 跨平台

目前`g++`的編譯參數仍然只有辦法在`mac`上編譯

## 事件當前狀態取得和設定

就是事件`Python`當前的執行狀態（包括Call Stack, Heap..等），目前上無頭緒，可能需要動到Python-dev的底層。要不一個替代的解決方案就是自己設計一個很像Python的Script，自行做他的Interpreter。

目前在[stackoverflow的發問](http://stackoverflow.com/questions/27737089/pyobject-how-to-save-the-status-of-a-function-which-is-from-a-class)

## 地形

這部分包括背景與主角的前後關係

不過這引擎的方向並不是全然RPG，我打算是往*恐怖遊戲*類型遊戲進行開發優化，所以並不會出現回合制對戰系統。及時制系統有可能會出現。