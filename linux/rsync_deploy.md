# 推送脚本

## 读取ini配置文件

[bash_ini_parser from github](https://github.com/rudimeier/bash_ini_parser)


- [/root/development/read_ini.sh](https://github.com/rudimeier/bash_ini_parser/blob/master/read_ini.sh)
- /root/development/config.ini

```
[nginx1]
to=192.168.1.5
from=192.168.1.1
path=/www/app/nginx/conf/vhost/
;ignore=

[complain]
to=192.168.1.5
from=192.168.1.1
path=/www/node/complain/

[dashboard]
to=192.168.1.5
from=192.168.1.1
path=/www/node/dashboard/

[agency]
to=192.168.1.5
from=192.168.1.1
path=/www/node/agency/
;...
```

- /root/development/deploy.ini

```
conf=./config.ini
. ./read_ini.sh
read_ini $conf
#echo "the value of nginx from: ${INI__nginx1__from}"
#echo "list of all ini vars: ${INI__ALL_VARS}"
#echo "number of sections: ${INI__NUMSECTIONS}"
#echo "all sections: ${INI__ALL_SECTIONS}"
function Usage(){
    echo "./deploy.sh   option service_name"
    echo "sync          sync the code to remote server"
    echo "restart       restart the service on remote server"
    echo "list          list the all service"
    echo "logs          show service log"
}

function sync(){
    echo "sync file";
    if [ ! -d ./codes ]; then 
        mkdir codes/
    fi
    # echo $0
    codevar="INI__${1}__path"
    fromvar="INI__${1}__from"
    tovar="INI__${1}__to"
    # echo "${tovar}"

    codepath=${!codevar}
    to=${!tovar}
    from=${!fromvar}
    # echo "${to}"
    cpath=`pwd`
    tmppath="${cpath}/codes$codepath"
    echo "sync file from $from  to local"
    echo "$from:$codepath";
    #create local path
    if [ ! -d $tmppath ]; then
        mkdir -p $tmppath
    fi

    #sync file to local
    cd $tmppath;
    git clean -fd;
    cd  $codepath;
    git clean -fd;
    echo "rsync -avP --exclude=tmp $from:$codepath $tmppath" 
    rsync -avP --exclude=tmp $from:$codepath $tmppath
    cd $tmppath;
    #sync file to remote
    echo "ssh $to \"su -l www -c \" mkdir -p $codepath  \"\""
    ssh $to "su -l www -c \" mkdir -p $codepath  \""
    echo "sync file to remote $to"
    echo "rsync -avP $tmppath $to:$codepath"
    rsync -avP $tmppath $to:$codepath
}
function logs(){
    tovar="INI__${1}__to"
    to=${!tovar}
    ssh $to "su -l www -c \"pm2 logs /www/node/${1}/config/pm2/development.json\" "
}

function restart(){
    tovar="INI__${1}__to"
    to=${!tovar}
    ssh $to "su -l www -c \"pm2 restart /www/node/${1}/config/pm2/development.json\" "
}

function list(){
    echo "list service ${1}";
}

action=$1

case $action in
    sync)
        sync $2;
        ;;
    restart)
        restart $2;
        ;;
    logs)
        logs $2;
        ;;
    *)
        Usage;
        ;;
esac
```

- /root/development/one_key_deployment.sh

```
p=`pwd`;                                                                                              
echo "$p";
function deploy(){
    cd $p; 
    source deploy.sh sync dashboard
    source deploy.sh restart dashboard
    cd $p;
    source deploy.sh sync complain
    source deploy.sh restart complain
    cd $p;
    source deploy.sh sync agency
    source deploy.sh restart agency
    # ...
}
deploy;
```