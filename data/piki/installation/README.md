# 重裝系統

## MAC製作開機隨身碟

1. 插入隨身碟
2. 在terminal輸入：`diskutil list`，找到隨身碟的編號*N*
3. 先取消連結（避免佔用資源，無法進行下一個步驟）：`diskutil unmountDisk /dev/diskN`
4. `sudo dd if=YOURISOFILE.ISO of=/dev/rdiskN bs=1m`：dd指令會把檔案全寫進去，rdisk是無buffer。
5. 退出隨身碟：`diskutil eject /dev/diskN` 
