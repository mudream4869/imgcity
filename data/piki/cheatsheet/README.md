# Cheatsheet

有點雜亂的 Cheatsheet ，在 [misc-note](https://github.com/mudream4869/misc-note) 
有 [一份](https://github.com/mudream4869/misc-note/blob/master/cheatsheet/)，
可能會開 repo 來管理。

## Python

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

* 禁止ssh root

```
sed -i 's/PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config
/etc/init.d/ssh restart
```

* [ssh 小技巧](http://www.study-area.org/tips/ssh_tips.htm)

## Vim

* Makefile tab : `<C-V><Tab>`

## Git

### 移除 Submodule

```bash
mv a/submodule a/submodule_tmp

git submodule deinit -f -- a/submodule    
rm -rf .git/modules/a/submodule
git rm -f a/submodule
```

## Bash

### 尋找並且取代

```bash
sed -i 's/old-text/new-text/g' filename
```

### 尋找超過 1M 的檔案

```bash
find . -type f -size +1M
```

### 尋找某些檔案

```bash
find -L . -name '*.png'
```

### 在指定位置解開 deb package

```bash
dpkg -x {deb filename} {target folder}
```

### CMake 顯示所有 option

```bash
cmake -LA
```

## Ansible

### Python 版本問題

Ansible 錯誤訊息：

```
An unhandled exception occurred while running the lookup plugin 'hashi_vault'.
Error was a <class 'ansible.errors.AnsibleError'>,
original message:
Please pip install hvac to use the hashi_vault lookup module.
```

請檢查 Ansible 的 Python env

```bash
ansible -m debug -a 'var=ansible_playbook_python' localhost
```


```
localhost | SUCCESS => {
    "ansible_playbook_python": "/usr/local/Cellar/ansible/2.6.0/libexec/bin/python2.7"
}
```

```bash
source /usr/local/Celler/ansible/2.6.0/libexec/bin/activate
pip install hvac
```

[參考資料](https://github.com/ansible/ansible/issues/28050#issuecomment-402220672)

