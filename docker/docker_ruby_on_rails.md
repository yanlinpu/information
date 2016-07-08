## Docker 搭建 ruby on rails 环境demo                                                                                                              

#### 安装docker 

https://yeasy.gitbooks.io/docker_practice/content/install/ubuntu.html

#### 镜像images

```
$ sudo docker pull ubuntu:14.04
$ sudo docker pull ubuntu:15.10
$ sudo docker images

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              15.10               1d3353b199ba        12 days ago         137.3 MB
ubuntu              14.04               38c759202e30        12 days ago         196.6 MB

# Docker以ubuntu15.10 镜像创建一个新容器，然后在容器里执行 echo "Hello world"，然后输出结果。
$ sudo docker run ubuntu:15.10 echo "Hello world"
Hello world

# 运行交互式的容器
$ sudo docker run -ti --name web ubuntu:15.10 bash
root@8a978faeee46:/#

# 启动容器（后台模式）
$ sudo docker run -d ubuntu:15.10 /bin/sh -c "while true; do echo hello world; sleep 1; done"
087e546beb46977e46bf61c6c590a36aa68c9ef0655ec23701a1c836f9024e09

$ sudo docker logs 087e546beb46

# 停止容器
# sudo docker stop 087e546beb46

# 删除容器( -f )
$ sudo docker rm -f 087e546beb46

# 清理所有处于终止状态的容器
$ sudo docker rm $(sudo docker ps -a -q)

# 进入某个正在运行的容器
$ sudo docker exec -ti 2cf3a9c9d1f7(name) bash

# 容器互联
# $ sudo docker run -d -P --name web --link db:db training/webapp python app.py
# -P 当使用 -P 标记时，Docker 会随机映射一个 49000~49900 的端口到内部容器开放的网络端口。
# -p sudo docker run -d -p 5000:5000 ...

```

#### 创建git用户

```
$ useradd -m -s /bin/bash git # -m home directory will be created
$ passwd git ---> git
$ usermod -s /bin/bash git    # 修改git shell
$ vim /etc/sudoers #add    `git  ALL=(ALL:ALL) ALL`
```

#### ruby on rails 环境 

```
$ su - git
$ sudo apt-get update && apt-get -y upgrade && apt-get install
$ sudo apt-get install -y vim
$ sudo apt-get install -y build-essential zlib1g-dev libyaml-dev libssl-dev libgdbm-dev libreadline-dev libncurses5-dev libffi-dev curl git-core openssh-server redis-server postfix checkinstall libxml2-dev libxslt-dev libcurl4-openssl-dev libicu-dev mysql-client libmysqlclient-dev
$ python --version
$ sudo ln -s /usr/bin/python /usr/bin/python2
$ sudo apt-get install openssh-server
# rvm
$ curl -sSL https://get.rvm.io | bash;
$ source ~/.bashrc;
$ source ~/.bash_profile
$ rvm install 2.1.2
$ rvm use 2.1.2
$ rvm use 2.1.2 --default 
$ rvm gemset create rails4.2.1
$ rvm use 2.1.2@rails4.2.1
$ rvm use 2.1.2@rails4.2.1 --default
$ gem install rails -v=4.2.1
```

#### commit
```
$ sudo docker commit -m 'ruby(2.1.2) on rails(4.2.1) --default' -a 'yanlp' 9271e56ec1b3 yanlp/ubuntu14.04ruby-on-rails:v1
$ sudo docker login
$ sudo docker push yanlp/ubuntu14.04ruby-on-rails
```

#### 资源

- https://www.gitbook.com/book/yeasy/docker_practice/details
- http://blog.saymagic.cn/2015/06/01/learning-docker.html
- http://www.runoob.com/docker/docker-container-usage.html
- https://hub.docker.com/         # 用户名: yanlp
