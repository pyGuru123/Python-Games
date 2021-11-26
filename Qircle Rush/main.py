# Corner Dash

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 23 November, 2021

import math
import random
import pygame

from objects import Circle, Player, Dot, Particle, Snowflake, \
					ScoreCard, Button, Message, BlinkingText
 
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

# FONTS **********************************************************************

score_font = "Fonts/neuropol x rg.ttf"
title_font = 'Fonts/AvQest.ttf'
score_msg = ScoreCard(WIDTH//2, 60, 35, score_font, WHITE, win)
final_score_msg = Message(144, HEIGHT//2-50, 100, "0", score_font, WHITE, win)
new_high_msg = Message(WIDTH//2, HEIGHT//2+20, 16, "NEW HIGH!", score_font, WHITE, win)
qircle_msg = Message(WIDTH-160, 150, 80, "Qircle", title_font, WHITE, win)
dash_msg = Message(WIDTH-100, 220, 60, "Rush", title_font, WHITE, win)
tap_to_play = BlinkingText(WIDTH//2, HEIGHT-60, 20, "Tap To Play", None, WHITE, win)

# SOUNDS *********************************************************************

dash_fx = pygame.mixer.Sound('Sounds/dash.mp3')
click_fx = pygame.mixer.Sound('Sounds/click.mp3')
dead_fx = pygame.mixer.Sound('Sounds/dead.mp3')
score_page_fx = pygame.mixer.Sound('Sounds/score_page.mp3')

pygame.mixer.music.load('Sounds/music.wav')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.3)

# IMAGES *********************************************************************

main_circle = pygame.image.load('Assets/main.png')
flake_img = 'Assets/flake.png'

close_img = pygame.image.load('Assets/closeBtn.png')
replay_img = pygame.image.load('Assets/replay.png')
sound_off_img = pygame.image.load("Assets/soundOffBtn.png")
sound_on_img = pygame.image.load("Assets/soundOnBtn.png")

# Buttons ********************************************************************

close_btn = Button(close_img, (24, 24), WIDTH // 4 - 18, HEIGHT//2 + 120)
replay_btn = Button(replay_img, (36,36), WIDTH // 2  - 18, HEIGHT//2 + 115)
sound_btn = Button(sound_on_img, (24, 24), WIDTH - WIDTH // 4 - 18, HEIGHT//2 + 120)

# GROUP & OBJECTS ************************************************************

flake_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()
circle_group = pygame.sprite.Group()

p = Player()
d = Dot()
pos = random.randint(0, 11)

# VARIABLES ******************************************************************

clicked = False
rotate = True
shrink = True
sound_on = True

clicks = 0
count = 50
score = 0
high_score = 0
score_list = []

home_page = True
game_page = False
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
			if home_page:
				home_page = False
				game_page = True

				for i in range(12):
					c = Circle(i)
					circle_group.add(c)

			elif game_page:
				if not clicked :
					clicked = True
					rotate = False
					clicks += 1
					click_fx.play()

		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
			rotate = True

	if home_page:
		count += 1
		if count % 100 == 0:
			x = random.randint(40, WIDTH-40)
			y = 0
			flake = Snowflake(x, y, flake_img)
			flake_group.add(flake)
			count = 0

		flake_group.update(win)
		qircle_msg.update()
		dash_msg.update()
		tap_to_play.update()
		
	if score_page:
		final_score_msg.update(score, YELLOW)
		if score and score >= high_score:
			high_score = score
			new_high_msg.update(shadow=False)

		if close_btn.draw(win):
			running = False

		if replay_btn.draw(win):
			clicks = 0
			score = 0
			pos = random.randint(0, 11)

			p.reset()
			final_score_msg = Message(144, HEIGHT//2-50, 100, "0", score_font, WHITE, win)

			score_page = False
			game_page = True

		if sound_btn.draw(win):
			pass
			sound_on = not sound_on
			
			if sound_on:
				sound_btn.update_image(sound_on_img)
				pygame.mixer.music.play(loops=-1)
			else:
				sound_btn.update_image(sound_off_img)
				pygame.mixer.music.stop()

	if game_page:
		win.blit(main_circle, (CENTER[0] - 12.5, CENTER[1] - 12.5))

		score_msg.update(score)

		particle_group.update()
		circle_group.update(shrink)
		circle_group.draw(win)
		p.update(rotate)
		p.draw(win)

		if p.alive:
			if score and score % 7 == 0:
				if score not in score_list:
					score_list.append(score)
					shrink = not shrink

			if clicks and clicks % 5 == 0:
				color_index = (color_index + 1) % len(color_list)
				color = color_list[color_index]

				r = random.choice([-1, 1])
				for c in circle_group:
					c.dt *= -r
					c.rotate = True

				clicks = 0

			dot_circle = circle_group.sprites()[pos]
			x, y = dot_circle.rect.center
			d.update(x, y, win, color)

			for circle in circle_group:
				if circle.complete:
					if pygame.sprite.collide_mask(p, circle):
						if circle.i == pos:
							pos = random.randint(0, 11)

							x, y = circle.rect.center
							for i in range(10):
								particle = Particle(x, y, color, win)
								particle_group.add(particle)

							score += 1
							dash_fx.play()
						p.dr *= -1

			x, y = p.rect.center
			if (x < 0 or x > WIDTH or y < 0 or y > HEIGHT):
				for i in range(10):
					particle = Particle(x, y, WHITE, win)
					particle_group.add(particle)
				p.alive = False
				dead_fx.play()

		if not p.alive and len(particle_group) == 0:
			particle_group.empty()

			game_page = False
			score_page = True
			score_page_fx.play()

	pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 8)
	clock.tick(FPS)
	pygame.display.update()

running = False