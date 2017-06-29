#coding=utf-8
'''
                    0
            1                       2
    3               4           5       6
7       8       9
广度优先算法： 
    层次遍历 
        0 1 2 3 4 5 6 7 8 9
深度优先算法：
    先序遍历（DLR)
        0 1 3 7 8 4 9 2 5 6
    中序遍历（LDR)
        7 3 8 1 9 4 0 5 2 6
    后序遍历（LRD)
        7 8 3 9 4 1 5 6 2 0

实现功能：
① 树的构造
② 递归实现先序遍历、中序遍历、后序遍历
③ 堆栈实现先序遍历、中序遍历、后序遍历
④ 队列实现层次遍历
'''
class Node(object):
    """节点类"""
    def __init__(self, elem=None, lchild=None, rchild=None):
        self.elem = elem
        self.lchild = lchild
        self.rchild = rchild

class Tree(object):
    """树类"""
    def __init__(self):
        self.root = Node()
        self.myQueue = []
    def add(self, elem):
        """为树添加节点"""
        node = Node(elem)
        if self.root.elem == None: # 如果树是空的，则对根节点赋值
            self.root = node
            self.myQueue.append(self.root)
        else:
            treeNode = self.myQueue[0] # 此结点的子树还没有齐。
            if treeNode.lchild == None:
                treeNode.lchild = node
                self.myQueue.append(treeNode.lchild)
            else:
                treeNode.rchild = node
                self.myQueue.append(treeNode.rchild)
                self.myQueue.pop(0) # 如果该结点存在右子树，将此结点丢弃。
    def front_digui(self, root):
        """利用递归实现树的先序遍历DLR"""
        # 递归出口
        if root == None:
            return
        print root.elem,
        self.front_digui(root.lchild)
        self.front_digui(root.rchild)
    def middle_digui(self, root):
        """利用递归实现树的中序遍历"""
        if root == None:
            return
        self.middle_digui(root.lchild)
        print root.elem,
        self.middle_digui(root.rchild)
    def later_digui(self, root):
        """利用递归实现树的后序遍历"""
        if root == None:
            return
        self.later_digui(root.lchild)
        self.later_digui(root.rchild)
        print root.elem,
    def front_stack(self, root):
        """利用堆栈实现树的先序遍历"""
        if root == None:
            return
        myStack = []
        node = root
        while node or myStack:
            while node: #从根节点开始，一直找它的左子树
                print node.elem,
                myStack.append(node)
                node = node.lchild
            node = myStack.pop()  #while结束表示当前节点node为空，即前一个节点没有左子树了
            node = node.rchild    #开始查看它的右子树
    def middle_stack(self, root):
        """利用堆栈实现树的中序遍历"""
        if root == None:
            return
        myStack = []
        node = root
        while node or myStack:
            while node:           #从根节点开始，一直找它的左子树
                myStack.append(node)
                node = node.lchild
            node = myStack.pop()      #while结束表示当前节点node为空，即前一个节点没有左子树了
            print node.elem,
            node = node.rchild         #开始查看它的右子树
    def later_stack(self, root):
        """利用堆栈实现树的后序遍历"""
        if root == None:
            return
        myStack1 = []
        myStack2 = []
        node = root
        myStack1.append(node)
        while myStack1:  #这个while循环的功能是找出后序遍历的逆序，存在myStack2里面
            node = myStack1.pop()
            if node.lchild:
                myStack1.append(node.lchild)
            if node.rchild:
                myStack1.append(node.rchild)
            myStack2.append(node)
        while myStack2:  #将myStack2中的元素出栈，即为后序遍历次序
            print myStack2.pop().elem,
    def level_queue(self, root):
        """利用队列实现树的层次遍历"""
        if root == None:
            return
        myQueue = []
        node = root
        myQueue.append(node)
        while myQueue:
            node = myQueue.pop(0)
            print node.elem,
            if node.lchild != None:
                myQueue.append(node.lchild)
            if node.rchild != None:
                myQueue.append(node.rchild)
if __name__ == '__main__':
    """主函数"""
    elems = range(10)      #生成十个数据作为树节点
    tree = Tree()     #新建一个树对象
    for elem in elems:
        tree.add(elem)      #逐个添加树的节点
    print '递归实现先序遍历:'
    tree.front_digui(tree.root)
    print '\n递归实现中序遍历:'
    tree.middle_digui(tree.root)
    print '\n递归实现后序遍历:'
    tree.later_digui(tree.root)
    print '\n\n堆栈实现先序遍历:'
    tree.front_stack(tree.root)
    print '\n堆栈实现中序遍历:'
    tree.middle_stack(tree.root)
    print '\n堆栈实现后序遍历:'
    tree.later_stack(tree.root)
    print '\n\n队列实现层次遍历:'
    tree.level_queue(tree.root)
'''
树的遍历主要有两种，一种是深度优先遍历，像前序、中序、后序；
另一种是广度优先遍历，像层次遍历。
在树结构中两者的区别还不是非常明显，但从树扩展到有向图，到无向图的时候，
深度优先搜索和广度优先搜索的效率和作用还是有很大不同的。

深度优先一般用递归，广度优先一般用队列。
一般情况下能用递归实现的算法大部分也能用堆栈来实现。
'''