## /etc/nginx/nginx.conf

```
user git;                                                                                                                                                                                                    
worker_processes 4;
pid /run/nginx.pid;

events {
  worker_connections 768;
  # multi_accept on;
}

http {

  ##
  # Basic Settings
  ##

  sendfile on;
  tcp_nopush on;
  tcp_nodelay on;
  keepalive_timeout 65;
  types_hash_max_size 2048;
  # server_tokens off;
  # server_names_hash_bucket_size 64;
  # server_name_in_redirect off;

  include /etc/nginx/mime.types;
  default_type application/octet-stream;

  ##
  # Logging Settings
  ##

  access_log /var/log/nginx/access.log;
  error_log /var/log/nginx/error.log;

  ##
  # Gzip Settings
  ##

  gzip on;
  gzip_disable "msie6";

  # gzip_vary on;
  # gzip_proxied any;
  # gzip_comp_level 6;
  # gzip_buffers 16 8k;
  # gzip_http_version 1.1;
  # gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;
  # upload_file size
  client_max_body_size 100m;                                                                                                                                                                                 

  server {
    listen          80;
    server_name     test.ylp.net;
    index           index.html;
#   access_log      logs/uc.access.log  main;
    error_page  404  /404.html;
    location  = /404.html {
      root   html;
    }
    error_page 400 500 502 503 504  /500.html;
    location = /500.html {
      root    html;
    }
    location / {
      proxy_pass      http://127.0.0.1:3000;
#     include proxy.conf;
    }

    location ~ \.php$ {
      root /home/git/labhub/public/emd/php;
      index index.php index.html index.shtml;
      fastcgi_pass 127.0.0.1:7000;
      fastcgi_index index.php;
      fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
      include fastcgi_params;
    }
  }
  
  server {
    listen  80;
    server_name rnd-sdnbeta.ylp.com;
    index index.html;
    error_page  404 /404.html;
    location = /404.html {
      root  html;
    }
    error_page 400 500 502 503 504  /500.html;
    location = /500.html {
      root  html;
    }
    location / {
      proxy_pass  http://127.0.0.1:3456;
    }
  }

  include /etc/nginx/conf.d/*.conf;
  include /etc/nginx/sites-enabled/*;
}

```
