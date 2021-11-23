# Corner Dash

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 23 November, 2021

import math
import random
import pygame

from objects import Circle
 
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

# GROUP & OBJECTS ************************************************************

circle_group = pygame.sprite.Group()
for i in range(12):
	c = Circle(i)
	circle_group.add(c)

running = True
while running:
	win.fill(GRAY)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

	pygame.draw.circle(win, RED, (CENTER[0], CENTER[1]), 5)

	circle_group.update(win)

	pygame.draw.rect(win, BLACK, (0, 0, WIDTH, HEIGHT), 8)
	clock.tick(FPS)
	pygame.display.update()

running = False