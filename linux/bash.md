- 磁盘空间`$ df -h`
- 某个目录的磁盘使用情况`$ du dir/ -h`

    - h：按用户易读的格式输出大小，即用K替代千字节，用M替代兆字节，用G替代吉字节。
    - s：显示每个输出参数的总计。
- 排序`$ sort -t ':' -k 3 -n /etc/passwd` 目录磁盘大小排序`du -s * | sort -nr `
- 搜索`$ grep -nRi --exclude-dir=node_modules --exclude-dir=public 'business_certificate' ./tg_sys_admin`
- `which ps`=`type -a ps`
- 全局环境变量`env | printenv | printenv HOME | echo $HOME`
- 局部环境变量`set` 包括全局环境变量



## read,array,declare

```
read [-pt] variable
-p ：后面可以接提示字符！
-t ：后面可以接等待的“秒数！”这个比较有趣～不会一直等待使用者啦！

declare [-aixr] variable
-a ：将后面名为 variable 的变量定义成为阵列 （array） 类型
-i ：将后面名为 variable 的变量定义成为整数数字 （integer） 类型
-x ：用法与 export 一样，就是将后面的 variable 变成环境变量；
-r ：将变量设置成为 readonly 类型，该变量不可被更改内容，也不能 unset
```

## 变量内容的删除、取代与替换

```
1. 从变量内容的最前面开始向右删除，且仅删除最短的那个
${variable#/*:}

2. 从变量内容的最前面开始向右删除，且仅删除最长的那个
${variable##/*:}

3. 从变量内容的最后面开始向左删除，且仅删除最短的那个
${variable%:*}

4. 从变量内容的最后面开始向左删除，且仅删除最长的那个
${variable%%:*}

${变量#关键字}              若变量内容从头开始的数据符合“关键字”，则将符合的最短数据删除
${变量##关键字}             若变量内容从头开始的数据符合“关键字”，则将符合的最长数据删除
${变量%关键字}              若变量内容从尾向前的数据符合“关键字”，则将符合的最短数据删除
${变量%%关键字}             若变量内容从尾向前的数据符合“关键字”，则将符合的最长数据删除
${变量/旧字串/新字串}        若变量内容符合“旧字串”则“第一个旧字串会被新字串取代” 
${变量//旧字串/新字串}       若变量内容符合“旧字串”则“全部的旧字串会被新字串取代”

```


## 变量设置方式


变量设置方式|str 没有设置|str 为空字串|str 已设置非为空字串
---|---|---|---
var=${str-expr}| var=expr| var=| var=$str
var=${str:-expr}| var=expr| var=expr| var=$str
var=${str+expr}| var= |var=expr |var=expr
var=${str:+expr}| var= | var=| var=expr
var=${str=expr}| str=expr var=expr| str 不变 var=| str 不变 var=$str
var=${str:=expr}| str=expr var=expr| str=expr var=expr| str 不变 var=$str
var=${str?expr}| expr 输出至 stderr| var=| var=$str
var=${str:?expr}| expr 输出至 stderr| expr 输出至 stderr| var=$str

## 数据流重导向

- 1> ：以覆盖的方法将“正确的数据”输出到指定的文件或设备上；
- 1>>：以累加的方法将“正确的数据”输出到指定的文件或设备上；
- 2> ：以覆盖的方法将“错误的数据”输出到指定的文件或设备上；
- 2>>：以累加的方法将“错误的数据”输出到指定的文件或设备上；
- 至于写入同一个文件的特殊语法如上表所示，你可以使用 2>&1;
- cat > catfile; 创建一个catfile文件 ctrl+d结束;
- cat > catfile < ~/.bashrc 用 stdin 取代键盘的输入以创建新文件;
- cat > catfile << "eof"  eof代替ctrl+d 结束;

## 排序命令： sort, wc, uniq

last | cut -d ' ' -f 1 | sort -b | uniq -c

## 字符转换命令： tr, col, join, paste, expand

