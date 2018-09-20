# -*- encoding: utf-8 -*-
#!/usr/bin/env python

###
# hello world
###

# 导入pygame库
import pygame
# 导入一些常用的函数和常量
from pygame.locals import *
# 向sys模块借一个exit函数用来退出程序
from sys import exit
# 初始化pygame,为使用硬件做准备
pygame.init()

# 创建了一个窗口
screen = pygame.display.set_mode((640, 480), 0, 32)
# 设置窗口标题
pygame.display.set_caption("Hello, World!")
# 加载并转换图像
# convert函数是将图像数据都转化为Surface对象，每次加载完图像以后就应该做这件事件（事实上因为 它太常用了，如果你不写pygame也会帮你做）；
# convert_alpha相比convert，保留了Alpha 通道信息（可以简单理解为透明的部分），这样我们的光标才可以是不规则的形状。
background_image_filename = ''
background = pygame.image.load(background_image_filename).convert()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    # 将背景图画上去
    # blit是个重要函数，第一个参数为一个Surface对象，第二个为左上角位置。
    screen.blit(background, (0,0))


    # 刷新一下画面(画完以后一定记得用update更新一下，否则画面一片漆黑。)
    pygame.display.update()