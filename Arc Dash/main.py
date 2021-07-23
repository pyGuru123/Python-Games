# Arc Dash

# Author : Prajjwal Pathak (pyguru)
# Date : Saturday, 22 July, 2021

import random
import pygame

from objects import Player, Balls, Dot, Shadow

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2
# | pygame.SCALED | pygame.FULLSCREEN
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
pygame.display.set_caption('Arc Dash')

clock = pygame.time.Clock()
FPS = 60

# COLORS

RED = (255, 0, 0)
BLUE = (30, 144, 255)
WHITE = (255, 255, 255)

# GAME VARIABLES

MAX_RAD = 120
rad_delta = 50

# OBJECTS 

ball_group = pygame.sprite.Group()
dot_group = pygame.sprite.Group()
shadow_group = pygame.sprite.Group()
p = Player(win)

ball_positions = [(CENTER[0]-105, CENTER[1]), (CENTER[0]+105, CENTER[1]),
					(CENTER[0]-45, CENTER[1]), (CENTER[0]+45, CENTER[1]),
					(CENTER[0], CENTER[1]-75), (CENTER[0], CENTER[1]+75)]
for index, pos in enumerate(ball_positions):
	if index in (4,5):
		type_ = 2
	else:
		type_ = 1
	ball = Balls(pos, type_, win)
	ball_group.add(ball)

dot_list = [(CENTER[0], CENTER[1]-MAX_RAD+3), (CENTER[0]+MAX_RAD-3, CENTER[1]),
			(CENTER[0], CENTER[1]+MAX_RAD-3), (CENTER[0]-MAX_RAD+3, CENTER[1])]
dot_index = random.choice([1,2,3,4])
dot_pos = dot_list[dot_index-1]
dot = Dot(*dot_pos, win)
dot_group.add(dot)


shadow = Shadow(dot_index, win)
shadow_group.add(shadow)



color = RED
clicked = False

running = True
while running:
	win.fill(color)

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

				dot_group.empty()
				dot_index = random.randint(1,4)
				dot_pos = dot_list[dot_index-1]
				dot = Dot(*dot_pos, win)
				dot_group.add(dot)

				print(dot_index)

				shadow_group.empty()
				shadow = Shadow(dot_index, win)
				shadow_group.add(shadow)

		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = False

	for radius in [30 + rad_delta, 60 + rad_delta, 90 + rad_delta, 120 + rad_delta]:
		if rad_delta > 0:
			radius -= 1
			rad_delta -= 1
		pygame.draw.circle(win, (0,0,0), CENTER, radius, 5)

	pygame.draw.rect(win, color, [CENTER[0]-10, CENTER[1]-MAX_RAD, 20, MAX_RAD*2])
	pygame.draw.rect(win, color, [CENTER[0]-MAX_RAD, CENTER[1]-10, MAX_RAD*2, 20])

	if rad_delta <= 0:
		p.update(color)
		shadow_group.update()
		ball_group.update()
		dot_group.update()

	pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 5, border_radius=10)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()