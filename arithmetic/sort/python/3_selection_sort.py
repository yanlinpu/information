# -*- coding: utf-8 -*
'''
3. 选择排序（Selection sort）

原理
选择排序（Selection sort）是一种简单直观的排序算法。
它的工作原理大致是将后面的元素最小元素一个个取出然后按顺序放置。

1. 在未排序序列中找到最小元素，存放到排序序列的起始位置，
2. 再从剩余未排序元素中继续寻找最小（大）元素，然后放到已排序序列的末尾。
3. 重复第二步，直到所有元素均排序完毕。
'''
    
def selection_sort(lists):
    count = len(lists)
    for i in range (count-1):  #count-1次遍历即可
        min_num = i
        for j in range(i+1, count):
            if lists[j] < lists[min_num]:
                min_num = j         # 找到未排序的最小的值得index
        lists[i], lists[min_num] = lists[min_num], lists[i]
    return lists

a = [3, 1, 5, 7, 2, 4, 9, 6, 8]
sorted = selection_sort(a)
print(sorted)