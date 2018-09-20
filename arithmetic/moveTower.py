# -*- encoding: utf-8 -*-
#!/usr/bin/env python

'''
河内塔问题

1、把圆盘数减一层数的小塔经过目标杆移动到中间杆
2、把剩下的圆盘移动到目标杆
3、把圆盘数减一层数的小塔从中间杆,经过起始杆移动到目标杆
'''
def moveTower(height, fromPole, withPole, toPole):
    if height==1:
        print('moving disk from %s to %s' %(fromPole, toPole))
        return
    # 将fromPole 上的(height-1)移动到withPole
    moveTower(height-1, fromPole, toPole, withPole)
    # 将fromPole中剩下的最后一个移到toPole
    moveTower(1, fromPole, withPole, toPole)
    # 递归withPole上(heigth-1)移动到toPole
    moveTower(height-1, withPole, fromPole, toPole)

moveTower(3, "A", "B", "C")