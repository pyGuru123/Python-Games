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
GRAY = (75, 75, 75)

# IMAGES *********************************************************************

bg_img = pygame.image.load('Assets/bg.png')
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

# GROUPS & OBJECTS ***********************************************************

tile_group = pygame.sprite.Group()
x = random.randint(0, 3)
t = Tile(x * TILE_WIDTH, -TILE_HEIGHT, win)
tile_group.add(t)

# FUNCTIONS ******************************************************************

def get_speed(score):
	return 200 + 5 * score

# VARIABLES ******************************************************************

num_tiles = 1
score = 0
speed = 1

clicked = False
pos = None

running = True
while running:
	pos = None
	win.blit(bg_img, (0,0))
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
				tile.alive = False
				score += 1

	if len(tile_group) > 0:
		t = tile_group.sprites()[-1]
		if t.rect.top + speed >= 0:
			x = random.randint(0, 3)
			y = -TILE_HEIGHT - (0 - t.rect.top)
			t = Tile(x * TILE_WIDTH, y, win)
			tile_group.add(t)
			num_tiles += 1

	for i in range(4):
		pygame.draw.line(win, WHITE, (TILE_WIDTH * i, 0), (TILE_WIDTH*i, HEIGHT), 1)

	speed = int(get_speed(score) * (FPS / 1000))

	clock.tick(FPS)
	pygame.display.update()

pygame.quit()