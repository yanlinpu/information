- 账号 /etc/passwd
- 密码 /etc/shadow
- gid组 /etc/group
- group密码 /etc/gshadow

### 目前的密码加密机制

```
$ authconfig --test &#124; grep hashing
password hashing algorithm is sha512
```

## group

- 有效群组（effective group）写
- 与初始群组（initial group）读
- newgrp: 有效群组的切换

## 账号管理

### 新增与移除使用者： useradd, 相关配置文件, passwd, usermod, userdel

```
useradd [-u UID] [-g 初始群组] [-G 次要群组] [-mM] > [-c 说明栏] [-d 主文件夹绝对路径] [-s shell] 使用者帐号名
选项与参数：
-u ：后面接的是 UID ，是一组数字。直接指定一个特定的 UID 给这个帐号；
-g ：后面接的那个群组名称就是我们上面提到的 initial group 啦～ 该群组的 GID 会被放置到 /etc/passwd 的第四个字段内。
-G ：后面接的群组名称则是这个帐号还可以加入的群组。这个选项与参数会修改 /etc/group 内的相关数据喔！
-M ：强制！不要创建使用者主文件夹！（系统帐号默认值）
-m ：强制！要创建使用者主文件夹！（一般帐号默认值）
-c ：这个就是 /etc/passwd 的第五栏的说明内容啦～可以随便我们设置的啦～
-d ：指定某个目录成为主文件夹，而不要使用默认值。务必使用绝对路径！
-r ：创建一个系统的帐号，这个帐号的 UID 会有限制 （参考 /etc/login.defs）
-s ：后面接一个 shell ，若没有指定则默认是 /bin/bash 的啦～
-e ：后面接一个日期，格式为“YYYY-MM-DD”此项目可写入 shadow 第八字段，亦即帐号失效日的设置项目啰；
-f ：后面接 shadow 的第七字段项目，指定密码是否会失效。0为立刻失效，-1 为永远不失效（密码只会过期而强制于登陆时重新设置而已。）

$ useradd -g users liujx
$ grep liujx /etc/shadow /etc/passwd /etc/group
/etc/shadow:liujx:!!:17772:0:99999:7:::
/etc/passwd:liujx:x:1015:100::/home/liujx:/bin/bash
```

使用 useradd 创建了帐号之后，在默认的情况下，该帐号是暂时被封锁的， 也就是说，该帐号是无法登陆的

```
passwd [-l] [-u] [--stdin] [-S] [-n 日数] [-x 日数] [-w 日数] [-i 日期] 帐号 
选项与参数：
--stdin ：可以通过来自前一个管线的数据，作为密码输入，对 shell script 有帮助！
-l ：是 Lock 的意思，会将 /etc/shadow 第二栏最前面加上 ! 使密码失效；
-u ：与 -l 相对，是 Unlock 的意思！
-S ：列出密码相关参数，亦即 shadow 文件内的大部分信息。
-n ：后面接天数，shadow 的第 4 字段，多久不可修改密码天数
-x ：后面接天数，shadow 的第 5 字段，多久内必须要更动密码
-w ：后面接天数，shadow 的第 6 字段，密码过期前的警告天数
-i ：后面接“日期”，shadow 的第 7 字段，密码失效日期

```

