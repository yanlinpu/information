import pygame
from sys import exit

try:
    screen = pygame.display.set_mode((640, -1))
except pygame.error, e:
    print "Can't create the display :-C"
    print e
    exit()