# -*- encoding: utf-8 -*-
#!/usr/bin/env python

'''
动态规划
一般用来求最大值，最优解等
overlab sub-problem
重叠子问题
把其中子问题保存

思考动态规划的第一点----最优子结构：
思考动态规划的第二点----子问题重叠：
思考动态规划的第三点----边界：
思考动态规划的第四点----子问题独立：

那么遇到问题如何用动态规划去解决呢？根据上面的分析我们可以按照下面的步骤去考虑：      
1、构造问题所对应的过程。
2、思考过程的最后一个步骤，看看有哪些选择情况。
3、找到最后一步的子问题，确保符合“子问题重叠”，把子问题中不相同的地方设置为参数。
4、使得子问题符合“最优子结构”。
5、找到边界，考虑边界的各种处理方式。
6、确保满足“子问题独立”，一般而言，如果我们是在多个子问题中选择一个作为实施方案，而不会同时实施多个方案，那么子问题就是独立的。
7、考虑如何做备忘录。
8、分析所需时间是否满足要求。
9、写出转移方程式。
'''

# demo1 从一堆数字选择不相邻数字 求最大值  [4,1,1,9,1] --> 4+9=13
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
# 递归
def rec_opt(arr, i):
    if i == 0:
        return arr[0]
    elif i == 1:
        return max(arr[0], arr[1])
    else:
        A = rec_opt(arr, i - 2) + arr[i]
        B = rec_opt(arr, i - 1)
        return max(A, B)

# 动态规划
import numpy as np
def dp_opt(arr):
    opt = np.zeros(len(arr))
    opt[0] = arr[0]
    opt[1] = max(arr[0], arr[1])
    for i in range(2, len(arr)):
        A = opt[i-2] + arr[i]
        B = opt[i-1]
        opt[i] = max(A, B)
    return opt[len(arr)-1]

arr = [1,2,4,1,7,8,3]
# print(rec_opt(arr, 6)) 
print(dp_opt(arr)) 


# demo2 [3, 34, 4, 12, 5, 2] 求n个数字相加能否等于给定数字9   假设所有数字>0 返回True or False
    
def rec_subset(arr, i, s):
    if s==0:
        return True
    elif i==0:
        return arr[0]==s
    elif arr[i]>s:
        return rec_subset(arr, i-1, s)
    else:
        A = rec_subset(arr, i-1, s-arr[i])
        B = rec_subset(arr, i-1, s)
        return A or B

def dp_subset(arr, S):
    subset = np.zeros((len(arr), S+1), dtype=bool)
    subset[:, 0] = True
    subset[0, :] = False
    subset[0, arr[0]] = True
    # print(subset)
    for i in range(1, len(arr)):
        for s in range(1, S+1):
            if arr[i] > s:
                subset[i, s] = subset[i-1, s]
            else:
                A = subset[i-1, s-arr[i]]
                B = subset[i-1, s]
                subset[i, s] = A or B
    r, c = subset.shape
    return subset[r-1, c-1]
arr2 = [3, 34, 4, 12, 5, 2]
# print(rec_subset(arr2, len(arr2)-1, 9))
print(dp_subset(arr2, 9))
print(dp_subset(arr2, 13))


# demo3 用最少的硬币来找零。
'''
1. 首先我们要弄清楚基本结束条件。如果我们要找的 零钱的价值和某一种硬币的价值一样,那么答案很简单,只要一个硬币。
2. 我们需要的是一个 1 美分加上给原始价值减去 1 美分找 零所需硬币数量的最小值,
    或者一个 5 美分加上给原始价值减去 5 美分找零所需硬币数量的最小 值,
    或者一个 10 美分加上给原始价值减去 10 美分找零所需硬币数量的最小值,等等。
'''
def recChange(coinValueList, change):
    minCoins = change
    if change in coinValueList:
        return 1
    else:
        for i in [c for c in coinValueList if c <= change]:
            numCoins = 1 + recChange(coinValueList, change-i)
            if numCoins < minCoins:
                minCoins = numCoins
    return minCoins

# 以上递归算法的问题就是它太低效了。事实上,它需要67716925次递归调用才能得出有4种硬币 时找零63美分问题的最优解!
# print(recChange([1, 5, 10, 25], 63))
def dpChange(coinValueList, change, minCoins, coinsUsed):
    for cents in range(change + 1):
        coinCount = cents
        newCoin = 1
        for i in [c for c in coinValueList if c <= cents]:
            if minCoins[cents-i] < coinCount:
                coinCount = minCoins[cents-i] + 1
                newCoin = i
        minCoins[cents] = coinCount
        coinsUsed[cents] = newCoin
        # print('====')
        # print(minCoins)
        # print(coinsUsed)
    coinslist, coin = [], change
    while coin > 0:
        coinslist.append(coinsUsed[coin])
        coin = coin - coinsUsed[coin]
    return minCoins[change], coinslist

change = 65
changeMinUsed, changeMinList = dpChange([1,5,10,21,25], change, np.zeros(change+1), np.zeros(change+1))
print(changeMinUsed, changeMinList)

