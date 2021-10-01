# Aeroblasters

import random
import pygame
from objects import Background, Player, Enemy, Bullet

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

# Groups and objects

bg = Background(win)
p = Player(144, HEIGHT - 100)

enemy_group = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()

# Variables
level = 1
plane_frequency = 4500
start_time = pygame.time.get_ticks()

moving_left = False
moving_right = False

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				moving_left = True
			if event.key == pygame.K_RIGHT:
				moving_right = True
			if event.key == pygame.K_SPACE:
				x, y = p.rect.center[0], p.rect.y
				b = Bullet(x-30, y, 6)
				player_bullet_group.add(b)
				b = Bullet(x+30, y, 6)
				player_bullet_group.add(b)

		if event.type == pygame.MOUSEBUTTONDOWN:
			x = event.pos[0]
			if x <= WIDTH // 2:
				moving_left = True
			if x >= WIDTH // 2:
				moving_right = True

		if event.type == pygame.KEYUP:
			moving_left = False
			moving_right = False

		if event.type == pygame.MOUSEBUTTONUP:
			moving_left = False
			moving_right = False

	current_time = pygame.time.get_ticks()
	delta_time = current_time - start_time
	if delta_time >= plane_frequency:
		x = random.randint(10, WIDTH - 100)
		e = Enemy(x, -150, 5)
		enemy_group.add(e)
		start_time = current_time


	bg.update(1)

	p.update(moving_left, moving_right)
	p.draw(win)

	player_bullet_group.update()
	player_bullet_group.draw(win)
	enemy_bullet_group.update()
	enemy_bullet_group.draw(win)

	enemy_group.update(enemy_bullet_group)
	enemy_group.draw(win)

	player_hit = pygame.sprite.spritecollide(p, enemy_bullet_group, False)
	for bullet in player_hit:
		p.health -= bullet.damage
		print(p.health)
		bullet.kill()

	for bullet in player_bullet_group:
		planes_hit = pygame.sprite.spritecollide(bullet, enemy_group, False)
		for plane in planes_hit:
			plane.health -= bullet.damage
			bullet.kill()



	pygame.draw.rect(win, WHITE, (0,0, WIDTH, HEIGHT), 5, border_radius=4)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()