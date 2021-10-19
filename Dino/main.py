# Dino

# Author : Prajjwal Pathak (pyguru)
# Date : Sunday, 17 October, 2021

import random
import pygame

from objects import Ground, Dino

pygame.init()
SCREEN = WIDTH, HEIGHT = (600, 200)
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)

clock = pygame.time.Clock()
FPS = 60

# COLORS *********************************************************************

WHITE = (225,225,225)
BLACK = (32, 33, 36)
GRAY = (172, 172, 172)

# OBJECTS ********************************************************************

ground = Ground()
dino = Dino(50, 110)

# VARIABLES ******************************************************************

SPEED = 4

running = True
while running:
	win.fill(BLACK)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

	ground.update(SPEED)
	ground.draw(win)
	dino.update()
	dino.draw(win)

	pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 4)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()