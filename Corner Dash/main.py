# Corner Dash

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 23 November, 2021

import math
import random
import pygame

from objects import Circle, Player, Dot, Particle, Snowflake, \
					ScoreCard
 
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

# COLORS *********************************************************************

RED = (255,0,0)
GREEN = (0,177,64)
BLUE = (30, 144,255)
ORANGE = (252,76,2)
YELLOW = (254,221,0)
PURPLE = (155,38,182)
AQUA = (0,103,127)
WHITE = (255, 255, 255)
BLACK = (20,20,20)
GRAY = (128,128,128)

color_list = [BLUE, GREEN, ORANGE, YELLOW]
color_index = 3
color = color_list[color_index]

# IMAGES *********************************************************************

main_circle = pygame.image.load('Assets/main.png')
leaf = 'Assets/flake.png'

# FONTS **********************************************************************

score_font = "Fonts/neuropol x rg.ttf"
score_msg = ScoreCard(WIDTH//2, 60, 30, score_font, WHITE, win)

# GROUP & OBJECTS ************************************************************

flake_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()
circle_group = pygame.sprite.Group()
for i in range(12):
	c = Circle(i)
	circle_group.add(c)

p = Player()
d = Dot()
pos = random.randint(0, 11)
dot_circle = circle_group.sprites()[pos]

# TIMER **********************************************************************

start_time = pygame.time.get_ticks()

# VARIABLES ******************************************************************

clicked = False
rotate = True
clicks = 0
shrink = False
score = 0

home_page = False
game_page = True
score_page = False

running = True
while running:
	win.fill(BLACK)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			if not clicked :
				clicked = True
				rotate = False
				clicks += 1

		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
			rotate = True

	if home_page:
		pass

	if score_page:
		pass

	if game_page:
		win.blit(main_circle, (CENTER[0] - 12.5, CENTER[1] - 12.5))

		score_msg.update(score)

		particle_group.update()
		# flake_group.update(win)
		circle_group.update(shrink)
		circle_group.draw(win)
		p.update(rotate)
		p.draw(win)

		if score and score % 7 == 0:
			shrink = not shrink

		if clicks and clicks % 5 == 0:
			color_index = (color_index + 1) % len(color_list)
			color = color_list[color_index]
			r = random.choice([-1, 1])
			for c in circle_group:
				c.dt *= -r
				c.rotate = True

			x = random.randint(40, WIDTH-40)
			y = 0
			flake = Snowflake(x, y, leaf)
			flake_group.add(flake)

			clicks = 0

		x, y = dot_circle.rect.center
		d.update(x, y, win, color)

		for circle in circle_group:
			if circle.complete:
				if pygame.sprite.collide_mask(p, circle):
					print(circle.i)
					if circle.i == pos:
						pos = random.randint(0, 11)

						x, y = circle.rect.center
						for i in range(10):
							particle = Particle(x, y, color, win)
							particle_group.add(particle)

						score += 1
					p.dr *= -1

		x, y = p.rect.center
		if (x < 0 or x > WIDTH or y < 0 or y > HEIGHT):
			for i in range(10):
				particle = Particle(x, y, WHITE, win)
				particle_group.add(particle)
			p.reset()

	pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 8)
	clock.tick(FPS)
	pygame.display.update()

running = False