# Piano Tiles

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 30 November, 2021

import random
import pygame
from objects import Tile

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
TILE_WIDTH = WIDTH // 4
TILE_HEIGHT = 130

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 30

# COLORS *********************************************************************

WHITE = (255, 255, 255)

# GROUPS & OBJECTS ***********************************************************

tile_group = pygame.sprite.Group()

# FUNCTIONS ******************************************************************

def get_speed(score):
	return 200 + 5 * score

# VARIABLES ******************************************************************
scrolling = 0
num_tiles = 0
score = 0
speed = 1

clicked = False
pos = None

running = True
while running:
	pos = None
	win.fill(WHITE)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = event.pos

	tile_group.update(speed)
	if pos:
		for tile in tile_group:
			if tile.rect.collidepoint(pos):
				tile.kill()
				score += 1

	if scrolling - 10 > (num_tiles * TILE_HEIGHT):
		x = random.randint(0, 3)
		t = Tile(x * TILE_WIDTH, -TILE_HEIGHT, win)
		tile_group.add(t)
		num_tiles += 1

	for i in range(4):
		pygame.draw.line(win, (25, 25, 25), (TILE_WIDTH * i, 0), (TILE_WIDTH*i, HEIGHT), 1)

	speed = get_speed(score) * (FPS / 1000)
	scrolling += speed
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()