# -*- encoding: utf-8 -*-
#!/usr/bin/env python
import numpy as np

# [3, 34, 4, 12, 5, 2] 求n个数字相加能否等于给定数字9   假设所有数字>0 返回True or False

# 递归
def recSubset(arr, i, s):
    if s==0:
        return True
    elif i==0:
        return arr[0]==s
    elif arr[i]>s:
        return recSubset(arr, i-1, s)
    else:
        A = recSubset(arr, i-1, s-arr[i])
        B = recSubset(arr, i-1, s)
        return A or B

arr = [3, 34, 4, 12, 5, 2]
# print(recSubset(arr, len(arr)-1, 9))

# 动态规划（二维数组）
def dpSubset(arr, S):
    subset = np.zeros((len(arr), S+1), dtype=bool)
    subset[:, 0] = True
    subset[0, :] = False
    if arr[0]<S:
        subset[0, arr[0]] = True
    for i in range(1, len(arr)):
        for s in range(1, S+1):
            if arr[i] > s:
                subset[i, s] = subset[i-1, s]
            else:
                A = subset[i-1, s-arr[i]]
                B = subset[i-1, s]
                subset[i, s] = A or B
    print(subset)
    r, c = subset.shape
    return subset[r-1, c-1]
arr = [3, 34, 4, 12, 5, 2]
print(dpSubset(arr, 9))