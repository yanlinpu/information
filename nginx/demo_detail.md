# Nginx配置文件详解


### nginx.conf

```
user www www;                       # 用户 用户组

# ** 2个4核CPU
worker_processes 8；    
# ** 为每个进程分配cpu，上例中将8个进程分配到8个cpu，当然可以写多个，或者将一个进程分配到多个cpu。 
worker_cpu_affinity 00000001 00000010 00000100 00001000 00010000 00100000 01000000 10000000;
error_log logs/error.log;           # 错误日志
pid logs/nginx.pid;                 # pid文件位置

# ** nginx能打开文件的最大句柄数，最好与ulimit -n的值保持一致，使用ulimit -SHn 65535 设置
worker_rlimit_nofile 65535; 
events {
    use epoll;                      # 使用epoll的I/O模型
    connections 20000;              # 每个进程允许的最多连接数

    # ** 该值受系统进程最大打开文件数限制，需要使用命令ulimit -n 查看当前设置
    worker_connections 65535;
    multi_accept on;
    # maxclients=65535*2
}

http {
    include conf/mime.types;
    default_type  application/octet-stream;
    include    proxy.conf;
    include    fastcgi.conf;
    # proxy cache
    proxy_cache_path /myweb/server/proxycache levels=1:2 keys_zone=MYPROXYCACHE:10m max_size=2m inactive=5m loader_sleep=1m;
    proxy_temp_path /myweb/server/tmp;

    # 不能带单位！配置个主机时必须设置该值，否则无法运行Nginx或测试时不通过。
    # 该设置与server_names_hash_max_size 共同控制保存服务器名的HASH表，hash_bucket_size总是等于hash表的大小，并且是一路处理器缓存大小的倍数。
    # 若hash_bucket_size等于一路处理器缓存的大小，那么在查找键的时候，最坏的情况下在内存中查找的次数为2。
    # 第一次是确定存储单元的地址，第二次是在存储单元中查找键值。
    # 若报出hash max size 或 hash bucket size的提示，则我们需要增加server_names_hash_max_size的值。
    # ** 为了高速寻找到响应server name 能力，Nginx使用列表来存储。设置每个散列桶占用内存大小。 32|64|128
    server_names_hash_bucket_size 128; 

    # 客户端请求头部的缓冲区大小，根据系统分页大小设置，`$ getconf PAGESIZE`   
    client_header_buffer_size 32k;   

    # 4为个数，32k为大小，默认是4k。申请4个32k。
    # 当http 的URI太长或者request header过大时会报414 Request URI too large或400 bad request，
    # 这很有可能是cookie中写入的值太大造成的，因为header中的其他参数的size一般比较固定，只有cookie可能被写入较大的数据，
    # 这时可以调大上述两个值，相应的浏览器中cookie的字节数上限会增大。
    large_client_header_buffers 4 32k;  

    # underscores_in_headers on; 
    
    # 提高文件传输性能
    sendfile on; 
    tcp_nopush on;                  # 打开linux下TCP_CORK，sendfile打开时才有效，作减少报文段的数量之用
    keepalive_timeout 60; 
    tcp_nodelay on;                 # 打开TCP_NODELAY在包含了keepalive才有效

    # fastcgi 配置
    # fastcgi是实现php的解析程序
    # fastcgi可以让HTTP服务器专一地处理静态请求或者将动态脚本服务器的结果返回给客户端
    fastcgi_connect_timeout 300;    # 指定连接到后端FastCGI的超时时间
    fastcgi_send_timeout 300;       # 向FastCGI传送请求的超时时间，这个值是指已经完成两次握手后向FastCGI传送请求的超时时间。
    fastcgi_read_timeout 300;       # 接收FastCGI应答的超时时间，这个值是指已经完成两次握手后接收FastCGI应答的超时时间。
    fastcgi_buffer_size 64k;        # 这里可以设置为fastcgi_buffers指令指定的缓冲区大小
    fastcgi_buffers 4 64k;          # 指定本地需要用多少和多大的缓冲区来缓冲FastCGI的应答
    fastcgi_busy_buffers_size 128k; # 建议为fastcgi_buffer_size的两倍
    fastcgi_temp_file_write_size 256k;   # 在写入fastcgi_temp_path时将用多大的数据块，默认值是fastcgi_buffer_size的两倍，设置上述数值设置太小时若负载上来时可能报 502 Bad Gateway
    #   fastcgi_cache dingtm            # 开启FastCGI缓存并且为其制定一个名称，有效降低CPU负载，并且防止502错误
    #   fastcgi_cache_valid 200 302 1h; # 指定应答代码缓存时间为1小时
    #   fastcgi_cache_valid 301 1d;     # 1天
    #   fastcgi_cache_valid any 1m;     # 其它为1分钟
    #   fastcgi_cache_min_uses 1;       # 缓存在fastcgi_cache_path指令


    # gzip 配置
    gzip on; 
    gzip_min_length  1k;        # 默认20，建议1k
    gzip_buffers     4 16k;     # 建议size的值 `$ getconf PAGESIZE`
    gzip_http_version 1.1;
    gzip_comp_level 2;
    gzip_types     text/plain application/javascript application/x-javascript text/javascript text/css application/xml;
    gzip_vary on;               #  开启后的效果是在响应头部添加了`Accept-Encoding: gzip`
    gzip_proxied   expired no-cache no-store private auth;
    gzip_disable   "MSIE [1-6]\.";

    server_tokens off;              # 关闭错误时Nginx版本显示
    # 日志的格式
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
    # access_log logs/access.log main;
    access_log off;
    
    # 配置error_page
    server {
        listen       80;
        server_name  10.*;
        access_log off;
        root /www/site/default;
        index  index.html index.htm;
        error_page  404              /404.html;
        error_page  500 502 503 504  /50x.html;
        location ~ /\.ht {                                       
            deny  all;
        }
    }

    # fastcgi的例子
    # Connecting NGINX to PHP FPM
    # fastcgi是实现php的解析程序
    server {
        listen       80; 
        server_name  cytools.domain.com 10.0.0.1;
        root /www/site/domain;
        index  index.html index.htm index.php;
        access_log  /www/log/nginx/access.log  main;
        location ~ .*\.(php|php5)?$
        {    
            if ( $fastcgi_script_name ~ \..*\/.*php ) { 
                return 403;
            }   
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            # fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
            include        fastcgi_params;
        }   
    }   


    # 这个是反向代理的例子
    server {
        listen 80;
        server_name tgcs.demo.com 10.0.0.2;
        access_log /www/log/nginx/tgcs.demo.com.log main;

        # allow ***.***.***.***;
        # allow ***.***.***.***;
        # allow ***.***.***.***;
        # deny all;

        location ~ ^/(fonts|js|html|css|images|img|lib|video|plugins)/ {
            root /www/node/cs_web/public/;
            # 过期30天，静态文件不怎么更新，过期可以设大一点，如果频繁更新，则可以设置得小一点。
            # expires 30d;
        }

        location /framework/ {
            proxy_pass http://127.0.0.1:9001;
        }

        location / {
            proxy_set_header X-Real-IP $remote_addr;
            proxy_pass http://localhost:8212/;
        }

        location /cert/ {
            proxy_set_header X-Real-IP $remote_addr;
            proxy_pass http://localhost:8213/;
        }
    }

    # upstream的负载均衡，weight是权重，可以根据机器配置定义权重。据说nginx可以根据后台响应时间调整。后台需要多个web服务器。
    upstream backend {
        server 192.168.1.2:80 weight=5;
        server 192.168.1.3:80 weight=2;
        server 192.168.1.4:80;              # 默认weight=1
    }

    server {
        listen 80;
        server_name www.myweb.name 10.0.0.3;
        index index.html index.htm;
        location / {
            proxy_pass http://backend;
            proxy_set_header Host $host;
        }
    }

    # proxy_cache 例子
    server {
        location / {
            proxy_pass http://www.myweb.name/;
            proxy_cache MYPROXYCACHE;
            proxy_cache_valid 200 302 1h;
            proxy_cache_valid 301 1d;
            proxy_cache any 1m;
        }
    }
    
    include vhost/*.conf;               # 其他虚拟主机（server)配置
    include vhost/complain/*.conf;      # 其他虚拟主机（server)配置
} 

```


