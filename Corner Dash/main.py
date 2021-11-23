# Rotate Dash

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 15 November, 2021

import random
import pygame

from objects import Ball, Line, Circle, Square, get_circle_position, \
					Particle, ScoreCard, Button, Message, rotate_image, \
					BlinkingText

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 60

# COLORS *********************************************************************

RED = (255,0,0)
GREEN = (0,177,64)
BLUE = (30, 144,255)
ORANGE = (252,76,2)
YELLOW = (254,221,0)
PURPLE = (155,38,182)
AQUA = (0,103,127)
WHITE = (200,200,200)
BLACK = (30,30,30)
GRAY = (128,128,128)

score_bg = 128

color_list = [BLUE, GREEN, RED, ORANGE, YELLOW, PURPLE]
color_index = 0
color = color_list[color_index]