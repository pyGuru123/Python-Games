# Rotate Dash

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 15 November, 2021

import random
import pygame

from objects import Ball, Line, Circle, Square, get_circle_position, \
					Particle

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

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
WHITE = (200,200,200)
BLACK = (0,0,0)
GRAY = (128,128,128)

color_list = [RED, GREEN, BLUE, ORANGE, YELLOW, PURPLE]
color_index = 0
color = color_list[color_index]

# Groups **********************************************************************

line_group = pygame.sprite.Group()
circle_group = pygame.sprite.Group()
square_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()


RADIUS = 70
ball = Ball((CENTER[0], CENTER[1]+RADIUS), RADIUS, 90, win)

line_type = random.randint(1, 2)
line = Line(line_type, win)
line_group.add(line)

for i in range(4):
	angle = 45 * (2*(i+1) - 1)
	x, y = get_circle_position(angle)
	circle = Circle(x, y, i+1, win)
	circle_group.add(circle)

clicked = False
counter = 0
score = 1

running = True
while running:
	win.fill(WHITE)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			if not clicked:
				clicked = True
				ball.dtheta *= -1

		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = False

	counter += 1
	if counter % 200 == 0:
		square = Square(win)
		square_group.add(square)
		counter = 0

	square_group.update()
	ball.update(BLUE)
	line_group.update()
	circle_group.update()
	particle_group.update()

	if pygame.sprite.spritecollide(ball, line_group, True):
		if line_type == 1:
			line_type = 2
		else:
			line_type = 1
		line = Line(line_type, win)
		line_group.add(line)
		score += 1

	if pygame.sprite.spritecollide(ball, circle_group, False) and ball.alive:
		ball.alive = False
		x, y = ball.rect.center
		for i in range(20):
			particle = Particle(x, y, BLUE, win)
			particle_group.add(particle)

	pygame.draw.circle(win, BLACK, (WIDTH//2, HEIGHT//2), 35)
	pygame.draw.circle(win, BLACK, (WIDTH//2, HEIGHT//2), 120, 5)

	pygame.draw.rect(win, BLACK, (0, 0, WIDTH, HEIGHT), 5)
	clock.tick(FPS)
	pygame.display.update()

running = False