# -*- coding: utf-8 -*
'''
4. 希尔排序（shell sort）

原理
希尔排序(Shell Sort)是插入排序的一种。
也称缩小增量排序，是直接插入排序算法的一种更高效的改进版本。
希尔排序是非稳定排序算法。
该方法因DL．Shell于1959年提出而得名。 
希尔排序是把记录按下标的一定增量分组，对每组使用直接插入排序算法排序；
随着增量逐渐减少，每组包含的关键词越来越多，当增量减至1时，整个文件恰被分成一组，算法便终止。

将n个记录分成d个子序列
lists[0], lists[d], lists[2d]...lists[kd]
lists[1], lists[1+d], lists[1+2d]...lists[1+kd]
lists[2], lists[2+d], lists[2+2d]...lists[2+kd]
...
lists[d-1]...

1. 先取一个小于n的整数d1作为第一个增量，把文件的全部记录分成d1个组。所有距离为d1的倍数的记录放在同一个组中。在各组内进行直接插入排序
2. 取第二个增量d2<d1重复上述的分组和排序，直至所取的增量dt=1(dt<dt-l<；…<d2<d1），即所有记录放在同一组中进行直接插入排序为止。
'''
    
def shell_sort(lists):
    count = len(lists)
    step = 2
    dt = count/2  #增量dt 每次除以2 
    while dt > 0: #dt=1时，所有记录放在同一组 进行最后一次插入排序
        for i in range(dt):     # 分为dt各组
            j = i + dt          # 取下一个元素
            while j < count: 
                sorted_last_key = j - dt
                sort_value = lists[j]
                while sorted_last_key >= 0:
                    if lists[sorted_last_key] <= sort_value:
                        break
                    else:
                        lists[sorted_last_key + dt] = lists[sorted_last_key]
                        lists[sorted_last_key] = sort_value
                        sorted_last_key -= dt
                j += dt
        dt /= step 
    return lists

a = [3, 1, 5, 7, 2, 4, 9, 6, 8]
sorted = shell_sort(a)
print(sorted)