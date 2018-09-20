# -*- encoding: utf-8 -*-
#!/usr/bin/env python
import numpy as np

# 最长公共子序列
'''
最长公共子序列的问题常用于解决字符串的相似度

一个给定序列的子序列是在该序列中删去若干元素后得到的序列。
eg.
['cnblogs', 'belong'] -> 'blog'

现有两个序列X={x1,x2,x3，...xi}，Y={y1,y2,y3，....，yj}，
设一个C[i,j]: 保存Xi与Yj的LCS的长度。
递归定义最优值
if i == 0 or j == 0:
    C[i][j] = 0
elif X[i] == Y[j]:
    C[i][j] = C[i-1][j-1]+1
else:
    max(C[i-1][j], C[i][j-1])
'''

def dpLcs(a, b):
    c=np.zeros((len(a)+1, len(b)+1), dtype=int)
    flag=np.zeros((len(a)+1, len(b)+1), dtype=str)
    for i in range(len(a)):
        for j in range(len(b)):
            if a[i] == b[j]:
                c[i+1][j+1] = c[i][j]+1
                flag[i+1][j+1] = 'O' # OK
            else:
                if c[i+1][j] > c[i][j+1]:
                    c[i+1][j+1]=c[i+1][j]
                    flag[i+1][j+1] = 'L' # LEFT
                else:
                    c[i+1][j+1] = c[i][j+1]
                    flag[i+1][j+1] = 'U' # UP
    
    return c[len(a), len(b)], flagParse(flag, a, len(a), len(b), '')

def flagParse(flag, a, i, j, result):
    if i == 0 or j == 0:
        return result
    if flag[i][j] == 'O':
        result = a[i-1] + result
        return flagParse(flag, a, i-1, j-1, result)
    elif flag[i][j] == 'L':
        return flagParse(flag, a, i, j-1, result)
    elif flag[i][j] == 'U':
        return flagParse(flag, a, i-1, j, result)

a='ABCBDAB'
b='BDCABA'
c, flag = dpLcs(a, b)
print(c)
print(flag)