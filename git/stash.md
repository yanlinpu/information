```
SYNOPSIS
       git stash list [<options>]
       git stash show [<stash>]
       git stash drop [-q|--quiet] [<stash>]
       git stash ( pop | apply ) [--index] [-q|--quiet] [<stash>]
       git stash branch <branchname> [<stash>]
       git stash [save [-p|--patch] [-k|--[no-]keep-index] [-q|--quiet]
                    [-u|--include-untracked] [-a|--all] [<message>]]
       git stash clear
       git stash create [<message>]
       git stash store [-m|--message <message>] [-q|--quiet] <commit>
```

1. 简单的一次存取

```
$ git stash
$ git stash pop
```

2. 创建带有message的 并取指定暂存

```
$ git checkout -b develop
$ echo -e  "\ndevelop stash1" >> README.md
# 创建一条stash message为develop stash1
$ git stash save "develop stash1"
$ git stash list
      # stash@{0}: On develop: develop stash1
$ git checkout master
$ echo -e  "\nmaster stash1" >> README.md
$ git stash save "master stash1"
$ git stash list
      # stash@{0}: On master: master stash1
      # stash@{1}: On develop: develop stash1
$ echo "new file" >> new_file.md
$ git stash -u
$ echo "new file2" >> new_file2.md
$ git stash save -u "new_file2"
$ git stash list
      # stash@{0}: On master: new_file2
      # stash@{1}: WIP on master: 39eea1e del a
      # stash@{2}: On master: master stash1
      # stash@{3}: On develop: develop stash1
$ git stash show stash@{3}
      # README.md | 3 ++-
      # 1 file changed, 2 insertions(+), 1 deletion(-)
# git stash show -p 参数显示diffs
$ git stash show -p stash@{3}
      # diff --git a/README.md b/README.md
      # index 7a64a8d..da67740 100644
      # --- a/README.md
      # +++ b/README.md
      # @@ -1 +1,2 @@
      # -Hello yanlp_test1
      # \ No newline at end of file
      # +Hello yanlp_test1
      # +develop stash1
# 应用指定stash
$ git stash apply stash@{3}
$ cat README.md
      # Hello yanlp_test1
      # develop stash1
# 删除最新的一个stash
$ git stash drop
# 删除指定stash
$ git stash drop stash@{2}
# 清空所有stash
$ git stash clear
```
