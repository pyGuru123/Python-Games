import os
import pygame
from pygame.locals import *

from objects import Ball, World, load_level

SIZE = WIDTH, HEIGHT = 192, 192
tile_size = 16

pygame.init()
win = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Bounce')
clock = pygame.time.Clock()
FPS = 30


# game variables

ROWS = 12
MAX_COLS = 150
TILE_SIZE = 16

# COLORS
BLUE = 175, 207, 240

# scroll variables
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 0.5

# world data
level = 1
max_level = len(os.listdir('levels/'))
level_data = load_level(level)

ppos = (18, 170)
ball = Ball(win, ppos)
world = World(win, level_data)

running = True
while running:
	win.fill(BLUE)
	scroll = world.draw(scroll_left, scroll_right, scroll)

	for event in pygame.event.get():
		if event.type == QUIT:
			running = False

	pressed_keys = pygame.key.get_pressed()	
	scroll_left, scroll_right = ball.update(pressed_keys, scroll_left, scroll_right)


	clock.tick(FPS)
	pygame.display.update()

pygame.quit()