### proxy.conf

```
proxy_redirect          off;
proxy_set_header        Host            $host;
proxy_set_header        X-Real-IP       $remote_addr;
proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
# HTTP请求的BODY最大限制值，若超出此值，报413 Request Entity Too Large 
client_max_body_size    50m; 
proxy_connect_timeout   90;
proxy_send_timeout      90;
proxy_read_timeout      90;
proxy_buffer_size       16k;            # 设置代理服务器（nginx）保存用户头信息的缓冲区大小
proxy_buffers 4 64k;                    # proxy_buffers缓冲区，网页平均在64k以下的设置
proxy_busy_buffers_size 128k;           # 高负荷下缓冲大小（proxy_buffers*2）
proxy_temp_file_write_size 128k;        # 设定缓存文件夹大小，大于这个值，将从upstream服务器传
client_body_buffer_size 128k;
```

### fastcgi.conf

```
fastcgi_param  SCRIPT_FILENAME    $document_root$fastcgi_script_name;
fastcgi_param  QUERY_STRING       $query_string;
fastcgi_param  REQUEST_METHOD     $request_method;
fastcgi_param  CONTENT_TYPE       $content_type;
fastcgi_param  CONTENT_LENGTH     $content_length;
fastcgi_param  SCRIPT_NAME        $fastcgi_script_name;
fastcgi_param  REQUEST_URI        $request_uri;
fastcgi_param  DOCUMENT_URI       $document_uri;
fastcgi_param  DOCUMENT_ROOT      $document_root;
fastcgi_param  SERVER_PROTOCOL    $server_protocol;
fastcgi_param  GATEWAY_INTERFACE  CGI/1.1;
fastcgi_param  SERVER_SOFTWARE    nginx/$nginx_version;
fastcgi_param  REMOTE_ADDR        $remote_addr;
fastcgi_param  REMOTE_PORT        $remote_port;
fastcgi_param  SERVER_ADDR        $server_addr;
fastcgi_param  SERVER_PORT        $server_port;
fastcgi_param  SERVER_NAME        $server_name;

fastcgi_index  index.php;

fastcgi_param  REDIRECT_STATUS    200;
```


