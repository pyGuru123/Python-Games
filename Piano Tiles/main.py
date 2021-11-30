# Piano Tiles

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 30 November, 2021

import pygame
from objects import Tile

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

# COLORS *********************************************************************

BLACK = (255, 255, 255)

# GROUPS & OBJECTS ***********************************************************

tile_group = pygame.sprite.Group()
t = Tile(80, 0, win)
tile_group.add(t)

speed = 3

running = True
while running:
	win.fill(BLACK)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

	tile_group.update(speed)

	clock.tick(FPS)
	pygame.display.update()

running = False