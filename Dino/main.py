# Dino

# Author : Prajjwal Pathak (pyguru)
# Date : Sunday, 17 October, 2021

import random
import pygame

from objects import Ground, Dino, Cactus, Cloud, Ptera

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
ptera_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()

# FUNCTIONS ******************************************************************

def reset():
	global counter, SPEED

	counter = 0
	SPEED = 5

	cactus_group.empty()
	ptera_group.empty()
	cloud_group.empty()

	dino.reset()

# VARIABLES ******************************************************************

counter = 0
enemy_time = 100
cloud_time = 500

SPEED = 5
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

			if event.key == pygame.K_SPACE:
				if dino.alive:
					jump = True
				else:
					reset()

			if event.key == pygame.K_UP:
				jump = True

			if event.key == pygame.K_DOWN:
				duck = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
				jump = False

			if event.key == pygame.K_DOWN:
				duck = False 

	counter += 1
	if counter % enemy_time == 0:
		if random.randint(1, 10) == 5:
			y = random.choice([85, 130])
			ptera = Ptera(WIDTH, y)
			ptera_group.add(ptera)
		else:
			type = random.randint(1, 4)
			cactus = Cactus(type)
			cactus_group.add(cactus)

	if counter % cloud_time == 0:
		y = random.randint(20, 100)
		cloud = Cloud(WIDTH, y)
		cloud_group.add(cloud)

	if counter % 100 == 0:
		SPEED += 0.2
		enemy_time -= 1

	ground.update(SPEED)
	ground.draw(win)
	cactus_group.update(SPEED)
	cactus_group.draw(win)
	ptera_group.update(SPEED-1)
	ptera_group.draw(win)
	cloud_group.update(SPEED-3)
	cloud_group.draw(win)
	dino.update(jump, duck)
	dino.draw(win)

	for cactus in cactus_group:
		if pygame.sprite.collide_mask(dino, cactus):
			SPEED = 0
			dino.alive = False

	if pygame.sprite.spritecollide(dino, ptera_group, False):
		SPEED = 0
		dino.alive = False

	pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 4)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()