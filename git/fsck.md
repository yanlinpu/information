## branch stash 删除恢复

```
$ git fsck --lost-found
# => dangling commit 674c0618ca7d0c251902f0953987ff71860cb067
$ git merge 674c0618ca7d0c251902f0953987ff71860cb067
$ git rebase 674c0618ca7d0c251902f0953987ff71860cb067
```

git中把commit删了后，并不是真正的删除，而是变成了悬空对象（dangling commit）。我们只要把把这悬空对象（dangling commit）找出来，用git rebase也好，
用git merge也行就能把它们给恢复。删除的分支名恢复不了，只是找回commit号。
