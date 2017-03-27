## 交互式rebase `$ rebase -i, --interactive`

```
$ git rebase -i HEAD~5
pick fc62e55 added file_size
pick 9824bf4 fixed little thing
pick 21d80a5 added number to log
pick 76b9da6 added the apply command
pick c264051 Revert "added file_size" - not implemented correctly

# Rebase d30af05..08ef411 onto d30af05 (2 command(s))
#
# Commands:
# p, pick = use commit
# r, reword = use commit, but edit the commit message                     ========>修改commit信息 pick->reword
# e, edit = use commit, but stop for amending
# s, squash = use commit, but meld into previous commit                   =========>将下面的squash提交，合并到前一个
# f, fixup = like "squash", but discard this commit's log message         
# x, exec = run command (the rest of the line) using shell
#
# These lines can be re-ordered; they are executed from top to bottom.
#
# If you remove a line here THAT COMMIT WILL BE LOST.
#
# However, if you remove everything, the rebase will be aborted.
#
# Note that empty commits are commented out
```

### 简单操作

- 删除某个commit c264051  
      简单的删除c264051所在行
- commit 互换fc62e55 9824bf4  
      fc62e55 9824bf4上下顺序互换



### 提交原则：（蒋鑫[做一个有品位的程序员](http://www.worldhello.net/2015/12/23/taste-of-a-programmer.html)）
#### 1.提交做小（拆分历史某个提交）  

- 不拆分file

```
$ git rebase -i HEAD~5 #如上
#修改21d80a5的action为edit
#edit   21d80a5 added number to log
$ wq
# 假设提交21d80a5修改了两个文件，file1和file2，你想把这两个修改放到不同的提交里
$ git reset HEAD^
$ git add file1
$ git commit 'first part of split commit'
$ git add file2
$ git commit 'second part of split commit'
$ git rebase --continue
```

- 拆分某个file

  - 松耦合
  
    [git add --interactive "Your edited hunk does not apply"](http://stackoverflow.com/questions/3268596/git-add-interactive-your-edited-hunk-does-not-apply)
    
    [diffs Chunk Header](https://www.git-tower.com/learn/git/ebook/cn/command-line/advanced-topics/diffs)

    ``` 
      $ git rebase -i HEAD~5
      $ git reset HEAD^
      $ git add -p
      # 此处显示补丁块（hunk），用户根据提示信息，输入自己的选择
      # 输入 y，此块儿补丁要提交
      # 输入 n，此块儿补丁不提交
      # 输入 s，尝试将此块儿补丁细分
      # 输入 e，打开编辑器对此块儿补丁进行再次编辑
      $ ----> s
      $ ----> e
      $ git commit -e -C HEAD@{1}
      $ git add -u
      $ git commit -m 'second part of split commit'
      $ git rebase --continue 
    ``` 
  - 紧耦合

    ```
      $ git rebase -i HEAD~5
    ```

    如果要拆分的提交，不同的实现逻辑耦合在一起，难以通过补丁块拣选（git add -p）的方式修改提交，怎么办？这时可以 直接编辑文件，删除要剥离出此次提交的修改，然后执行
    
    ```
      $ git commit --amend
    ```

    接下来执行下面的命令，还原出原有的文件修改，然后再次提交。如下

    ```
      $ git checkout HEAD@{1} -- .
      $ git commit
    ``` 
   
#### 2.	提交做对

```
# 发现历史提交 54321 中包含错误，直接在当前工作区中针对这个错误进行修改
$ git add README
$ git commit --fixup 54321
$ git rebase -i --autosquash 54321^
$ git push origin master -f
```

#### 3. 提交做好

```
$ git commit -se

#style
  1 theme
  2 
  3 1.What——要解决什么问题？什么情况下会发生？  
  4 2.How ——怎么样解决这个问题  
  5 3.Why ——为什么这样解决是合理的，比其他解决方法更好 
  6 
  7 Signed-off-by: yanlinpu <yanlinpu@huawei.com>

```

### 提交之后pull

`$ git reset origin/master --hard`
### 减少merge提交

`$ git pull --rebase origin master` || `$ git rebase origin/master` || `$ git rebase -i origin/master`
