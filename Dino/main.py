# Dino

# Author : Prajjwal Pathak (pyguru)
# Date : Sunday, 17 October, 2021

import random
import pygame

from objects import Ground, Dino, Cactus, Cloud

pygame.init()
SCREEN = WIDTH, HEIGHT = (600, 200)
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)

clock = pygame.time.Clock()
FPS = 60

# COLORS *********************************************************************

WHITE = (225,225,225)
BLACK = (0, 0, 0)
GRAY = (32, 33, 36)

# OBJECTS & GROUPS ***********************************************************

ground = Ground()
dino = Dino(50, 160)

cactus_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()

# VARIABLES ******************************************************************

counter = 0
cactus_time = 100
cloud_time = 500

SPEED = 6
jump = False
duck = False

running = True
while running:
	win.fill(GRAY)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

			if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
				jump = True

			if event.key == pygame.K_DOWN:
				duck = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
				jump = False

			if event.key == pygame.K_DOWN:
				duck = False

	counter += 1
	if counter % cactus_time == 0:
		type = random.randint(1, 4)
		cactus = Cactus(type)
		cactus_group.add(cactus)
		# ctime = random.randint(200,250)

	if counter % cloud_time == 0:
		y = random.randint(20, 100)
		cloud = Cloud(WIDTH, y)
		cloud_group.add(cloud)

	ground.update(SPEED)
	ground.draw(win)
	cactus_group.update(SPEED)
	cactus_group.draw(win)
	cloud_group.update(2)
	cloud_group.draw(win)
	dino.update(jump, duck)
	dino.draw(win)

	pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 4)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()