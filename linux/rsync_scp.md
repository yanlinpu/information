# rsync 和 scp 的最大区别是：
rsync 是分块校验+传输，scp 是整个文件传输。rsync 比 scp 有优势的地方在于单个大文件的一小部分存在改动时，只需传输改动部分，
无需重新传输整个文件。如果传输一个新的文件，理论上 rsync 没有优势。
另外，rsync 不是加密传输，而 scp 是加密传输，使用时可以按需选择。
rsync可以压缩传输。

## rsync 

- usage

    - 本地机器的内容拷贝到远程机器 `rsync [OPTION]... SRC [SRC]... [USER@]HOST:DEST`
    - 将远程机器的内容拷贝到本地机器 `rsync [OPTION]... [USER@]HOST:SRC [DEST]`
    - 拷贝本地文件 `rsync [OPTION]... SRC [SRC]... DEST`
    - 从本地机器拷贝文件到远程rsync服务器中 `rsync [OPTION]... SRC [SRC]... [USER@]HOST::DEST`
    - 从远程rsync服务器中拷贝文件到本地机 `rsync [OPTION]... [USER@]HOST::SRC [DEST]`
    - 列远程机的文件列表 `rsync [OPTION]... rsync://[USER@]HOST[:PORT]/SRC [DEST]`
    - `rsync [OPTION]... SRC [SRC]... rsync://[USER@]HOST[:PORT]/DEST`

-  OPTIONS
```
# rsync -avP --exclude=tmp
-a, --archive 归档模式，表示以递归方式传输文件，并保持所有文件属性，等于-rlptgoD。 
-v, --verbose 详细模式输出。
--partial 保留那些因故没有完全传输的文件，以是加快随后的再次传输。 
-P 等同于 --partial。  
--exclude=PATTERN 指定排除不需要传输的文件模式。 
--include=PATTERN 指定不排除而需要传输的文件模式。 
--exclude-from=FILE 排除FILE中指定模式的文件。 
--include-from=FILE 不排除FILE指定模式匹配的文件。

-r, --recursive 对子目录以递归模式处理。 
-l, --links 保留软链结。 
-p, --perms 保持文件权限。 
-t, --times 保持文件时间信息。 
-g, --group 保持文件属组信息。 
-o, --owner 保持文件属主信息。 
-D, --devices 保持设备文件信息。 


--delete 删除那些DST中SRC没有的文件。 
-q, --quiet 精简输出模式。 
-c, --checksum 打开校验开关，强制对文件传输进行校验。 
-R, --relative 使用相对路径信息。 
-b, --backup 创建备份，也就是对于目的已经存在有同样的文件名时，将老的文件重新命名为~filename。可以使用--suffix选项来指定不同的备份文件前缀。 
--backup-dir 将备份文件(如~filename)存放在在目录下。 
-suffix=SUFFIX 定义备份文件前缀。 
-u, --update 仅仅进行更新，也就是跳过所有已经存在于DST，并且文件时间晚于要备份的文件，不覆盖更新的文件。 
-L, --copy-links 想对待常规文件一样处理软链结。 
--copy-unsafe-links 仅仅拷贝指向SRC路径目录树以外的链结。 
--safe-links 忽略指向SRC路径目录树以外的链结。 
-H, --hard-links 保留硬链结。 
-S, --sparse 对稀疏文件进行特殊处理以节省DST的空间。 
-n, --dry-run现实哪些文件将被传输。 
-w, --whole-file 拷贝文件，不进行增量检测。 
-x, --one-file-system 不要跨越文件系统边界。 
-B, --block-size=SIZE 检验算法使用的块尺寸，默认是700字节。 
-e, --rsh=command 指定使用rsh、ssh方式进行数据同步。 
--rsync-path=PATH 指定远程服务器上的rsync命令所在路径信息。 
-C, --cvs-exclude 使用和CVS一样的方法自动忽略文件，用来排除那些不希望传输的文件。 
--existing 仅仅更新那些已经存在于DST的文件，而不备份那些新创建的文件。 
--delete-excluded 同样删除接收端那些被该选项指定排除的文件。 
--delete-after 传输结束以后再删除。 
--ignore-errors 及时出现IO错误也进行删除。 
--max-delete=NUM 最多删除NUM个文件。 
--force 强制删除目录，即使不为空。 
--numeric-ids 不将数字的用户和组id匹配为用户名和组名。 
--timeout=time ip超时时间，单位为秒。 
-I, --ignore-times 不跳过那些有同样的时间和长度的文件。 
--size-only 当决定是否要备份文件时，仅仅察看文件大小而不考虑文件时间。 
--modify-window=NUM 决定文件是否时间相同时使用的时间戳窗口，默认为0。 
-T --temp-dir=DIR 在DIR中创建临时文件。 
--compare-dest=DIR 同样比较DIR中的文件来决定是否需要备份。 
--progress 显示备份过程。 
-z, --compress 对备份的文件在传输时进行压缩处理。  
--version 打印版本信息。 
--address 绑定到特定的地址。 
--config=FILE 指定其他的配置文件，不使用默认的rsyncd.conf文件。 
--port=PORT 指定其他的rsync服务端口。 
--blocking-io 对远程shell使用阻塞IO。 
-stats 给出某些文件的传输状态。 
--progress 在传输时现实传输过程。 
--log-format=formAT 指定日志文件格式。 
--password-file=FILE 从FILE中得到密码。 
--bwlimit=KBPS 限制I/O带宽，KBytes per second。 
-h, --help 显示帮助信息。
```    
- [demo](https://linux.cn/article-4503-1.html)

```
# 启用压缩
rsync -zvr /home/aloft/ /backuphomedir
# 保留文件和文件夹的属性
rsync -azvr /home/aloft/ /backuphomedir
# 同步本地到远程主机
rsync -avz /home/aloft/ demo@192.168.1.4:/share/rsysnctest/
# 远程同步到本地
rsync -avz demo@192.168.1.4:/share/rsysnctest/ /home/aloft/
# 找出文件间的不同
rsync -avzi /backuphomedir /home/aloft/
# 备份
rsync -avz -e 'ssh -p2093' /home/test/ root@192.168.1.150:/oracle/data/
```


## scp


`scp [-12346BCEpqrv] [-c cipher] [-F ssh_config] [-i identity_file] [-l limit] [-o ssh_option] [-P port] [-S program] [[user@]host1:]file1 ... [[user@]host2:]file2`

```
scp -r -P 22 local_folder [remote_username@]remote_ip:remote_folder
scp -r [remote_username@]remote_ip:remote_folder local_folder

-r 若 source 中含有目录名，则将目录下之档案亦皆依序拷贝至目的地。
-P 选择端口 . 注意 -p 已经被 rcp 使用 . 
-a 尽可能将档案状态、权限等资料都照原状予以复制。
-f 若目的地已经有相同档名的档案存在，则在复制前先予以删除再行复制。
-v 和大多数 linux 命令中的 -v 意思一样 , 用来显示进度 . 可以用来查看连接 , 认证 , 或是配置错误 . 
-C 使能压缩选项 . 
-4 强行使用 IPV4 地址 . 
-6 强行使用 IPV6 地址 .
```

