# -*- coding: utf-8 -*
'''
1. 插入排序—直接插入排序(Straight Insertion Sort)

基本思想:
插入排序（Insertion Sort）是一种简单直观的排序算法。
它的工作原理是通过构建有序序列，对于未排序数据，在已排序序列中从后向前扫描，找到相应位置并插入。

1. 从第一个元素开始，该元素可以认为已经被排序
2. 取出下一个元素，在已经排序的元素序列中从后向前扫描
3. 如果该元素（已排序）大于新元素，将该元素移到下一位置
4. 重复步骤3，直到找到已排序的元素小于或者等于新元素的位置
5. 将新元素插入到该位置后
6. 重复步骤2~5
'''

def insert_sort(lists):
    count = len(lists)
    for i in range (1, count):
        if lists[i] < lists[i-1]: # 找到比前一个元素（已排序的最大或者最小元素）小的元素  大于或者等于已经跳过
            temp = lists[i]       # 取出该元素
            index = i             # 插入元素的位置
            for j in range(i-1, -1, -1):  # 从后往前找出比temp小的元素
                if lists[j] > temp:       # 大于temp 元素位置交换
                    lists[j+1] = lists[j]
                    index = j
                else:
                    break
            lists[index] = temp   # 插入元素
    return lists
    
a = [3, 1, 5, 7, 2, 4, 9, 6, 8]
sorted = insert_sort(a)
print(sorted)