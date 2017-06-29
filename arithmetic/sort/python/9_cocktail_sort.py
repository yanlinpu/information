# -*- coding: utf-8 -*
'''
9. 鸡尾酒排序(Cocktail sort)

原理

鸡尾酒排序也就是定向冒泡排序, 
鸡尾酒搅拌排序, 搅拌排序 (也可以视作选择排序的一种变形), 涟漪排序,来回排序 or 快乐小时排序, 是冒泡排序的一种变形。
此演算法与冒泡排序的不同处在于排序时是以双向在序列中进行排序。
数组中的数字本是无规律的排放，先找到最小的数字，把他放到第一位，然后找到最大的数字放到最后一位。
然后再找到第二小的数字放到第二位，再找到第二大的数字放到倒数第二位。以此类推，直到完成排序。

'''
def cocktail_sort(l):
    size = len(l)
    # 假如一趟来回没有交换任何数字,则表示该数组已经有序了,可以设置了个变量表示有没有交换过
    sign = True  
    for i in range(size / 2):
        if sign:
            sign = False
            for j in range(i, size - 1 - i):
                if l[j] > l[j + 1]:
                    l[j], l[j + 1] = l[j + 1], l[j]
                    sign = True
            # print(l)
            for k in range(size - 2 - i, i, -1):
                if l[k] < l[k - 1]:
                    l[k], l[k - 1] = l[k - 1], l[k]
                    sign = True 
            # print(l)
        else:
            break
    # return l
a = [3, 1, 5, 7, 2, 4, 9, 6, 8]
cocktail_sort(a)
print(a)
