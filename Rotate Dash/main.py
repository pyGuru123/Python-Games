# Rotate Dash

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 15 November, 2021

import random
import pygame

from objects import Ball, Line

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

color_list = [RED, GREEN, BLUE, ORANGE, YELLOW, PURPLE]
color_index = 0
color = color_list[color_index]

# Groups **********************************************************************

line_group = pygame.sprite.Group()

RADIUS = 70
ball = Ball((CENTER[0], CENTER[1]+RADIUS), RADIUS, 90, win)
# ball_group.add(ball)

line = Line(1, win)
line_group.add(line)

clicked = False

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
				for ball in ball_group:
					ball.dtheta *= -1

		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = False

	pygame.draw.circle(win, BLACK, (WIDTH//2, HEIGHT//2), 35)
	pygame.draw.circle(win, BLACK, (WIDTH//2, HEIGHT//2), 120, 5)

	ball.update(BLUE)
	line_group.update()

	pygame.draw.rect(win, BLACK, (0, 0, WIDTH, HEIGHT), 5)
	clock.tick(FPS)
	pygame.display.update()

running = False