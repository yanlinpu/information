## 简介

在计算机科学中，分治法是一种很重要的算法。字面上的解释是“分而治之”，就是`把一个复杂的问题分成两个或更多的相同或相似的子问题，再把子问题分成更小的子问题……直到最后子问题可以简单的直接求解，原问题的解即子问题的解的合并。`

分治算法也叫分治策略，把输入分为若干个部分，递归解决每一个问题，最后将这些子问题合并为一个全局解。如果子问题较大，可以再次使用分治策略。

## 特点

1. 该问题的规模缩小到一定程度就可以很容易的解决
2. 该问题可以分解为若干个规模较小的相同问题，即该问题具有最优子结构性质。
3. 分解出的子问题的解可以合并为原问题的解
4. 分解出的各个子问题是相互独立的，即子问题之间不包含公共的子子问题。

第一条特征是绝大多数问题都可以满足的，因为问题的计算复杂性一般是随着问题规模的增加而增加；

第二条特征是应用分治法的前提它也是大多数问题可以满足的，此特征反映了递归思想的应用；

`第三条特征是关键，能否利用分治法完全取决于问题是否具有第三条特征，如果具备了第一条和第二条特征，而不具备第三条特征，则可以考虑用贪心法或动态规划法。`

第四条特征涉及到分治法的效率，如果各子问题是不独立的则分治法要做许多不必要的工作，重复地解公共的子问题，此时虽然可用分治法，但一般用动态规划法较好。

## 步骤

分治法在每一层递归上都有三个步骤：

    step1 分解：将原问题分解为若干个规模较小，相互独立，与原问题形式相同的子问题；

    step2 解决：若子问题规模较小而容易被解决则直接解，否则递归地解各个子问题

    step3 合并：将各个子问题的解合并为原问题的解。

它的一般的算法设计模式如下：

    Divide-and-Conquer(P)

    1. if |P|≤n0

    2. then return(ADHOC(P))

    3. 将P分解为较小的子问题 P1 ,P2 ,...,Pk

    4. for i←1 to k

    5. do yi ← Divide-and-Conquer(Pi) △ 递归解决Pi

    6. T ← MERGE(y1,y2,...,yk) △ 合并子问题

    7. return(T)

    其中|P|表示问题P的规模；n0为一阈值，表示当问题P的规模不超过n0时，问题已容易直接解出，不必再继续分解。ADHOC(P)是该分治法中的基本子算法，用于直接解小规模的问题P。因此，当P的规模不超过n0时直接用算法ADHOC(P)求解。算法MERGE(y1,y2,...,yk)是该分治法中的合并子算法，用于将P的子问题P1 ,P2 ,...,Pk的相应的解y1,y2,...,yk合并为P的解。

## 经典问题：

- 二叉树查找算法
- 查找最大最小值
- 归并排序
- 快速排序
- 选择第K小元素
- 大整数乘法
- 二分搜索
- Strassen矩阵乘法
- 棋盘覆盖
- 合并排序
- 线性时间选择
- 最接近点对问题
- 汉诺塔