import os
import sys
import math
import time
import pygame
import pymunk
from characters import Bird, Pig

pygame.init()
WIDTH, HEIGHT = 800, 480
win = pygame.display.set_mode((WIDTH, HEIGHT))

# COLORS **********************************************************************

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# IMAGES **********************************************************************

bg = pygame.image.load('res/background3.png').convert_alpha()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
redbird_img = pygame.image.load('res/red-bird3.png').convert_alpha()
sling_image = pygame.image.load('res/sling-3.png').convert_alpha()
pig_image = pygame.image.load('res/pig.png')

# FUNCTIONS *******************************************************************

def convert_to_pygame(pos):
	return int(pos.x), int(-pos.y + HEIGHT)

# OBJECTS *********************************************************************

space = pymunk.Space()
space.gravity = (0, -700)

pigs = []
birds = []
beams = []
columns = []

# FLOOR ***********************************************************************

static_floor = pymunk.Body(body_type=pymunk.Body.STATIC)
static_lines1 = [pymunk.Segment(static_floor, (0,60), (800, 60), 0)]
static_lines2 = [pymunk.Segment(static_floor, (WIDTH- 10,60), (WIDTH-10, HEIGHT), 0)]

for line in static_lines1:
	line.elasticity = 0.95
	line.friction = 1
	line.collision_type = 3
for line in static_lines2:
	line.elasticity = 0.95
	line.friction = 1
	line.collision_type = 3

space.add(static_floor, static_lines1, static_lines2)

# SLING ACTION ****************************************************************

mouse_distance = 0
rope_length = 90

angle = 0
mouse_x = 0
mouse_y = 0

mouse_pressed = False
time_of_release = 0

sling_x, sling_y = 135, 100

running = True
while running:
	win.blit(bg, (0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

	win.blit(sling_image, (sling_x, sling_y))

	pygame.display.update()

pygame.quit()