```
tr [-ds] SET1 ...
-d ：删除讯息当中的 SET1 这个字串；
-s ：取代掉重复的字符！
$ last | tr [a-z] [A-Z]

col [-xb]
-x ：将 tab 键转换成对等的空白键
$ cat /etc/man_db.conf | col -x | cat -A | more

join [-ti12] file1 file2
-t ：join 默认以空白字符分隔数据，并且比对“第一个字段”的数据，如果两个文件相同，则将两笔数据联成一行，且第一个字段放在第一个！
-i ：忽略大小写的差异；
-1 ：这个是数字的 1 ，代表“第一个文件要用那个字段来分析”的意思；
-2 ：代表“第二个文件要用那个字段来分析”的意思。

paste [-d] file1 file2
-d ：后面可以接分隔字符。默认是以 [tab] 来分隔的！
- ：如果 file 部分写成 - ，表示来自 standard input 的数据的意思。

expand [-t] file
-t ：后面可以接数字。一般来说，一个 tab 按键可以用 8 个空白键取代。
我们也可以自行定义一个 [tab] 按键代表多少个字符呢！
```

## xargs 
```
xargs [-0epn] command
-0 ：如果输入的 stdin 含有特殊字符，例如 `, \, 空白键等等字符时，这个 -0 参数可以将他还原成一般字符。这个参数可以用于特殊状态喔！
-e ：这个是 EOF （end of file） 的意思。后面可以接一个字串，当 xargs 分析到这个字串时，就会停止继续工作！
-p ：在执行每个指令的 argument 时，都会询问使用者的意思；
-n ：后面接次数，每次 command 指令执行时，要使用几个参数的意思。

$ ls *.jpg | xargs -n1 -i cp {} /external-hard-drive/directory
$ cut -d ':' -f 1 /etc/passwd | head -n 3 | xargs -i id {}
$ cut -d ':' -f 1 /etc/passwd | head -n 3 | xargs -n 1 id
```

## sed

```
sed [-nefr] [动作]
选项与参数：
-n ：使用安静（silent）模式。在一般 sed 的用法中，所有来自 STDIN 的数据一般都会被列出到屏幕上。但如果加上 -n 参数后，则只有经过 sed 特殊处理的那一行（或者动作）才会被列出来。
-e ：直接在命令行界面上进行 sed 的动作编辑；
-f ：直接将 sed 的动作写在一个文件内， -f filename 则可以执行 filename 内的 sed 动作；
-r ：sed 的动作支持的是延伸型正则表达式的语法。（默认是基础正则表达式语法）
-i ：直接修改读取的文件内容，而不是由屏幕输出。
动作说明： [n1[,n2]]function
n1, n2 ：不见得会存在，一般代表“选择进行动作的行数”，举例来说，如果我的动作
是需要在 10 到 20 行之间进行的，则“ 10,20[动作行为] ”
function 有下面这些咚咚：
a ：新增， a 的后面可以接字串，而这些字串会在新的一行出现（目前的下一行）～
c ：取代， c 的后面可以接字串，这些字串可以取代 n1,n2 之间的行！
d ：删除，因为是删除啊，所以 d 后面通常不接任何咚咚；
i ：插入， i 的后面可以接字串，而这些字串会在新的一行出现（目前的上一行）；
p ：打印，亦即将某个选择的数据印出。通常 p 会与参数 sed -n 一起运行～
s ：取代，可以直接进行取代的工作哩！通常这个 s 的动作可以搭配正则表达式！
例如 1,20s/old/new/g 就是啦！
```

## awk

awk 也是一个非常棒的数据处理工具！相较于 sed 常常作用于一整个行的处理， awk 则比较
倾向于一行当中分成数个“字段”来处理。因此，awk 相当的适合处理小型的数据数据处理呢！

```
$ last -n 5 | awk '{print $1 "\t lines: " NR "\t columns: " NF}'
$ cat passwd | awk '{FS=":"} $3 > 1000 {print $1 "\t" $3}'
$ cat passwd | awk 'BEGIN {FS=":"} $3 > 1000 {print $1 "\t" $3}'

pay.txt
Name 1st 2nd 3th
VBird 23000 24000 25000
DMTsai 21000 20000 23000
Bird2 43000 42000 41000

$ cat pay.txt | awk 'NR==1 {printf "%10s %10s %10s %10s %10s\n", $1, $2, $3, $4, "Total"} NR>=2 {total=$2+$3+$4; printf "%10s %10d %10d %10d %10.2f\n", $1, $2, $3, $4, total}'
$ cat pay.txt | awk '{if(NR==1) printf "%10s %10s %10s %10s %10s\n", $1, $2, $3, $4, "Total"} NR>=2 {total=$2+$3+$4; printf "%10s %10d %10d %10d %10.2f\n", $1, $2, $3, $4, total}'
```