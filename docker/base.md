## 基础命令
```
docker pull nginx:1.15
docker run -it --rm ubuntu:18.04 bash
docker image ls --format="table {{.ID}}\t{{.Repository}}\t{{.Tag}}\t{{.Size}}"
docker image rm $(docker image ls -q redis)
docker run --name webserver -d -p 8000:80 nginx
docker exec -ti webserver bash
docker commit --author='yanlp' --message='update nginx index.html' webserver nginx:v2
```

## Dockerfile定制镜像
- `FROM` 指定基础镜像

    定制镜像，那一定是以一个镜像为基础，在其上进行定制。而 FROM 就是指定基础镜像，因此一个 Dockerfile 中 FROM 是必备的指令，并且必须是第一条指令。

    除了选择现有镜像为基础镜像外，Docker 还存在一个特殊的镜像，名为 scratch。这个镜像是虚拟的概念，并不实际存在，它表示一个空白的镜像。`FROM scratch`
- `RUN` 执行命令

    `RUN`指令在定制镜像时是最常用的指令之一。其格式有两种：
    
    - `shell` 格式 `RUN <命令>`
    - `exec`  格式 `RUN ["可执行文件", "参数1", "参数2"]`

    Dockerfile 中每一个指令都会建立一层，RUN 也不例外。每一个 RUN 的行为，就和手工建立镜像的过程一样：新建立一层，在其上执行这些命令，执行结束后，commit 这一层的修改，构成新的镜像。使用 `&&` 将各个所需命令串联起来，简化为了层数。
- `COPY` 复制文件

    格式：
    - `COPY [--chown=<user>:<group>] <源路径>... <目标路径>`
    - `COPY [--chown=<user>:<group>] ["<源路径1>",... "<目标路径>"]`

    ```
    COPY hom* /mydir/
    COPY hom?.txt /mydir/
    # --chown=<user>:<group> 选项来改变文件的所属用户及所属组。
    COPY --chown=55:mygroup files* /mydir/
    COPY --chown=bin files* /mydir/
    ```
- `ADD` 更高级的复制文件

    尽可能的使用 COPY，因为 COPY 的语义很明确，就是复制文件而已，而 ADD 则包含了更复杂的功能，其行为也不一定很清晰。最适合使用 ADD 的场合，就是所提及的需要自动解压缩的场合。

    另外需要注意的是，ADD 指令会令镜像构建缓存失效，从而可能会令镜像构建变得比较缓慢。

- `CMD` 容器启动命令

    CMD 指令就是用于指定默认的容器主进程的启动命令的。格式:
    - `shell` 格式 `CMD <命令>`
    - `exec`  格式 `CMD ["可执行文件", "参数1", "参数2"]`
    - 参数列表格式：`CMD ["参数1", "参数2"...]`。在指定了 ENTRYPOINT 指令后，用 CMD 指定具体的参数。

    `CMD echo $HOME` 在实际执行中，会将其变更为： `CMD [ "sh", "-c", "echo $HOME" ]`

    `CMD service nginx start` 会被理解为 `CMD [ "sh", "-c", "service nginx start"]`，因此主进程实际上是 sh。那么当 service nginx start 命令结束后，sh 也就结束了，sh 作为主进程退出了，自然就会令容器退出。 正确的做法是直接执行 nginx 可执行文件，并且要求以前台形式运行。比如：`CMD ["nginx", "-g", "daemon off;"]`
- `<ENTRYPOINT> "<CMD>"` 入口点

    - 让镜像变成像命令一样使用
        
        `CMD [ "curl", "-s", "https://ip.cn" ]` 跟`-i`参数需要执行`docker run myip curl -s https://ip.cn -i`

        `ENTRYPOINT [ "curl", "-s", "https://ip.cn" ]`直接`docker run myip -i`

        这是因为当存在 ENTRYPOINT 后，CMD 的内容将会作为参数传给 ENTRYPOINT，而这里 -i 就是新的 CMD，因此会作为参数传给 curl，从而达到了我们预期的效果。
    - 应用运行前的准备工作

        `ENTRYPOINT ["docker-entrypoint.sh"]`

        ```
        #!/bin/sh
        ...
        # allow the container to be started with `--user`
        if [ "$1" = 'redis-server' -a "$(id -u)" = '0' ]; then
            chown -R redis .
            exec su-exec redis "$0" "$@"
        fi

        exec "$@"
        ```

        `docker run -it redis id` => `uid=0(root) gid=0(root) groups=0(root)`
- `ENV` 设置环境变量

    - `ENV <key> <value>`
    - `ENV <key1>=<value1> <key2>=<value2>...`

