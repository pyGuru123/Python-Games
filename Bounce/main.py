import os
import pygame

from player import Ball
from world import World, load_level

pygame.init()
WIDTH, HEIGHT = 192, 192
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption('Bounce')

clock = pygame.time.Clock()
FPS = 30

# GAME VARIABLES **************************************************************
ROWS = 12
MAX_COLS = 150
TILE_SIZE = 16

# COLORS **********************************************************************

BLUE = (175, 207, 240)

# Objects *********************************************************************

objects_list = []

# Load Level ******************************************************************
level = 1
world_data, level_length = load_level(level)

p = Ball(50, 50)
w = World(objects_list)
w.generate_world(world_data, win)

# VARIABLES *******************************************************************

moving_left = False
moving_right = False
screen_scroll = 0

running = True
while running:
	win.fill(BLUE)


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				moving_left = True
			if event.key == pygame.K_RIGHT:
				moving_right = True
			if event.key == pygame.K_UP:
				if not p.jump:
					p.jump = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				moving_left = False
			if event.key == pygame.K_RIGHT:
				moving_right = False

	w.draw_world(win, screen_scroll)
	p.update(moving_left, moving_right)
	p.draw(win)

	pygame.draw.rect(win, (255, 255,255), (0, 0, WIDTH, HEIGHT), 2, border_radius=5)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()