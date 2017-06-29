# -*- coding: utf-8 -*
'''
7. 归并排序(merge sort）

原理

归并排序是建立在归并操作上的一种有效的排序算法,该算法是采用分治法（Divide and Conquer）的一个非常典型的应用。
将已有序的子序列合并，得到完全有序的序列；
即先使每个子序列有序，再使子序列段间有序。
若将两个有序表合并成一个有序表，称为二路归并。

1. 将序列每相邻两个数字进行归并操作，形成 {displaystyle floor(n/2)} floor(n/2)个序列，排序后每个序列包含两个元素
2. 将上述序列再次归并，形成 {displaystyle floor(n/4)} floor(n/4)个序列，每个序列包含四个元素
3. 重复步骤2，直到所有元素排序完毕
'''
# 递归法

def merge_sort(list):
    # 认为长度不大于1的数列是有序的
    if len(list) <= 1:
        return list
    # 二分列表
    middle = len(list) // 2
    left = merge_sort(list[:middle])
    # print(left)
    right = merge_sort(list[middle:])
    # print(right)
    # 最后一次合并
    return merge(left, right)
# 合并
def merge(left, right):
    l, r = 0, 0
    result=[]
    while l<len(left) and r<len(right):
        if left[l] < right[r]:
            result.append(left[l])
            l += 1
        else:
            result.append(right[r])
            r += 1
    result += left[l:]
    result += right[r:]
    return result
a = [3, 1, 5, 7, 2, 4, 9, 6, 8]
sorted = merge_sort(a)
print(sorted)
