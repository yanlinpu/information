# -*- encoding: utf-8 -*-
#!/usr/bin/env python
import numpy as np

# 从一堆数字选择不相邻数字 求最大值  [4,1,1,9,1] --> 4+9=13
'''
构造问题所对应的过程。

arr = [1,2,4,1,7,8,3]
选arr[6] and 不选arr[6]两种情况
OPT(6) max(OPT(4)+3, OPT(5)) 
OPT(n) max(OPT(n-2)+arr[n], OPT(n-1))
边界
OPT(0) = arr[0]
OPT(1) = max(arr[0], arr[1])
'''

def dpOpt(arr):
    opt = np.zeros(len(arr), int)
    flag = np.zeros(len(arr), int)
    opt[0] = arr[0]
    if arr[1] > arr[0]:
        opt[1] = arr[1]
        flag[1] = 1
    else:
        opt[1] = arr[0]
    for i in range(2, len(arr)):
        if opt[i-1] > arr[i]+opt[i-2]:
            opt[i] = opt[i-1]
            flag[i] = i - 1
        else:
            opt[i] = arr[i]+opt[i-2]
            flag[i] = i
    nums, n = [], len(arr)-1
    while n > -1:
        if n == flag[n]:
            nums.append(n)
            n = n - 2
        else:
            n = flag[n]
    nums.reverse()
    return opt[len(arr)-1], [arr[i] for i in nums]

# arr = [1,2,4,1,7,8,3,1]
arr = [4,3,5,7]
maxNum, selectList = dpOpt(arr)
print(maxNum)
print(selectList)


# 递归
def recOpt(arr, i):
    if i == 0:
        return arr[0]
    elif i == 1:
        return max(arr[0], arr[1])
    else:
        A = rec_opt(arr, i - 2) + arr[i]
        B = rec_opt(arr, i - 1)
        return max(A, B)