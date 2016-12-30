## 创建新的空分支

```
$ git symbolic-ref HEAD refs/heads/init
$ git branch
# => master
$ git status
# => 位于分支 init
$ rm .git/index
$ git clean -fdx
# => 正删除 README.md
# <do work>
# git add your files
# git commit -m 'Initial commit'
$ git branch
# => init
```
