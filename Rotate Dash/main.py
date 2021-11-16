# Rotate Dash

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 15 November, 2021

import random
import pygame

from objects import Ball, Line, Circle, Square, get_circle_position, \
					Particle, ScoreCard

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
BLACK = (30,30,30)
GRAY = (128,128,128)

color_list = [BLUE, GREEN, RED, ORANGE, YELLOW, PURPLE]
color_index = 0
color = color_list[color_index]

# FONTS ***********************************************************************

score_font = "Fonts/DroneflyRegular-K78LA.ttf"
score_msg = ScoreCard(WIDTH//2, 60, 50, score_font, BLACK, win)

# SOUNDS **********************************************************************

score_fx = pygame.mixer.Sound('Sounds/click.wav')
score_fx.set_volume(0.2)
score_page_fx = pygame.mixer.Sound('Sounds/score_page.mp3')
explode_fx = pygame.mixer.Sound('Sounds/explode.wav')

pygame.mixer.music.load('Sounds/music.wav')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.5)

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

inner_center = [WIDTH//2,HEIGHT//2]

clicked = False
start_rotation = False
counter = 0
clicks = 0
score = 0

home_page = False
game_page = True
score_page = False

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
				if not start_rotation:
					start_rotation = True

				clicked = True
				clicks += 1

				ball.dtheta *= -1

		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = False

	if home_page:
		pass

	if score_page:
		pass

	if game_page:
		counter += 1
		if counter % 200 == 0:
			square = Square(win)
			square_group.add(square)
			counter = 0

		if clicks and clicks % 5 == 0:
			color_index = (color_index + 1) % len(color_list)
			color = color_list[color_index]
			clicks = 0

		particle_group.update()
		if ball.alive:
			square_group.update()
			ball.update(color, start_rotation)
			line_group.update(color)
			circle_group.update()
			score_msg.update(score)

		if pygame.sprite.spritecollide(ball, line_group, True):
			if line_type == 1:
				line_type = 2
			else:
				line_type = 1
			line = Line(line_type, win)
			line_group.add(line)

			score += 1
			score_fx.play()
			score_msg.animate = True

		if pygame.sprite.spritecollide(ball, circle_group, False) and ball.alive:
			ball.alive = False
			x, y = ball.rect.center
			for i in range(15):
				particle = Particle(x, y, color, win)
				particle_group.add(particle)
			explode_fx.play()

		if not ball.alive:
			inner_center[1] -= 10
			if inner_center[1] <= -120:
				score_page = True
				game_page = False
				score_page_fx.play()

		pygame.draw.circle(win, BLACK, inner_center, 35)
		if clicks % 3 == 0:
			pygame.draw.circle(win, color, inner_center, 118, 5)
		pygame.draw.circle(win, BLACK, inner_center, 120, 5)

	pygame.draw.rect(win, BLACK, (0, 0, WIDTH, HEIGHT), 8)
	clock.tick(FPS)
	pygame.display.update()

running = False