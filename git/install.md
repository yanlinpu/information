## ubuntu升级git到最新版本

- apt-get(but false -_-!)

  ```
$ sudo apt-add-repository ppa:git-core/ppa  
$ sudo apt-get update  
$ sudo apt-get install git
#如果本地已经安装过Git，可以使用升级命令
$ sudo apt-get dist-upgrade 
  ```
  
- 源码 make

  ```
#下载 https://www.kernel.org/pub/software/scm/git/
# 1 安装编译源码包的工具：
$sudo apt-get installlibcurl4-gnutls-dev libexpat1-dev gettext libz-dev libssl-dev
# 2 展开源码包，进入：
$ tar -xvf Git-2.6.2.tar.xz
$ cd git-2.6.2
# 3 安装Git到/usr/local/bin中（安装方法写在INSTALL文件中）：
$ make prefix=/usr/local all
$ sudo make prefix=/usr/local install
# 新开终端
$ git --version
  ```
