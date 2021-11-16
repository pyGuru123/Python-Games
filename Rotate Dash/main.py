# Rotate Dash

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 15 November, 2021

import random
import pygame

from objects import Ball, Line, Circle, Square, get_circle_position, \
					Particle, ScoreCard, Button, Message, rotate_image, \
					BlinkingText

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
WHITE = (200,200,200)
BLACK = (30,30,30)
GRAY = (128,128,128)

score_bg = 128

color_list = [BLUE, GREEN, RED, ORANGE, YELLOW, PURPLE]
color_index = 0
color = color_list[color_index]

# FONTS **********************************************************************

score_font = "Fonts/DroneflyRegular-K78LA.ttf"
final_score_font = "Fonts/BubblegumSans-Regular.ttf"
new_high_font = "Fonts/DalelandsUncialBold-82zA.ttf"
title_font = "Fonts/Aladin-Regular.ttf"

f = pygame.font.Font(title_font, 45)
r_msg = f.render('R', 'True', RED)
r_rect = r_msg.get_rect()
r_rect.x = 90
r_rect.y = (HEIGHT // 2) - 190 

otate_msg = f.render('OTATE', True, GREEN)
dash_msg = f.render('DASH', True, BLUE)
final_score_msg = Message(144, HEIGHT//2-50, 100, "0",final_score_font, WHITE, win)
new_high_msg = Message(WIDTH//2, HEIGHT//2+10, 20, "NEW HIGH", new_high_font, WHITE, win)
tap_to_play = BlinkingText(WIDTH//2, HEIGHT-60, 20, "Tap To Play", None, BLACK, win)

score_msg = ScoreCard(WIDTH//2, 60, 50, score_font, BLACK, win)

# SOUNDS *********************************************************************

score_fx = pygame.mixer.Sound('Sounds/click.wav')
score_fx.set_volume(0.2)
score_page_fx = pygame.mixer.Sound('Sounds/score_page.mp3')
explode_fx = pygame.mixer.Sound('Sounds/explode.wav')

pygame.mixer.music.load('Sounds/music.wav')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.7)

# Button images **************************************************************

close_img = pygame.image.load('Assets/closeBtn.png')
replay_img = pygame.image.load('Assets/replay.png')
sound_off_img = pygame.image.load("Assets/soundOffBtn.png")
sound_on_img = pygame.image.load("Assets/soundOnBtn.png")

# Buttons ********************************************************************

close_btn = Button(close_img, (24, 24), WIDTH // 4 - 18, HEIGHT//2 + 120)
replay_btn = Button(replay_img, (36,36), WIDTH // 2  - 18, HEIGHT//2 + 115)
sound_btn = Button(sound_on_img, (24, 24), WIDTH - WIDTH // 4 - 18, HEIGHT//2 + 120)

# Groups *********************************************************************

line_group = pygame.sprite.Group()
circle_group = pygame.sprite.Group()
square_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()

RADIUS = 70
ball = Ball((CENTER[0], CENTER[1]+RADIUS), RADIUS, 90, win)

line_type = 1
line = Line(line_type, win)
line_group.add(line)

# VARIABLES ******************************************************************

inner_center = [WIDTH//2,HEIGHT//2]

clicked = False
start_rotation = False
sound_on = True
counter = 0
circle_count = 0
clicks = 0
score = 0
high_score = 0

angle = 0

home_page = True
game_page = False
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
			if home_page:
				ball.alive = True
				ball.reset()

				home_page = False
				game_page = True

			elif game_page:
				if not clicked :
					if not start_rotation:
						start_rotation = True

					clicked = True
					clicks += 1

					ball.dtheta *= -1

					if len(circle_group) < 4:
						circle_count += 1
						angle = 45 * (2 * circle_count - 1)
						x, y = get_circle_position(angle)
						circle = Circle(x, y, circle_count, win)
						circle_group.add(circle)

		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = False

	if home_page:
		image, rect, angle = rotate_image(r_msg, r_rect, angle)
		win.blit(image, rect)
		win.blit(otate_msg, (120, HEIGHT//2 - 190))
		win.blit(dash_msg, (140, HEIGHT//2 - 140))

		ball.alive = True
		ball.update(color, True)

		tap_to_play.update()

	if score_page:
		if score_bg > 40:
			score_bg -= 1
		win.fill((score_bg, score_bg, score_bg))

		if score and score > high_score:
			high_score = score
			new_high_msg.update(shadow=False)

		final_score_msg.update(score, color)

		if close_btn.draw(win):
			running = False

		if replay_btn.draw(win):
			clicks = 0
			ball.reset()
			start_rotation = False
			score = 0
			final_score_msg = Message(144, HEIGHT//2-50, 100, "0",final_score_font, WHITE, win)

			score_page = False
			game_page = True

			inner_center = [WIDTH//2,HEIGHT//2]
			line_type = 1
			line = Line(line_type, win)
			line_group.add(line)

		if sound_btn.draw(win):
			sound_on = not sound_on
			
			if sound_on:
				sound_btn.update_image(sound_on_img)
				pygame.mixer.music.play(loops=-1)
			else:
				sound_btn.update_image(sound_off_img)
				pygame.mixer.music.stop()

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
				score_bg = 128

				particle_group.empty()
				line_group.empty()

		pygame.draw.circle(win, BLACK, inner_center, 35)
		if clicks % 3 == 0:
			pygame.draw.circle(win, color, inner_center, 118, 5)
		pygame.draw.circle(win, BLACK, inner_center, 120, 5)

	pygame.draw.rect(win, BLACK, (0, 0, WIDTH, HEIGHT), 8)
	clock.tick(FPS)
	pygame.display.update()

running = False