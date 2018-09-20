# -*- encoding: utf-8 -*-
#!/usr/bin/env python
import numpy as np

# 用最少的硬币来找零。
'''
1. 首先我们要弄清楚基本结束条件。如果我们要找的 零钱的价值和某一种硬币的价值一样,那么答案很简单,只要一个硬币。
2. 我们需要的是一个 1 美分加上给原始价值减去 1 美分找 零所需硬币数量的最小值,
    或者一个 5 美分加上给原始价值减去 5 美分找零所需硬币数量的最小 值,
    或者一个 10 美分加上给原始价值减去 10 美分找零所需硬币数量的最小值,等等。

eg. [1, 5, 10, 21, 25], 63
'''
coinValueList = [1, 5, 10, 21, 25]
change = 63
# 递归
def recChange(coinValueList, change):
    minCoins = change
    if change in coinValueList:
        return 1
    else:
        for i in [c for c in coinValueList if c < change]:
            numCoins = 1 + recChange(coinValueList, change-i)
            if numCoins < minCoins:
                minCoins = numCoins
    return minCoins

# print(recChange(coinValueList, change))
# 以上递归算法的问题就是它太低效了。事实上,它需要67716925次递归调用才能得出有4种硬币 时找零63美分问题的最优解!

# 动态规划
def dpChange(coinValueList, change):
    minCoins = np.zeros(change+1, int)
    for cents in range(1, change+1):
        coinCount = cents
        for i in [c for c in coinValueList if c <= cents]:
            if minCoins[cents-i] < coinCount:
                coinCount = minCoins[cents-i] + 1
        minCoins[cents] = coinCount
    return minCoins[change]
print(dpChange(coinValueList, 63))

# 打印出 找零的值
def dpChange2(coinValueList, change):
    minCoins = np.zeros(change+1, int)
    coinsUsed = np.zeros(change+1, int)
    for cents in range(1, change+1):
        coinCount = cents
        newCoin = 1
        for i in [c for c in coinValueList if c <= cents]:
            if minCoins[cents-i] < coinCount:
                coinCount = minCoins[cents-i] + 1
                newCoin = i
        minCoins[cents] = coinCount
        coinsUsed[cents] = newCoin

    coinslist, coin = [], change
    while coin > 0:
        coinslist.append(coinsUsed[coin])
        coin = coin - coinsUsed[coin]
    return minCoins[change], coinslist

print(dpChange2(coinValueList, 63))