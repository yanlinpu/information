#!/usr/bin/env python
import pygame
from pygame.locals import *
from sys import exit
import sys
from random import *
from math import pi
import random

pygame.init();
screen = pygame.display.set_mode((490, 650), 0, 32)
pygame.display.set_caption("2048")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == KEYDOWN:
            delta = False
            if  event.key == K_LEFT:
                if (check_column() == True  or  up_zero() == True):
                    push_up()
                    delta = True
            elif  event.key == K_RIGHT:
                if (check_column() == True  or  down_zero() == True):
                    push_down()
                    delta = True
            elif  event.key == K_UP:
                if (check_row() == True  or  left_zero() == True):
                    push_left()
                    delta = True
            elif  event.key == K_DOWN: 
                if (check_row() == True  or  right_zero() == True):
                    push_right()
                    delta = True
            if (delta == True and has_zero() == True):
                insert()
            if (game_over() == True):
                print "Loser"
            map_init()
            
    map_init()
    pygame.display.update()