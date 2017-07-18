# nginx.conf配置文件详解
nginx配置文件主要分为六个区域：   

- main(全局设置)
- events(nginx工作模式)
- http(http设置)
- sever(主机设置)
- location(URL匹配)
- upstream(负载均衡服务器设置)

参考文献：

> - [nginx的配置、虚拟主机、负载均衡和反向代理](https://www.zybuluo.com/phper/note/89391)
> - [（总结）Nginx配置文件nginx.conf中文详解](http://www.ha97.com/5194.html)

## main模块
```
# 定义Nginx运行的用户和用户组，默认由nobody账号运行
# user user [group];
user www www;

# nginx进程数，建议设置为等于CPU总核心数。
# worker_processes number | auto;
worker_processes 8;

# 进程文件
pid /var/run/nginx.pid;

# 全局错误日志定义类型 服务日志
# error_log file | stderr [debug | info | notice | warn | error | crit | alert| emerg]
error_log  /var/log/nginx/error.log  notice;

# 一个nginx进程打开的最多文件描述符数目，理论值应该是最多打开文件数（系统的值ulimit -n）与nginx进程数相除，
# 但是nginx分配请求并不均匀，所以建议与ulimit -n的值保持一致。
worker_rlimit_nofile 40960;
```

## events 模块
events模块来用指定nginx的工作模式和工作模式及连接数上限，一般是这样：

```
events {
  # 设置网络连接的序列化 
  # 当某一时刻只有一个网络连接到来时，多个睡眠进程会被同时惊醒，但只有一个进程可获得连接。
  # 如果每次唤醒的进程数太多，会影响一部分系统性能。默认on
  # accept_mutex on | off

  # 设置是否允许同时接收多个网络连接。默认off
  # multi_accept on | off
  multi_accept on

  # 事件驱动模型的选择
  # use method
  # 常用method有：select poll kqueue epoll rtsig /dev/poll eventport
  use epoll;

  # 配置最大连接数
  # worker_connections number;
  # number 不能大于操作系统支持打开的最大文件句柄数量。
  worker_connections 40960;
}
```

> - `use` 参考事件模型，use [ kqueue | rtsig | epoll | /dev/poll | select | poll ];
epoll模型是Linux 2.6以上版本内核中的高性能网络I/O模型，如果跑在FreeBSD上面，就用kqueue模型。

> - `worker_connections`用于定义Nginx每个进程的最大连接数，即接收前端的最大请求数，默认是1024。
最大客户端连接数由worker_processes和worker_connections决定，即Max_clients=worker_processes*worker_connections，
在作为反向代理时，Max_clients变为：Max_clients = worker_processes * worker_connections/4。 
进程的最大连接数受Linux系统进程的最大打开文件数限制，在执行操作系统命令`ulimit -n 40960`后worker_connections的设置才能生效

## http 模块
http模块可以说是最核心的模块了，它负责HTTP服务器相关属性的配置，它里面的server和upstream子模块，至关重要

```
http {
  # 文件扩展名与文件类型映射表
  include mime.types; 
  
  # 默认文件类型
  # 默认为 text/plain
  default_type application/octet-stream;

  # log_format name string 
  # name 默认为 combined
  log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';    

  # 默认编码
  charset utf-8; 
  
  # 为了高速寻找到响应server name 能力，Nginx使用列表来存储。设置每个散列桶占用内存大小。 32|64|128
  # server_names_hash_bucket_size 128; 
  
  # 上传文件大小限制
  # 默认值：1k
  # 这个指令指定客户端请求的http头部缓冲区大小绝大多数情况下一个头部请求的大小不会大于1k
  # getconf PAGESIZE
  # client_header_buffer_size 32k; 
  
  # 语法：large_client_header_buffers number size; 4 4k/8k
  # 指令指定客户端请求的一些比较大的头文件到缓冲区的最大值，如果一个请求的URI大小超过这个值，服务
  # 器将返回一个"Request URI too large" (414)，同样，如果一个请求的头部字段大于这个值，服务器将返回"Bad request" (400)。
  # large_client_header_buffers 4 64k; 
  
  # 这个指令指定允许客户端请求的最大的单个文件字节数，它出现在请求头部的Content-Length字段。
  # 如果请求大于指定的值，客户端将收到一个"Request Entity Too Large" (413)错误。
  # 默认值：client_max_body_size 1m
  client_max_body_size 1024m;
  
  # 开启高效文件传输模式，sendfile指令指定nginx是否调用sendfile函数来输出文件，对于普通应用设为 on，
  # 如果用来进行下载等应用磁盘IO重负载应用，可设置为off，以平衡磁盘与网络I/O处理速度，降低系统的负载。
  # 注意：如果图片显示不正常把这个改成off。
  # sendfile on | off;
  sendfile on; 
  # sendfile_max_chunk size;
  # 默认为0
  # if 0 sendfile()传输的数据量大小无限制，if > 0 sendfile()传输的数据量最大不能超过这个值
  sendfile_max_chunk 128k;

  
  # 开启目录列表访问，合适下载服务器，默认关闭。
  autoindex on;
  
  tcp_nopush on; #防止网络阻塞
  tcp_nodelay on; #防止网络阻塞

  # 配置连接超时时间
  # keepalive_timeout timeout[header_timeout];
  # 长连接超时时间，单位是秒
  # 服务器端保持连接的时间为120s，发送给用户端的应答报文头部中keep-alive域的时间为10s
  keepalive_timeout 120s 100s; 

  # 单链接请求数上限
  # 用于限制用户通过某一连接向Nginx服务器发送请求的次数。
  # keepalive_requests number; 默认100

  #FastCGI相关参数是为了改善网站的性能：减少资源占用，提高访问速度。下面参数看字面意思都能理解。
  fastcgi_connect_timeout 300;
  fastcgi_send_timeout 300;
  fastcgi_read_timeout 300;
  fastcgi_buffer_size 64k;
  fastcgi_buffers 4 64k;
  fastcgi_busy_buffers_size 128k;
  fastcgi_temp_file_write_size 128k;

  #gzip模块设置
  gzip on; #开启gzip压缩输出
  gzip_min_length 1k; #最小压缩文件大小
  gzip_buffers 16 8k; #压缩缓冲区
  # gzip_http_version 1.0; #压缩版本（默认1.1，前端如果是squid2.5请使用1.0）
  gzip_comp_level 3; #压缩等级
  gzip_types text/plain application/x-javascript text/css application/xml;
  #压缩类型，默认就已经包含text/html，所以下面就不用再写了，写上去也不会有问题，但是会有一个warn。
  gzip_vary on;
  
  # ip-filtering
  #limit_zone crawler $binary_remote_addr 10m; #开启限制IP连接数的时候需要使用
  #limit_req_zone $binary_remote_addr zone=allips:10m rate=20r/m;
  #limit_conn_zone $binary_remote_addr zone=one:10m; #来限制并发连接数以及下载带宽
  
  include /etc/nginx/sites-enabled/*;  # 其他http内部server、upstream模块配置文件
}
```

> - [nginx如何解决超长请求串](http://www.51testing.com/html/13/377613-805851.html)

> - [nginx配置limit_conn_zone来限制并发连接数以及下载带宽](http://www.dnsdizhi.com/post-189.html)

> - [nginx配置limit_req_zone来限制IP连接数](http://hopestar.github.io/2013/06/08/nginx-limit-moule-note/)

## server 模块
sever 模块是http的子模块，它用来定一个虚拟主机  
```                
server {
  # 配置网络监听
  # 一、监听IP地址
  # listen address[:port][default_server][setfib=number][backlog=number][rcvbuf=size][sndbuf=size][deferred][accept_filter=filter][bind][ssl];
  # 二、监听端口
  # listen port [default_server][setfib=number][backlog=number][rcvbuf=size][sndbuf=size][accept_filter=filter][deferred][bind][ipv6only=on|off][ssl];
  # 三、UNIX Domain Socket
  # listen unix:path [default_server][backlog=number][rcvbuf=size][sndbuf=size][accept_filter=filter][deferred][bind][ssl];
  listen       8080; # 监听具体端口上的所有IP连接 等同于 listen *:8080

  # 虚拟主机配置
  # server_name name ...;
  # server_name ~^www\d+\.myserver.com$; regex
  server_name  localhost 192.168.12.10 www.yangyi.com;
  
  # 全局定义，如果都是这一个目录，这样定义最简单。
  # 表示在这整个server虚拟主机内，全部的root web根目录
  root   /Users/yangyi/www;

  index  index.php index.html index.htm; 

  charset utf-8;

  # 设置网址的错误页面
  # error_page code ... [=[response]] uri
  error_page  404              /404.html;
  error_page  500 502 503 504  /50x.html;
  error_page 410 =301          /empty.gif;

  # 黑名单 白名单 访问权限
  # allow address | CIDR | all;
  # deny address | CIDR |all
  # CIDR 例如：202.80.18.23/25 其中/25代表IP地址前25位是网络部分，其余位代表主机部分。
  # 遇到匹配的配置，停止向下所搜相关配置。
  allow 36.110.21.194;
  allow 172.16.128.114;
  allow 10.8.0.0/16;
  deny all;
  # 自定义服务日志
  # access_log path[format[buffer=size]]
  # 默认 access_log logs/access.log combined;
  # 取消 access_log off;
  # main 指向上面的 log_format
  access_log  usr/local/var/log/host.access.log  main;

  error_log  usr/local/var/log/host.error.log  error;
  rewrite_log on;
  ...
}
```
## location 模块
location模块是nginx中用的最多的，也是最重要的模块了，什么负载均衡啊、反向代理啊、虚拟域名啊都与它相关

```
server {
  ...
  # location [ = | ~ | ~* | ^~ ] uri {...}
  # = 标准uri前， 严格与URI匹配
  # ~ 表示uri包含正则，并区分大小写
  # ~* 不区分大小写
  # ^~ 用于标准uri前，要求Nginx服务器找到标识uri和请求字符串匹配度最高的location后，立即使用此location处理请求，不再使用location块中的正则uri和请求字符串做匹配。
  # 图片缓存时间设置
  location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$ {
    expires 10d;
  }
  
  # JS和CSS缓存时间设置
  location ~ .*\.(js|css)?$ {
    expires 1h;
  }
  
  #对 "/" 启用反向代理
  location / {
    proxy_pass http://127.0.0.1:88;
    proxy_redirect off;
    proxy_set_header X-Real-IP $remote_addr;
    
    #后端的Web服务器可以通过X-Forwarded-For获取用户真实IP
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    
    #以下是一些反向代理的配置，可选。
    proxy_set_header Host $host;
    client_max_body_size 10m; #允许客户端请求的最大单文件字节数
    client_body_buffer_size 128k; #缓冲区代理缓冲用户端请求的最大字节数，
    proxy_connect_timeout 90; #nginx跟后端服务器连接超时时间(代理连接超时)
    proxy_send_timeout 90; #后端服务器数据回传时间(代理发送超时)
    proxy_read_timeout 90; #连接成功后，后端服务器响应时间(代理接收超时)
    proxy_buffer_size 4k; #设置代理服务器（nginx）保存用户头信息的缓冲区大小
    proxy_buffers 4 32k; #proxy_buffers缓冲区，网页平均在32k以下的设置
    proxy_busy_buffers_size 64k; #高负荷下缓冲大小（proxy_buffers*2）
    proxy_temp_file_write_size 64k; #设定缓存文件夹大小，大于这个值，将从upstream服务器传
  }
  ...
}
```
## upstream 模块
upstream 模块负债负载均衡模块，通过一个简单的调度算法来实现客户端IP到后端服务器的负载均衡

```
server {
  ...
  upstream blog.ha97.com {
    #upstream的负载均衡，weight是权重，可以根据机器配置定义权重。weigth参数表示权值，权值越高被分配到的几率越大。
    server 192.168.80.121:80 weight=3;
    server 192.168.80.122:80 weight=2;
    server 192.168.80.123:80 weight=3;
  }
  upstream iyangyi.com{
    ip_hash;
    server 192.168.12.1:80;
    server 192.168.12.2:80 down;
    server 192.168.12.3:8080  max_fails=3  fail_timeout=20s;
    server 192.168.12.4:8080;
  }
  ...
```

> ## Nginx的负载均衡模块目前支持4种调度算法:

> - weight 轮询（默认）
> > 每个请求按时间顺序逐一分配到不同的后端服务器，如果后端某台服务器宕机，故障系统被自动剔除，使用户访问不受影响。
weight。指定轮询权值，weight值越大，分配到的访问机率越高，主要用于后端每个服务器性能不均的情况下。

> - ip_hash
> > 每个请求按访问IP的hash结果分配，这样来自同一个IP的访客固定访问一个后端服务器，有效解决了动态网页存在的session共享问题。

> - fair
> > 比上面两个更加智能的负载均衡算法。此种算法可以依据页面大小和加载时间长短智能地进行负载均衡，
也就是根据后端服务器的响应时间来分配请求，响应时间短的优先分配。Nginx本身是不支持fair的，如果需要使用这种调度算法，
必须下载Nginx的upstream_fair模块

> - url_hash
> > 按访问url的hash结果来分配请求，使每个url定向到同一个后端服务器，可以进一步提高后端缓存服务器的效率。Nginx本身是不支持url_hash的，
如果需要使用这种调度算法，必须安装Nginx 的hash软件包

> ## 每个后端服务器在负载均衡调度中的状态

> - down，表示当前的server暂时不参与负载均衡。
> - backup，预留的备份机器。当其他所有的非backup机器出现故障或者忙的时候，才会请求backup机器，因此这台机器的压力最轻。
> - max_fails，允许请求失败的次数，默认为1。当超过最大次数时，返回proxy_next_upstream 模块定义的错误。
> - fail_timeout，在经历了max_fails次失败后，暂停服务的时间。max_fails可以和fail_timeout一起使用。

> ## 当负载调度算法为ip_hash时，后端服务器在负载均衡调度中的状态不能是weight和backup
