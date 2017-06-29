# -*- coding: utf-8 -*
'''
5. 快速排序(quick sort）

原理
快速排序由C. A. R. Hoare在1962年提出。它的基本思想是：
通过一趟排序将要排序的数据分割成独立的两部分，其中一部分的所有数据都比另外一部分的所有数据都要小，
然后再按此方法对这两部分数据分别进行快速排序，整个排序过程可以递归进行，以此达到整个数据变成有序序列。

快速排序使用分治法（Divide and conquer）策略来把一个序列（list）分为两个子序列（sub-lists）。

1. 从数列中挑出一个元素，称为"基准"（pivot）
2. 重新排序数列，所有元素比基准值小的摆放在基准前面，所有元素比基准值大的摆在基准的后面（相同的数可以到任一边）。
在这个分区结束之后，该基准就处于数列的中间位置。这个称为分区（partition）操作。
3. 递归地（recursive）把小于基准值元素的子数列和大于基准值元素的子数列排序。
'''

#方法1
def quick_sort_1(list):
    less = []
    pivotList = []
    more = []
    # 递归出口
    if len(list) <= 1:
        return list
    else:
        # 将第一个值做为基准
        pivot = list[0]
        for i in list:
            # 将比基准小的值放到less数列
            if i < pivot:
                less.append(i)
            # 将比基准大的值放到more数列
            elif i > pivot:
                more.append(i)
            # 将和基准相同的值保存在基准数列
            else:
                pivotList.append(i)
        # 对less数列和more数列继续进行排序
        less = quick_sort_1(less)
        more = quick_sort_1(more)
        return less + pivotList + more

a = [3, 1, 5, 7, 2, 4, 9, 6, 8]
sorted = quick_sort_1(a)
print(sorted)

#方法2
def quick_sort(array):
    qsort(array, 0, len(array)-1)

def qsort(array, low, high):
     if low < high:
        key_index = partition(array, low, high)
        qsort(array, low, key_index)
        qsort(array, key_index+1, high)
        
def partition(array, low, high):
    key = array[low]
    while low < high:
        while low < high and array[high] >= key:
            high -= 1
        while low < high and array[high] < key:
            array[low] = array[high]
            low += 1
            array[high] = array[low]
    array[low] = key
    return low

array = [3, 1, 5, 7, 2, 4, 9, 6, 8]
quick_sort(array)
print array