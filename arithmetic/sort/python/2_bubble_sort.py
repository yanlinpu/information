# -*- coding: utf-8 -*
'''
2. 冒泡排序(Bubble Sort)

原理
冒泡排序(Bubble Sort)是一种简单的排序算法。
它重复地走访过要排序的数列，一次比较两个元素，如果他们的顺序错误就把他们交换过来。
走访数列的工作是重复地进行直到没有再需要交换，也就是说该数列已经排序完成。这个算法的名字由来是因为越小的元素会经由交换慢慢“浮”到数列的顶端。

1. 比较相邻的元素。如果第一个比第二个大，就交换他们两个。
2. 对每一对相邻元素作同样的工作，从开始第一对到结尾的最后一对。这步做完后，最后的元素会是最大的数。
3. 针对所有的元素重复以上的步骤，除了最后一个。
4. 持续每次对越来越少的元素重复上面的步骤，直到没有任何一对数字需要比较。
'''
    
def bubble_sort(lists):
    count = len(lists)
    for i in range (count):
        flag = True  #标识符  步骤4
        for j in range(1, count-i): # i = 0遍历所有元素  i>1 count-i到count 已排序=====如步骤2，3
            if lists[j-1] > lists[j]:
                lists[j-1],lists[j] = lists[j],lists[j-1] #如果前一个元素大于后一个元素   互换值
                flag = False
        if flag:
            return lists
    return lists
    
a = [3, 1, 5, 7, 2, 4, 9, 6, 8]
sorted = bubble_sort(a)
print(sorted)