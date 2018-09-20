# -*- encoding: utf-8 -*-
#!/usr/bin/env python
import numpy as np

# 字符串相似度/编辑距离（edit distance）
'''
https://www.cnblogs.com/shihuajie/p/5772173.html

对于序列S和T，它们之间距离定义为：
对二者其一进行几次以下的操作
(1)删去一个字符；
(2)插入一个字符；
(3)改变一个字符。
每进行一次操作，计数增加1。将S和T变为同一个字符串的最小计数即为它们的距离。给出相应算法。

将S和T的长度分别记为len(S)和len(T)，并把S和T的距离记为m[len(S)][len(T)]，有以下几种情况：
如果末尾字符相同，那么m[len(S)][len(T)]=m[len(S)-1][len(T)-1]；
如果末尾字符不同，有以下处理方式
    1) 修改S或T末尾字符使其与另一个一致来完成，m[len(S)][len(T)]=m[len(S)-1][len(T)-1]+1；
    2) 在S末尾插入T末尾的字符，比较S[1...len(S)]和S[1...len(T)-1]；
    3) 在T末尾插入S末尾的字符，比较S[1...len(S)-1]和S[1...len(T)]；
    4) 删除S末尾的字符，比较S[1...len(S)-1]和S[1...len(T)]；
    5) 删除T末尾的字符，比较S[1...len(S)]和S[1...len(T)-1]；
总结为，对于i>0,j>0的状态(i,j),m[i][j] = min( m[i-1][j-1]+(s[i]==s[j])?0:1 , m[i-1][j]+1, m[i][j-1] +1)。
这里的重叠子结构是S[1...i]，T[1...j]。  


如果str1="ivan"，str2="ivan"，那么经过计算后等于 0。没有经过转换。相似度=1-0/Math.Max(str1.length,str2.length)=1
如果str1="ivan1"，str2="ivan2"，那么经过计算后等于1。str1的"1"转换"2"，转换了一个字符，所以距离是1，相似度=1-1/Math.Max(str1.length,str2.length)=0.8

1> str1或str2的长度为0返回另一个字符串的长度。 
    if len(str1)==0 or len(str2):
        return max(len(str1), len(str2));
2> 初始化(n+1)*(m+1)的矩阵d，并让第一行和列的值从0开始增长。
3> 扫描两字符串（n*m级的），如果：str1[i] == str2[j]，用temp记录它，为0。否则temp记为1。
然后在矩阵d[i,j]赋于d[i-1,j]+1 、d[i,j-1]+1、d[i-1,j-1]+temp三者（即左 上 左上三个方向）的最小值。
4> 扫描完后，返回矩阵的最后一个值d[n][m]即是它们的距离。
'''

def dpDistance(str1, str2):
    len1 = len(str1)
    len2 = len(str2)
    arr = np.zeros(shape=(len1+1, len2+1), dtype=int)
    if len1 == 0 or len2 == 0:
        return max(len1, len2)
    for i in range(len1+1):
        arr[0, i] = i
        arr[i, 0] = i
    # print(arr)
    for i in range(1, len1+1):
        for j in range(1, len2+1):
            if str1[i-1] == str2[j-1]:
                arr[i, j] = arr[i-1, j-1]
            else:
                arr[i, j] = min(arr[i, j-1]+1, arr[i-1, j]+1, arr[i-1, j-1]+1)
    print(arr)
    return arr[len1, len2]


print(dpDistance('abcd1','abcd2'))
print(dpDistance('abecd','bcdae'))