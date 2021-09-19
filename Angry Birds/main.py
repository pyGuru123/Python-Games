import os
import sys
import math
import time
import pygame
import pymunk
from characters import Bird, Pig
from objects import SlingShot

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
pig_image = pygame.image.load('res/pig.png')

# OBJECTS *********************************************************************

space = pymunk.Space()
space.gravity = (0, -700)

pigs = []
birds = []
beams = []
columns = []

sling_x, sling_y = 135, 100
sling = SlingShot(sling_x, sling_y)

# FLOOR ***********************************************************************

static_floor = pymunk.Body(body_type=pymunk.Body.STATIC)
static_lines = [pymunk.Segment(static_floor, (0,60), (800, 60), 0), 
				pymunk.Segment(static_floor, (WIDTH- 10,60), (WIDTH-10, HEIGHT), 0)]

for line in static_lines:
	line.elasticity = 0.95
	line.friction = 1
	line.collision_type = 3

space.add(static_floor, *static_lines)

# SLING ACTION ****************************************************************

mouse_distance = 0
rope_length = 90

angle = 0
mouse_x = 0
mouse_y = 0

mouse_pressed = False
time_of_release = 0

running = True
while running:
	win.blit(bg, (0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

	sling.draw(win)

	pygame.display.update()

pygame.quit()