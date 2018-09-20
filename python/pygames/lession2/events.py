# -*- encoding: utf-8 -*-
#!/usr/bin/env python

'''
###
事件	           产生途径	                            参数
QUIT	        用户按下关闭按钮	               none
ATIVEEVENT	    Pygame被激活或者隐藏	            gain, state
KEYDOWN	        键盘被按下	                     unicode, key, mod
KEYUP	        键盘被放开	                     key, mod
MOUSEMOTION	    鼠标移动	                      pos, rel, buttons
MOUSEBUTTONDOWN	鼠标按下	                      pos, button
MOUSEBUTTONUP	鼠标放开	                      pos, button
JOYAXISMOTION	游戏手柄(Joystick or pad)移动	     joy, axis, value
JOYBALLMOTION	游戏球(Joy ball)?移动	          joy, axis, value
JOYHATMOTION	游戏手柄(Joystick)?移动	         joy, axis, value
JOYBUTTONDOWN	游戏手柄按下	                     joy, button
JOYBUTTONUP	    游戏手柄放开	                     joy, button
VIDEORESIZE	    Pygame窗口缩放	                   size, w, h
VIDEOEXPOSE	    Pygame窗口部分公开(expose)?	     none
USEREVENT	    触发了一个用户事件	               code
###
'''

# 导入pygame库
import pygame
# # 导入一些常用的函数和常量
from pygame.locals import *
# # 向sys模块借一个exit函数用来退出程序
from sys import exit
# # 初始化pygame,为使用硬件做准备
pygame.init()

SCREEN_SIZE = (640, 480)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

font = pygame.font.SysFont("arial", 16);
font_height = font.get_linesize()
event_text = []
pygame.display.set_caption("event details")
while True:

    event = pygame.event.wait()
    event_text.append(str(event))
    # 获得时间的名称
    
    event_text = event_text[-SCREEN_SIZE[1]/font_height:]
    # 这个切片操作保证了event_text里面只保留一个屏幕的文字

    if event.type == QUIT:
        exit()

    screen.fill((255, 255, 255))

    y = SCREEN_SIZE[1]-font_height
    # 找一个合适的起笔位置，最下面开始但是要留一行的空
    for text in reversed(event_text):
        screen.blit( font.render(text, True, (0, 0, 0)), (0, y) )
        y-=font_height
        # 把笔提一行

    pygame.display.update()