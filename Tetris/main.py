# Tetris

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 30 September, 2021

import random
import pygame

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)

clock = pygame.time.Clock()
FPS = 60

# COLORS *********************************************************************

WHITE = (255, 255, 255)
BLUE = (30, 144,255)
BLACK = (0, 0, 20)


running = True
while running:
	win.fill(BLACK)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

	pygame.draw.rect(win, BLUE, (0,0, WIDTH, HEIGHT), 5, border_radius=2)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()