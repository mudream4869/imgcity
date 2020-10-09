# Cheatsheet

有點雜亂的 Cheatsheet ，在 [misc-note](https://github.com/mudream4869/misc-note) 
有 [一份](https://github.com/mudream4869/misc-note/blob/master/cheatsheet/)，
可能會開 repo 來管理。

## iPyhton Noetbook

### Unzip

[Unzipping file in python](https://stackoverflow.com/questions/3451111/unzipping-files-in-python)

```
import zipfile
with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
    zip_ref.extractall(directory_to_extract_to)
```

## VirtualEnv

```
$ virtualenv {{env name}}
$ source bin/activate
```

## Postgresql

* phppgadmin

```bash
$ cp /etc/apache2/conf.d/phppgadmin /etc/apache2/conf-enabled/phppgadmin.conf
```

* 建立使用者

```bash
$ sudo -u postgres createuser --superuser $USER
$ sudo -u postgres psql
```

```
postgres=# \password $USER
```

```bash
$ sudo -u postgres createdb $USER
$ sudo -u postgres dropdb  [option...] dbname
```

* 資料備份

DUMP + UP:

```bash
$ pg_dump dbname > outfile
$ pg_dumpall > outfile
```

Dump Only Schema :

```bash
$ pg_dump -s > outfile
```

## ssh 安全

* [禁止ssh root](https://blog.longwin.com.tw/2008/10/security-debian-ubuntu-linux-deny-root-login-2008/)
* [ssh 小技巧](http://www.study-area.org/tips/ssh_tips.htm)

## CDN File

* [RawGit](https://rawgit.com)

## Vim

* Makefile tab : `<C-V><Tab>`
