# -*- coding: utf-8 -*
'''
6. 堆排序(heap sort）

原理
堆排序（Heapsort）是指利用堆这种数据结构所设计的一种排序算法。
堆积是一个近似完全二叉树的结构，并同时满足堆积的性质：即子结点的键值或索引总是小于（或者大于）它的父节点。

1. 创建最大堆:将堆所有数据重新排序，使其成为最大堆
2. 最大堆调整:作用是保持最大堆的性质，是创建最大堆的核心子程序
3. 堆排序:移除位在第一个数据的根节点，并做最大堆调整的递归运算
'''
# 数组编号从 0开始
def left(i):
    return 2*i+1    # 2i
def right(i):
    return 2*i+2    # 2i + 1

def heap_sort(list):
    # 创建最大堆(初始化)
    for start in range(len(list) // 2 - 1, -1, -1): # 遍历len(list)//2次 节点-1对应list下标
        max_heapify(list, start, len(list)-1)
    # print(list)
    # 堆排序
    for end in range(len(list) - 1, 0, -1):
        list[0], list[end] = list[end], list[0]
        max_heapify(list, 0, end - 1)
    return list

def heap_sort1(list):
    # 创建最大堆(初始化)
    for start in range(len(list) // 2 - 1, -1, -1): # 遍历len(list)//2次 节点-1对应list下标
        sift_down(list, start, len(list)-1)
    # print(list)
    # 堆排序
    for end in range(len(list) - 1, 0, -1):
        list[0], list[end] = list[end], list[0]
        sift_down(list, 0, end - 1)
    return list


# 保持最大堆性质 使以root为根的子树成为最大堆  
def sift_down(list, root, end):
    while True:
        l = left(root)
        if l > end: # 左节点不存在 为叶子节点
            break
        r = right(root)
        max_child = l # 设左节点为最大值
        if r <= end and list[l] < list[r]: #右节点存在并且 左节点值小于右节点值
            max_child = r
        if list[root] < list[max_child]:
            list[root], list[max_child] = list[max_child], list[root]
            root = max_child
        else:
            break

def max_heapify(list, root, end):
    l = left(root)
    # 递归出口
    if l > end: # 左节点不存在 为叶子节点
        return
    r = right(root)
    max_child = l # 设左节点为最大值
    if r <= end and list[l] < list[r]: #右节点存在并且 左节点值小于右节点值
        max_child = r
    if list[root] < list[max_child]:
        list[root], list[max_child] = list[max_child], list[root]
        root = max_child
        max_heapify(list, max_child, end)

print(heap_sort([3, 1, 5, 7, 2, 4, 9, 6, 8]))
print(heap_sort1([3, 1, 5, 7, 2, 4, 9, 6, 8]))