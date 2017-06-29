# -*- coding: utf-8 -*
'''
8. 计数排序(Counting sort)

原理

当输入的元素是n个0到k之间的整数时，它的运行时间是Θ(n + k)。
计数排序不是比较排序，排序的速度快于任何比较排序算法。

由于用来计数的数组C的长度取决于待排序数组中数据的范围（等于待排序数组的最大值与最小值的差加上1），
这使得计数排序对于数据范围很大的数组，需要大量时间和内存。
例如：计数排序是用来排序0到100之间的数字的最好的算法，但是它不适合按字母顺序排序人名。



计数排序的过程类似小学选班干部的过程,如某某人10票,作者9票,那某某人是班长,作者是副班长
大体分两部分,第一部分是拉选票和投票,第二部分是根据你的票数入桶
看下具体的过程,一共需要三个数组,分别是待排数组,票箱数组,和桶数组
var unsorted = new int[] { 6, 2, 4, 1, 5, 9 };  //待排数组
var ballot = new int[unsorted.Length];          //票箱数组
var bucket = new int[unsorted.Length];          //桶数组

最后再看桶数组,先看待排数组和票箱数组
初始状态,迭代变量i = 0时,待排数组[i] = 6,票箱数组[i] = 0,这样通过迭代变量建立了数字与其桶号(即票数)的联系
待排数组[ 6 2 4 1 5 9 ] i = 0时,可以从待排数组中取出6
票箱数组[ 0 0 0 0 0 0 ] 同时可以从票箱数组里取出6的票数0,即桶号

1. 拉选票的过程
首先6出列开始拉选票,6的票箱是0号,6对其它所有数字说,谁比我小或与我相等,就给我投票,不然揍你
于是,2 4 1 5 分别给6投票,放入0号票箱,6得四票
待排数组[ 6 2 4 1 5 9 ]
票箱数组[ 4 0 0 0 0 0 ]
...
投票完毕时的状态是这样
待排数组[ 6 2 4 1 5 9 ]
票箱数组[ 4 1 2 0 3 5 ]

2. 入桶的过程
投票过程结束,每人都拥有自己的票数,桶数组说,看好你自己的票数,进入与你票数相等的桶,GO

6共计5票,进入5号桶
2得1票,进入1号桶,有几票就进几号桶
4两票,进2号桶,5三票进3号桶,9有5票,进5号桶
待排数组[ 6 2 4 1 5 9 ]
票箱数组[ 4 1 2 0 3 5 ]

-----------------------

入桶前 [ 0 1 2 3 4 5 ] //里边的数字表示桶编号
入桶后 [ 1 2 4 5 6 9 ] //1有0票,进的0号桶
排序完毕,顺序输出即可[ 1 2 4 5 6 9]
'''

def count_sort(list):
    n=len(list)
    bucket=[None]*n #桶
    for i in range(n):
        p=0
        q=0
        for j in range(n):
            if list[j] < list[i]:
                p += 1
            elif list[j] == list[i]:
                q+=1
        for k in range(p,p+q):
            bucket[k]=list[i]
    return bucket
print(count_sort([1, 101, 105, 107, 106, 102, 104, 109, 106, 108]))