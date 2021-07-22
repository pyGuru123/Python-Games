# Arc Dash

# Author : Prajjwal Pathak (pyguru)
# Date : Saturday, 17 July, 2021

import pygame
import random
from math import pi as PI

from objects import draw_arc

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
# | pygame.SCALED | pygame.FULLSCREEN
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
pygame.display.set_caption('Arc Dash')

clock = pygame.time.Clock()
FPS = 30


# VARIABLES


running = True
while running:
	win.fill((255, 255, 255))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

	draw_arc(win, [20,100,200,200], PI/2, PI)
	draw_arc(win, [60,100,200,140], PI/2, PI)
	draw_arc(win, [WIDTH-50,100,WIDTH-200,200], 0, PI)


	clock.tick(FPS)
	pygame.display.update()

pygame.quit()