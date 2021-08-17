# Connected

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 8 August, 2021

import random
import pygame

from objects import Balls, Coins, Tiles, Particle, Message, Button

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
pygame.display.set_caption('Connected')

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
dead_fx = pygame.mixer.Sound('Sounds/dead.mp3')
score_page_fx = pygame.mixer.Sound('Sounds/score_page.mp3')

pygame.mixer.music.load('Sounds/bgm.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.5)


# FONTS ***********************************************************************

title_font = "Fonts/Aladin-Regular.ttf"
score_font = "Fonts/DroneflyRegular-K78LA.ttf"
game_over_font = "Fonts/ghostclan.ttf"
final_score_font = "Fonts/DalelandsUncialBold-82zA.ttf"
new_high_font = "Fonts/BubblegumSans-Regular.ttf"


connected = Message(WIDTH//2, 120, 55, "ConnecteD", title_font, WHITE, win)
score_msg = Message(WIDTH//2, 100, 60, "0", score_font, (150, 150, 150), win)
game_msg = Message(80, 150, 40, "GAME", game_over_font, BLACK, win)
over_msg = Message(210, 150, 40, "OVER!", game_over_font, WHITE, win)
final_score = Message(WIDTH//2, HEIGHT//2, 90, "0", final_score_font, RED, win)
new_high_msg = Message(WIDTH//2, HEIGHT//2+60, 20, "New High", None, GREEN, win)

# Button images

home_img = pygame.image.load('Assets/homeBtn.png')
replay_img = pygame.image.load('Assets/replay.png')
sound_off_img = pygame.image.load("Assets/soundOffBtn.png")
sound_on_img = pygame.image.load("Assets/soundOnBtn.png")
easy_img = pygame.image.load("Assets/easy.jpg")
hard_img = pygame.image.load("Assets/hard.jpg")

# Buttons

easy_btn = Button(easy_img, (70, 24), WIDTH//4-10, HEIGHT-100)
hard_btn = Button(hard_img, (70, 24), WIDTH//2 + 10, HEIGHT-100)
home_btn = Button(home_img, (24, 24), WIDTH // 4 - 18, HEIGHT//2 + 120)
replay_btn = Button(replay_img, (36,36), WIDTH // 2  - 18, HEIGHT//2 + 115)
sound_btn = Button(sound_on_img, (24, 24), WIDTH - WIDTH // 4 - 18, HEIGHT//2 + 120)

# Groups **********************************************************************

RADIUS = 70
ball_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()

ball = Balls((CENTER[0], CENTER[1]+RADIUS), RADIUS, 90, win)
ball_group.add(ball)
ball = Balls((CENTER[0], CENTER[1]-RADIUS), RADIUS, 270, win)
ball_group.add(ball)

# TIME ************************************************************************

start_time = pygame.time.get_ticks()
current_time = 0
coin_delta = 850
tile_delta = 2000

# VARIABLES *******************************************************************

clicked = False
new_coin = True
num_clicks = 0
score = 0

player_alive = True
score = 0
highscore = 0
sound_on = True
easy_level = True

home_page = True
game_page = False
score_page = False

running = True
while running:
	win.fill(GRAY)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

		if event.type == pygame.MOUSEBUTTONDOWN and game_page:
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

		if event.type == pygame.MOUSEBUTTONDOWN and game_page:
			clicked = False

	if home_page:
		connected.update()

		pygame.draw.circle(win, BLACK, CENTER, 80, 20)
		ball_group.update(color)

		if easy_btn.draw(win):
			ball_group.empty()
			ball = Balls((CENTER[0], CENTER[1]+RADIUS), RADIUS, 90, win)
			ball_group.add(ball)

			home_page = False
			game_page = True
			easy_level = True

		if hard_btn.draw(win):
			ball_group.empty()
			ball = Balls((CENTER[0], CENTER[1]+RADIUS), RADIUS, 90, win)
			ball_group.add(ball)
			ball = Balls((CENTER[0], CENTER[1]-RADIUS), RADIUS, 270, win)
			ball_group.add(ball)

			home_page = False
			game_page = True
			easy_level = False

	if score_page:
		game_msg.update()
		over_msg.update()

		if score:
			final_score.update(score, color)
		else:
			final_score.update("0", color)
		if score and (score >= highscore):
			new_high_msg.update(shadow=False)

		if home_btn.draw(win):
			home_page = True
			score_page = False
			game_page = False
			player_alive = True
			score = 0
			score_msg = Message(WIDTH//2, 100, 60, "0", score_font, (150, 150, 150), win)
			
		if replay_btn.draw(win):
			home_page = False
			score_page = False
			game_page = True
			score = 0
			score_msg = Message(WIDTH//2, 100, 60, "0", score_font, (150, 150, 150), win)

			if easy_level:
				ball = Balls((CENTER[0], CENTER[1]+RADIUS), RADIUS, 90, win)
				ball_group.add(ball)
			else:
				ball = Balls((CENTER[0], CENTER[1]+RADIUS), RADIUS, 90, win)
				ball_group.add(ball)
				ball = Balls((CENTER[0], CENTER[1]-RADIUS), RADIUS, 270, win)
				ball_group.add(ball)

			player_alive = True


		if sound_btn.draw(win):
			sound_on = not sound_on
			
			if sound_on:
				sound_btn.update_image(sound_on_img)
				pygame.mixer.music.play(loops=-1)
			else:
				sound_btn.update_image(sound_off_img)
				pygame.mixer.music.stop()

	if game_page:
		pygame.draw.circle(win, BLACK, CENTER, 80, 20)
		ball_group.update(color)
		coin_group.update(color)
		tile_group.update()
		score_msg.update(score)
		particle_group.update()

		if player_alive:
			for ball in ball_group:
				if pygame.sprite.spritecollide(ball, coin_group, True):
					score_fx.play()
					score += 1
					if highscore <= score:
							highscore = score

					x, y = ball.rect.center
					for i in range(10):
						particle = Particle(x, y, color, win)
						particle_group.add(particle)

				if pygame.sprite.spritecollide(ball, tile_group, True):
					x, y = ball.rect.center
					for i in range(30):
						particle = Particle(x, y, color, win)
						particle_group.add(particle)

					player_alive = False
					dead_fx.play()

			current_time = pygame.time.get_ticks()
			delta = current_time- start_time
			if  coin_delta < delta < coin_delta + 100 and new_coin:
				y = random.randint(CENTER[1]-RADIUS, CENTER[1]+RADIUS)
				coin = Coins(y, win)
				coin_group.add(coin)
				new_coin = False

			if current_time- start_time >= tile_delta:
				y = random.choice([CENTER[1]-80, CENTER[1], CENTER[1]+80])
				type_ = random.randint(1,3)
				t = Tiles(y, type_, win)
				tile_group.add(t)

				start_time = current_time
				new_coin = True

		if not player_alive and len(particle_group) == 0:
			score_page = True
			game_page = False

			score_page_fx.play()

			ball_group.empty()
			tile_group.empty()
			coin_group.empty()

	pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT), 5, border_radius=10)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()