- `ARG` 构建参数

    `ARG <参数名>[=<默认值>]`

    构建参数和 ENV 的效果一样，都是设置环境变量。所不同的是，ARG 所设置的构建环境的环境变量，在将来容器运行时是不会存在这些环境变量的。

    `docker build` 中用 `--build-arg <参数名>=<值>` 来覆盖。

- `VOLUME` 定义匿名卷

    - `VOLUME ["<路径1>", "<路径2>"...]`
    - `VOLUME <路径>`

    `VOLUME /data` 这里的 /data 目录就会在运行时自动挂载为匿名卷，任何向 /data 中写入的信息都不会记录进容器存储层，从而保证了容器存储层的无状态化。当然，运行时可以覆盖这个挂载设置。比如：`docker run -d -v mydata:/data xxxx`

- `EXPOSE` 声明端口

    `EXPOSE <端口1> [<端口2>...]`

    要将 `EXPOSE` 和在运行时使用 `-p <宿主端口>:<容器端口>` 区分开来。`-p`，是映射宿主端口和容器端口，换句话说，就是将容器的对应端口服务公开给外界访问，而 EXPOSE 仅仅是声明容器打算使用什么端口而已，并不会自动在宿主进行端口映射
- `WORKDIR` 指定工作目录

    `WORKDIR <工作目录路径>`

- `USER` 指定当前用户

    `USER <用户名>[:<用户组>]`

    ```
    RUN groupadd -r redis && useradd -r -g redis redis
    USER redis
    RUN [ "redis-server" ]
    ```

    如果以 root 执行的脚本，在执行期间希望改变身份，比如希望以某个已经建立好的用户来运行某个服务进程，不要使用 su 或者 sudo，这些都需要比较麻烦的配置，而且在 TTY 缺失的环境下经常出错。建议使用 gosu。

    ```
    # 建立 redis 用户，并使用 gosu 换另一个用户执行命令
    RUN groupadd -r redis && useradd -r -g redis redis
    # 下载 gosu
    RUN wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/1.7/gosu-amd64" \
        && chmod +x /usr/local/bin/gosu \
        && gosu nobody true
    # 设置 CMD，并以另外的用户执行
    CMD [ "exec", "gosu", "redis", "redis-server" ]
    ```
- `HEALTHCHECK` 健康检查

    - `HEALTHCHECK [选项] CMD <命令>`：设置检查容器健康状况的命令
        - `--interval=<间隔>`：两次健康检查的间隔，默认为 30 秒；
        - `--timeout=<时长>`：健康检查命令运行超时时间，如果超过这个时间，本次健康检查就被视为失败，默认 30 秒；
        - `--retries=<次数>`：当连续失败指定次数后，则将容器状态视为 unhealthy，默认 3 次。
    - `HEALTHCHECK NONE`：如果基础镜像有健康检查指令，使用这行可以屏蔽掉其健康检查指令

    为了帮助排障，健康检查命令的输出（包括 stdout 以及 stderr）都会被存储于健康状态里，可以用 docker inspect 来查看。

    ```
    $ docker inspect --format '{{json .State.Health}}' web | python -m json.tool
    {
        "FailingStreak": 0,
        "Log": [
            {
                "End": "2016-11-25T14:35:37.940957051Z",
                "ExitCode": 0,
                "Output": "<!DOCTYPE html>\n<html>\n<head>\n<title>Welcome to nginx!</title>\n<style>\n    body {\n        width: 35em;\n        margin: 0 auto;\n        font-family: Tahoma, Verdana, Arial, sans-serif;\n    }\n</style>\n</head>\n<body>\n<h1>Welcome to nginx!</h1>\n<p>If you see this page, the nginx web server is successfully installed and\nworking. Further configuration is required.</p>\n\n<p>For online documentation and support please refer to\n<a href=\"http://nginx.org/\">nginx.org</a>.<br/>\nCommercial support is available at\n<a href=\"http://nginx.com/\">nginx.com</a>.</p>\n\n<p><em>Thank you for using nginx.</em></p>\n</body>\n</html>\n",
                "Start": "2016-11-25T14:35:37.780192565Z"
            }
        ],
        "Status": "healthy"
    }
    ```
- `ONBUILD` 为他人做嫁衣裳


- `build`构建镜像

    - `docker build [选项] <上下文路径/URL/->`eg.`docker build -t nginx:v3 .`
    - 直接用 Git repo 进行构建`docker build https://github.com/twang2218/gitlab-ce-zh.git#:11.1`
    - 用给定的 tar 压缩包构建`docker build http://server/context.tar.gz`


```
# 
FROM nginx
RUN echo '<h1>Hello, Docker!</h1>' > /usr/share/nginx/html/index.html
```
## 注意： 

- docker commit 命令除了学习之外，还有一些特殊的应用场合，比如被入侵后保存现场等。但是，不要使用 docker commit 定制镜像，定制镜像应该使用 Dockerfile 来完成。
