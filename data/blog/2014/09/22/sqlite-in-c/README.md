# Sqlite3 in C

最近在弄一些東西的時後發現有時會想要實作一些構想
然後又大概只是實驗性質的，資料庫內的資料並不會爆炸
`Sqlite` 就變成首選啦！

首先要在linux底下用他，必須先建制好環境：
```
sudo apt-get install sqlite3
sudo apt-get install libsqlite3-dev
```
然後這是範例code：
```c
// test.c
#include<sqlite3.h>
#include<stdio.h>
int main(){
    sqlite3* db;
    char* errmsg = NULL; 
    char** result;
    if(sqlite3_open_v2("main.db", &db, 
                        SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE, NULL)){
        printf("error!\n");
    }
    sqlite3_exec(db, "CREATE TABLE tbtest(pid int, ptitle char(50))", 0, 0, &errmsg);
    sqlite3_exec(db, "INSERT INTO (pid, ptitle) VALUES (1, 'test1')", 0, 0, &errmsg);
    printf("%lld\n", sqlite3_last_insert_rowid(db));
    sqlite3_close(db);
    return 0;
}
```
注意：
要編譯程式時必須link sqlite3
```
gcc test.c -lsqlite3 -o test
```

在開發時，可以搭配`sqliteman` GUI界面 。