### mime.types

```
types {
    text/html                             html htm shtml;
    text/css                              css;
    text/xml                              xml rss;
    image/gif                             gif;
    image/jpeg                            jpeg jpg;
    application/x-javascript              js;
    text/plain                            txt;
    text/x-component                      htc;
    text/mathml                           mml;
    image/png                             png;
    image/x-icon                          ico;
    image/x-jng                           jng;
    image/vnd.wap.wbmp                    wbmp;
    application/java-archive              jar war ear;
    application/mac-binhex40              hqx;
    application/pdf                       pdf;
    application/x-cocoa                   cco;
    application/x-java-archive-diff       jardiff;
    application/x-java-jnlp-file          jnlp;
    application/x-makeself                run;
    application/x-perl                    pl pm;
    application/x-pilot                   prc pdb;
    application/x-rar-compressed          rar;
    application/x-redhat-package-manager  rpm;
    application/x-sea                     sea;
    application/x-shockwave-flash         swf;
    application/x-stuffit                 sit;
    application/x-tcl                     tcl tk;
    application/x-x509-ca-cert            der pem crt;
    application/x-xpinstall               xpi;
    application/zip                       zip;
    application/octet-stream              deb;
    application/octet-stream              bin exe dll;
    application/octet-stream              dmg;
    application/octet-stream              eot;
    application/octet-stream              iso img;
    application/octet-stream              msi msp msm;
    audio/mpeg                            mp3;
    audio/x-realaudio                     ra;
    video/mpeg                            mpeg mpg;
    video/quicktime                       mov;
    video/x-flv                           flv;
    video/x-msvideo                       avi;
    video/x-ms-wmv                        wmv;
    video/x-ms-asf                        asx asf;
    video/x-mng                           mng;
}
```


