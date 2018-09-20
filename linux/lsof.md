## 使用 lsof 代替 Mac OS X 中的 netstat 查看占用端口的程序

`$ lsof -i :8200`

-------------

## lsof 

lsof（list open files）是一个列出当前系统打开文件的工具。

```
$ lsof -i
COMMAND     PID     USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
```

- COMMAND：进程的名称
- PID：进程标识符
- USER：进程所有者
- FD：文件描述符，应用程序通过文件描述符识别该文件。如cwd、txt等
- TYPE：文件类型，如DIR、REG等
- DEVICE：指定磁盘的名称
- SIZE：文件的大小
- NODE：索引节点（文件在磁盘上的标识）
- NAME：打开文件的确切名称

FD 列中的文件描述符cwd 值表示应用程序的当前工作目录，这是该应用程序启动的目录，除非它本身对这个目录进行更改,txt 类型的文件是程序代码，
如应用程序二进制文件本身或共享库，如上列表中显示的 /sbin/init 程序。

其次数值表示应用程序的文件描述符，这是打开该文件时返回的一个整数。如上的最后一行文件/dev/initctl，其文件描述符为 10。
u 表示该文件被打开并处于读取/写入模式，而不是只读 ® 或只写 (w) 模式。同时还有大写 的W 表示该应用程序具有对整个文件的写锁。
该文件描述符用于确保每次只能打开一个应用程序实例。初始打开每个应用程序时，都具有三个文件描述符，从 0 到 2，
分别表示标准输入、输出和错误流。所以大多数应用程序所打开的文件的 FD 都是从 3 开始。

与 FD 列相比，Type 列则比较直观。文件和目录分别称为 REG 和 DIR。而CHR 和 BLK，分别表示字符和块设备；
或者 UNIX、FIFO 和 IPv4，分别表示 UNIX 域套接字、先进先出 (FIFO) 队列和网际协议 (IP) 套接字。

## 常用参数

`lsof ［options］ filename`

- lsof abc.txt 显示开启文件abc.txt的进程
- lsof -c abc 显示abc进程现在打开的文件
- lsof -c -p 1234 列出进程号为1234的进程所打开的文件
- lsof -g gid 显示归属gid的进程情况
- lsof +d /usr/local/ 显示目录下被进程开启的文件
- lsof +D /usr/local/ 同上，但是会搜索目录下的目录，时间较长
- lsof -d 4 显示使用fd为4的进程
- lsof -i 用以显示符合条件的进程情况
- lsof -i[46] [protocol][@hostname|hostaddr][:service|port]
    - 46 --> IPv4 or IPv6
    - protocol --> TCP or UDP
    - hostname --> Internet host name
    - hostaddr --> IPv4地址
    - service --> /etc/service中的 service name (可以不止一个)
    - port --> 端口号 (可以不止一个)

## 实例

