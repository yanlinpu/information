- [模拟linux登录shell](#模拟linux登录shell)
- [yes/no返回不同的结构](#yesno返回不同的结构)
- [a/b/c/d四选一并有三次选错的机会](#abcd四选一并且有三次选错的机会)

## 模拟linux登录shell

  ```
#!/bin/bash
echo -n "login:"
read name
echo -n "password:"
stty -echo # 输入不显示
read password 
stty echo  # 关闭输入不显示
# echo -e "\nyour name is $name and password is $password"
if [[ "$name" = "ylp" && "$password" = "123" ]]; then
  echo "the host and password is right!"
else
  echo "input is error!"
fi
  ```
  
## yes/no返回不同的结构

  ```
#!/bin/bash
echo -n "enter [y/n]:"
read res 
case $res in
  y|Y|yes|YES) 
    echo "you enter y"
    ;;  
  n|N|no|NO)
    echo "you enter n"
    ;;  
  *)  
    echo "error"
    ;;  
esac
  ```
  
## a/b/c/d四选一并且有三次选错的机会

  ```
#!/bin/bash                                                                                           
# echo "the first argument is $1."
total=3

# array initialize
# choices="a|b|c|d"
# IFS='|' CHOICES=( $choices )
CHOICES=(a b c d)

puts_choice() {
  echo "your choice is: ${1}."
}

# select
choice_select() {
  echo "you have only $total time(s) to choice."
  # 四则运算
  # total=$[ total - 1 ]
  # total=$(( total - 1 ))
  let total=total-1
  PS3='enter your choice with number: ' # 提示符字串
  select val in "${CHOICES[@]}"; do     # val 为CHOICES中的值 not编号 
    check_validity $val
    break
  done
}

# case
check_validity() {
  if [[ "$total" > 0 ]]; then
    case "$1" in
      a|A )
        puts_choice a
        ;;  
      b|B )
        puts_choice b
        ;;  
      c|C )
        puts_choice c
        ;;  
      d|D )
        puts_choice d 
        ;;  
      * ) 
        choice_select
        ;;  
    esac
  else
    echo '参数错误: a(A) b(B) c(C) d(D).'
    exit 1
  fi  
}

check_validity "$1"

exit 0
  ```
  
  
