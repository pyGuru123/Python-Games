# Tetris

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 30 September, 2021

import random
import pygame

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 60


running = True
while running:
	win.fill((255, 255, 255))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

	pygame.draw.rect(win, (0,0,0), (0,0, WIDTH, HEIGHT), 5, border_radius=2)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()