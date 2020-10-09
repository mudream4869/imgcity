# Recording Gaming Moment

最近嘗試錄製 FTB Lite 3.0 的影片（[有興趣的話點我](https://www.youtube.com/watch?v=O1kDjf_xwLI)），發現聲音很糟。

## OBS

我是用 OBS 作為錄製工具，一方面來說之前我也拿來在 Twitch 上直播。

在聲音方面是因為聲音是擷取自麥克，所以來看看有沒有什麼方法可以直接抓取遊戲聲音。在 OBS 的一些 Windows 的教學文找，似乎只要新增一個叫做「Destop Audio」的音源即可，可是 Mac OS 並沒有給出這個選項。

硬是要擷取，是需要一個叫做 [Wavtap](https://github.com/pje/WavTap) 的軟體。

## WavTap

運作原理類似 **Sypthon** ，也是把訊號來源重新導向。

在 Mac OS 上安裝，需要看版本，像是我的版本是 **Sierra**，那麼要先在 Recovery Mode `⌘R` 把一部份 **SIP** 關掉：

```
csrutil enable --without kext
```

然後再一般模式才能成功安裝，並且執行。

## SIP

全名是 System Integrity Protection，是 10.11 追加的，主要是用來保護系統還有驅動程式。

## 參考

* [WavTap](https://github.com/pje/WavTap)
* [Setting Up Mac Desktop Sound Capture with WavTap](https://obsproject.com/forum/resources/setting-up-mac-desktop-sound-capture-with-wavtap.79/)
* [關閉 OSX 10.11 SIP (System Integrity Protection) 功能](https://cms.35g.tw/coding/%E9%97%9C%E9%96%89-osx-10-11-sip-system-integrity-protection-%E5%8A%9F%E8%83%BD/)