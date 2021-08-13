# Connected

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 8 August, 2021

import random
import pygame

from objects import Balls, Coins, Tiles

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
pygame.display.set_caption('Arc Dash')

clock = pygame.time.Clock()
FPS = 90

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
GRAY = (25, 25, 25)

color_list = [PURPLE, GREEN, BLUE, ORANGE, YELLOW, RED]
color_index = 0
color = color_list[color_index]

# SOUNDS **********************************************************************

flip_fx = pygame.mixer.Sound('Sounds/flip.mp3')
score_fx = pygame.mixer.Sound('Sounds/point.mp3')

# Groups **********************************************************************

RADIUS = 70
ball_group = pygame.sprite.Group()

ball = Balls((CENTER[0], CENTER[1]+RADIUS), RADIUS, 90, win)
ball_group.add(ball)
ball = Balls((CENTER[0], CENTER[1]-RADIUS), RADIUS, 270, win)
ball_group.add(ball)

coin_group = pygame.sprite.Group()
y = random.randint(CENTER[1]-RADIUS, CENTER[1]+RADIUS)
coin = Coins(y, win)
coin_group.add(coin)

tile_group = pygame.sprite.Group()
y = random.randint(CENTER[1]-100, CENTER[1]+100)
type_ = 3
t = Tiles(y, type_, win)
tile_group.add(t)

# VARIABLES *******************************************************************

clicked = False
num_clicks = 0
score = 0

running = True
while running:
	new_coin = False
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
				clicked = True
				for ball in ball_group:
					ball.dtheta *= -1
					flip_fx.play()

				num_clicks += 1
				if num_clicks % 5 == 0:
					color_index += 1
					if color_index > len(color_list) - 1:
						color_index = 0

					color = color_list[color_index]

		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = False

	pygame.draw.circle(win, BLACK, CENTER, 80, 20)
	ball_group.update(color)
	coin_group.update(color)
	tile_group.update()

	if pygame.sprite.groupcollide(ball_group, coin_group, False, True):
		new_coin = True
		score_fx.play()
		score += 1

	if len(coin_group) == 0:
		new_coin = True

	if new_coin:
		y = random.randint(CENTER[1]-RADIUS, CENTER[1]+RADIUS)
		coin = Coins(y, win)
		coin_group.add(coin)

	if score % 5 == 0:
		FPS = 120
	else:
		FPS = 90

	pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 5, border_radius=10)
	clock.tick(FPS)
	pygame.display.update()


pygame.quit()