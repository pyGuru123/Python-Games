# Hyper Dash

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 29 July, 2021

import random
import pygame

from objects import Tile, Player, Path

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2
# | pygame.SCALED | pygame.FULLSCREEN
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
pygame.display.set_caption('Arc Dash')

clock = pygame.time.Clock()
FPS = 60

# COLORS **********************************************************************

RED = (255,0,0)
GREEN = (0,177,64)
BLUE = (30, 144,255)
ORANGE = (252,76,2)
YELLOW = (254,221,0)
PURPLE = (155,38,182)
AQUA = (0,103,127)
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (32, 32, 32)

color_list = [RED, GREEN, BLUE, ORANGE, YELLOW, PURPLE]
color_index = 0
color = color_list[color_index]

# Images **********************************************************************


# OBJECTS *********************************************************************

tile_group = pygame.sprite.Group()

for i in range(8):
	tile = Tile(i, 1, win)
	tile_group.add(tile)
	tile = Tile(i, 2, win)
	tile_group.add(tile)

p = Player(win)
path = Path(p, tile_group, win)

clicked = False
num_clicks = 0
index = None

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

		if event.type == pygame.MOUSEBUTTONDOWN:
			if not clicked:
				pos = event.pos
				for tile in tile_group:
					if tile.rect.collidepoint(pos):
						tile.color = ORANGE
						tile.is_deadly = True
						type_ = tile.type
						index = tile.index
						x = tile.rect.centerx
						if type_ == 1:
							y = tile.rect.bottom
						elif type_ == 2:
							y = tile.rect.top
						p.set_move(x, y, index, type_)

				num_clicks += 1
				if num_clicks % 5 == 0:
					color_index += 1
					if color_index > len(color_list) - 1:
						color_index = 0

					color = color_list[color_index]

		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = False

	if pygame.sprite.spritecollide(p, tile_group, False):
		p.shadow()
		path.update()
	else:
		path.reset()
	tile_group.update()
	p.update(color)

	pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 5, border_radius=10)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()