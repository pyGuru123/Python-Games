# Aeroblasters

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 30 September, 2021

import random
import pygame
from objects import Background, Player, Enemy, Bullet, Explosion, Fuel, \
					Powerup, Button, Message, BlinkingText

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512

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

WHITE = (255, 255, 255)
BLUE = (30, 144,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 20)

# IMAGES **********************************************************************

plane_img = pygame.image.load('Assets/plane.png')
logo_img = pygame.image.load('Assets/logo.png')
fighter_img = pygame.image.load('Assets/fighter.png')
clouds_img = pygame.image.load('Assets/clouds.png')
clouds_img = pygame.transform.scale(clouds_img, (WIDTH, 350))

home_img = pygame.image.load('Assets/Buttons/homeBtn.png')
replay_img = pygame.image.load('Assets/Buttons/replay.png')
sound_off_img = pygame.image.load("Assets/Buttons/soundOffBtn.png")
sound_on_img = pygame.image.load("Assets/Buttons/soundOnBtn.png")


# BUTTONS *********************************************************************

home_btn = Button(home_img, (24, 24), WIDTH // 4 - 18, HEIGHT//2 + 120)
replay_btn = Button(replay_img, (36,36), WIDTH // 2  - 18, HEIGHT//2 + 115)
sound_btn = Button(sound_on_img, (24, 24), WIDTH - WIDTH // 4 - 18, HEIGHT//2 + 120)


# FONTS ***********************************************************************

game_over_font = 'Fonts/ghostclan.ttf'
tap_to_play_font = 'Fonts/BubblegumSans-Regular.ttf'
score_font = 'Fonts/DalelandsUncialBold-82zA.ttf'
final_score_font = 'Fonts/DroneflyRegular-K78LA.ttf'

game_over_msg = Message(WIDTH//2, 230, 30, 'Game Over', game_over_font, WHITE, win)
score_msg = Message(WIDTH-50, 28, 30, '0', final_score_font, RED, win)
final_score_msg = Message(WIDTH//2, 280, 30, '0', final_score_font, RED, win)
tap_to_play_msg = tap_to_play = BlinkingText(WIDTH//2, HEIGHT-60, 25, "Tap To Play",
				 tap_to_play_font, WHITE, win)


# SOUNDS **********************************************************************

player_bullet_fx = pygame.mixer.Sound('Sounds/gunshot.wav')
click_fx = pygame.mixer.Sound('Sounds/click.mp3')
collision_fx = pygame.mixer.Sound('Sounds/mini_exp.mp3')
blast_fx = pygame.mixer.Sound('Sounds/blast.wav')
fuel_fx = pygame.mixer.Sound('Sounds/fuel.wav')

pygame.mixer.music.load('Sounds/Defrini - Spookie.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.1)


# GROUPS & OBJECTS ************************************************************

bg = Background(win)
p = Player(144, HEIGHT - 100)

enemy_group = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
fuel_group = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()

# FUNCTIONS *******************************************************************

def shoot_bullet():
	x, y = p.rect.center[0], p.rect.y

	if p.powerup > 0:
		for dx in range(-3, 4):
			b = Bullet(x, y, 4, dx)
			player_bullet_group.add(b)
		p.powerup -= 1
	else:
		b = Bullet(x-30, y, 6)
		player_bullet_group.add(b)
		b = Bullet(x+30, y, 6)
		player_bullet_group.add(b)
	player_bullet_fx.play()

def reset():
	enemy_group.empty()
	player_bullet_group.empty()
	enemy_bullet_group.empty()
	explosion_group.empty()
	fuel_group.empty()
	powerup_group.empty()

	p.reset(p.x, p.y)

# VARIABLES *******************************************************************

level = 1
plane_destroy_count = 0
plane_frequency = 5000
start_time = pygame.time.get_ticks()

moving_left = False
moving_right = False

home_page = True
game_page = False
score_page = False

score = 0
sound_on = True

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

		if event.type == pygame.KEYDOWN and game_page:
			if event.key == pygame.K_LEFT:
				moving_left = True
			if event.key == pygame.K_RIGHT:
				moving_right = True
			if event.key == pygame.K_SPACE:
				shoot_bullet()

		if event.type == pygame.MOUSEBUTTONDOWN:
			if home_page:
				home_page = False
				game_page = True
				click_fx.play()
			elif game_page:
				x, y = event.pos
				if p.rect.collidepoint((x,y)):
					shoot_bullet()
				elif x <= WIDTH // 2:
					moving_left = True
				elif x > WIDTH // 2:
					moving_right = True

		if event.type == pygame.KEYUP:
			moving_left = False
			moving_right = False

		if event.type == pygame.MOUSEBUTTONUP:
			moving_left = False
			moving_right = False

	if home_page:
		win.fill(BLACK)
		win.blit(logo_img, (30, 80))
		win.blit(fighter_img, (WIDTH//2 - 50, HEIGHT//2))
		pygame.draw.circle(win, WHITE, (WIDTH//2, HEIGHT//2 + 50), 50, 4)
		tap_to_play_msg.update()

	if score_page:
		win.fill(BLACK)
		win.blit(logo_img, (30, 50))
		game_over_msg.update()
		final_score_msg.update(score)

		if home_btn.draw(win):
			home_page = True
			game_page = False
			score_page = False
			reset()
			click_fx.play()

			plane_destroy_count = 0
			level = 1
			score = 0

		if replay_btn.draw(win):
			score_page = False
			game_page = True
			reset()
			click_fx.play()

			plane_destroy_count = 0
			score = 0

		if sound_btn.draw(win):
			sound_on = not sound_on

			if sound_on:
				sound_btn.update_image(sound_on_img)
				pygame.mixer.music.play(loops=-1)
			else:
				sound_btn.update_image(sound_off_img)
				pygame.mixer.music.stop()

	if game_page:

		current_time = pygame.time.get_ticks()
		delta_time = current_time - start_time
		if delta_time >= plane_frequency:
			if level == 1:
				type = 1
			elif level == 2:
				type = 2
			elif level == 3:
				type = 3
			elif level == 4:
				type = random.randint(4, 5)
			elif level == 5:
				type = random.randint(1, 5)

			x = random.randint(10, WIDTH - 100)
			e = Enemy(x, -150, type)
			enemy_group.add(e)
			start_time = current_time

		if plane_destroy_count:
			if plane_destroy_count % 5 == 0 and level < 5:
				level += 1
				plane_destroy_count = 0

		p.fuel -= 0.05
		bg.update(1)
		win.blit(clouds_img, (0, 70))

		p.update(moving_left, moving_right, explosion_group)
		p.draw(win)

		player_bullet_group.update()
		player_bullet_group.draw(win)
		enemy_bullet_group.update()
		enemy_bullet_group.draw(win)
		explosion_group.update()
		explosion_group.draw(win)
		fuel_group.update()
		fuel_group.draw(win)
		powerup_group.update()
		powerup_group.draw(win)

		enemy_group.update(enemy_bullet_group, explosion_group)
		enemy_group.draw(win)

		if p.alive:
			player_hit = pygame.sprite.spritecollide(p, enemy_bullet_group, False)
			for bullet in player_hit:
				p.health -= bullet.damage
				
				x, y = bullet.rect.center
				explosion = Explosion(x, y, 1)
				explosion_group.add(explosion)

				bullet.kill()
				collision_fx.play()

			for bullet in player_bullet_group:
				planes_hit = pygame.sprite.spritecollide(bullet, enemy_group, False)
				for plane in planes_hit:
					plane.health -= bullet.damage
					if plane.health <= 0:
						x, y = plane.rect.center
						rand = random.random()
						if rand >= 0.9:
							power = Powerup(x, y)
							powerup_group.add(power)
						elif rand >= 0.3:
							fuel = Fuel(x, y)
							fuel_group.add(fuel)

						plane_destroy_count += 1
						blast_fx.play()

					x, y = bullet.rect.center
					explosion = Explosion(x, y, 1)
					explosion_group.add(explosion)

					bullet.kill()
					collision_fx.play()

			player_collide = pygame.sprite.spritecollide(p, enemy_group, True)
			if player_collide:
				x, y = p.rect.center
				explosion = Explosion(x, y, 2)
				explosion_group.add(explosion)

				x, y = player_collide[0].rect.center
				explosion = Explosion(x, y, 2)
				explosion_group.add(explosion)
				
				p.health = 0
				p.alive = False

			if pygame.sprite.spritecollide(p, fuel_group, True):
				p.fuel += 25
				if p.fuel >= 100:
					p.fuel = 100
				fuel_fx.play()

			if pygame.sprite.spritecollide(p, powerup_group, True):
				p.powerup += 2
				fuel_fx.play()

		if not p.alive or p.fuel <= -10:
			if len(explosion_group) == 0:
				game_page = False
				score_page = True
				reset()

		score += 1
		score_msg.update(score)

		fuel_color = RED if p.fuel <= 40 else GREEN
		pygame.draw.rect(win, fuel_color, (30, 20, p.fuel, 10), border_radius=4)
		pygame.draw.rect(win, WHITE, (30, 20, 100, 10), 2, border_radius=4)
		pygame.draw.rect(win, BLUE, (30, 32, p.health, 10), border_radius=4)
		pygame.draw.rect(win, WHITE, (30, 32, 100, 10), 2, border_radius=4)
		win.blit(plane_img, (10, 15))

	pygame.draw.rect(win, WHITE, (0,0, WIDTH, HEIGHT), 5, border_radius=4)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()