### fastcgi_params

```
fastcgi_param   QUERY_STRING            $query_string;
fastcgi_param   REQUEST_METHOD          $request_method;
fastcgi_param   CONTENT_TYPE            $content_type;
fastcgi_param   CONTENT_LENGTH          $content_length;

fastcgi_param   SCRIPT_FILENAME         $document_root$fastcgi_script_name;
fastcgi_param   SCRIPT_NAME             $fastcgi_script_name;
fastcgi_param   PATH_INFO               $fastcgi_path_info;
fastcgi_param       PATH_TRANSLATED         $document_root$fastcgi_path_info;
fastcgi_param   REQUEST_URI             $request_uri;
fastcgi_param   DOCUMENT_URI            $document_uri;
fastcgi_param   DOCUMENT_ROOT           $document_root;
fastcgi_param   SERVER_PROTOCOL         $server_protocol;

fastcgi_param   GATEWAY_INTERFACE       CGI/1.1;
fastcgi_param   SERVER_SOFTWARE         nginx/$nginx_version;

fastcgi_param   REMOTE_ADDR             $remote_addr;
fastcgi_param   REMOTE_PORT             $remote_port;
fastcgi_param   SERVER_ADDR             $server_addr;
fastcgi_param   SERVER_PORT             $server_port;
fastcgi_param   SERVER_NAME             $server_name;

fastcgi_param   HTTPS                   $https;

# PHP only, required if PHP was built with --enable-force-cgi-redirect
fastcgi_param   REDIRECT_STATUS         200;
```

-------------

# fastcgi 输出结果

```
array (
    'USER' => 'www-data',
    'HOME' => '/var/www',
    'FCGI_ROLE' => 'RESPONDER',
    'QUERY_STRING' => 'v=1',
    'REQUEST_METHOD' => 'GET',
    'CONTENT_TYPE' => '',
    'CONTENT_LENGTH' => '',
    'SCRIPT_FILENAME' => '/var/www/test.php',
    'SCRIPT_NAME' => '/test.php',
    'PATH_INFO' => '/foo/bar.php',
    'REQUEST_URI' => '/test.php/foo/bar.php?v=1',
    'DOCUMENT_URI' => '/test.php/foo/bar.php',
    'DOCUMENT_ROOT' => '/var/www',
    'SERVER_PROTOCOL' => 'HTTP/1.1',
    'GATEWAY_INTERFACE' => 'CGI/1.1',
    'SERVER_SOFTWARE' => 'nginx/1.4.0',
    'REMOTE_ADDR' => '192.168.56.1',
    'REMOTE_PORT' => '44644',
    'SERVER_ADDR' => '192.168.56.3',
    'SERVER_PORT' => '80',
    'SERVER_NAME' => '',
    'HTTPS' => '',
    'REDIRECT_STATUS' => '200',
    'HTTP_HOST' => 'lemp.test',
    'HTTP_USER_AGENT' => 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0',
    'HTTP_ACCEPT' => 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'HTTP_ACCEPT_LANGUAGE' => 'en-US,en;q=0.5',
    'HTTP_ACCEPT_ENCODING' => 'gzip, deflate',
    'HTTP_CONNECTION' => 'keep-alive',
    'PHP_SELF' => '/test.php/foo/bar.php',
    'REQUEST_TIME' => 1367829847,
)
```