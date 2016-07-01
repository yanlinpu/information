## 交互式脚本 --- expect

- 安装

  `sudo apt-get install expect`

- demo1 >> git http push

  ```
#!/bin/bash                                                                                                                
while true ; do
/usr/bin/expect <<EOF
spawn bash -c {cd /home/git/ylp/yanlp ; echo -e "aaaa\n" >> aaaa.md ; git add aaaa.md; git commit -m "aaaa"; git push origin master}
expect "Username for 'https://*"
send "yanlinpu\n"
expect "Password for 'https*"
send "********\n"
interact
sleep 1
EOF
sleep 10
done
  ```
- demo2 >> ssh实现自动登录,并停在登录服务器上

  ```
#!/usr/bin/expect
set ipaddr 192.168.5.71
set passwd git
spawn ssh git@$ipaddr

expect {
  "yes/no" {send "yes\n"; exp_continue}  # 可有可无 没有继续执行
  "password:" {send "$passwd\n"}
}
# 执行完成后保持交互状态，把控制权交给控制台
# 这个时候就可以手工操作了。如果没有这一句登录完成后会退出，而不是留在远程终端上。                                         
interact
  ```
  
- demo3 >> scp

  ```
#!/usr/bin/expect                                                                                                          
set timeout 10  
#set host [lindex $argv 0]  
#set username [lindex $argv 1]  
#set password [lindex $argv 2]  
#set src_file [lindex $argv 3]  
#set dest_file [lindex $argv 4]  
set host 192.168.5.71
set username git
set password git
set src_file /home/git/ylp
set dest_file /home/git/nohup.out
spawn scp $username@$host:$dest_file $src_file 
expect {  
  "(yes/no)?"  
  {  
    send "yes\n"
    exp_continue  
    expect "*assword:" { send "$password\n"; exp_continue}  
  }  
  "*assword:"  
  {  
    send "$password\n" 
    exp_continue 
  }  
} 
  ```
  
