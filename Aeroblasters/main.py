# Aeroblasters

import random
import pygame
from objects import Background, Player, Enemy, Bullet, Explosion, Fuel, Powerup

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

# IMAGES **********************************************************************

plane_img = pygame.image.load('Assets/plane.png')
plane_img = pygame.transform.scale(plane_img, (30, 30))

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
	global powerup
	x, y = p.rect.center[0], p.rect.y

	if powerup > 0:
		for dx in range(-3, 4):
			b = Bullet(x, y, 4, dx)
			player_bullet_group.add(b)
		powerup -= 1
	else:
		b = Bullet(x-30, y, 6)
		player_bullet_group.add(b)
		b = Bullet(x+30, y, 6)
		player_bullet_group.add(b)

# VARIABLES *******************************************************************

level = 1
plane_frequency = 5000
start_time = pygame.time.get_ticks()

moving_left = False
moving_right = False

current_fuel = 100
powerup = 5
generate_fuel = False

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
				shoot_bullet()

		if event.type == pygame.MOUSEBUTTONDOWN:
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

	current_time = pygame.time.get_ticks()
	delta_time = current_time - start_time
	if delta_time >= plane_frequency:
		x = random.randint(10, WIDTH - 100)
		e = Enemy(x, -150, 5)
		enemy_group.add(e)
		start_time = current_time
		generate_fuel = True

	if delta_time >= plane_frequency // 2 and generate_fuel:
		x = random.randint(10, WIDTH - 50)
		fuel = Fuel(x, -30)
		fuel_group.add(fuel)
		generate_fuel = False

	current_fuel -= 0.05

	bg.update(1)

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

		for bullet in player_bullet_group:
			planes_hit = pygame.sprite.spritecollide(bullet, enemy_group, False)
			for plane in planes_hit:
				plane.health -= bullet.damage
				if plane.health <= 0:
					if random.random() >= 0.9:
						x, y = plane.rect.center
						power = Powerup(x, y)
						powerup_group.add(power)

				x, y = bullet.rect.center
				explosion = Explosion(x, y, 1)
				explosion_group.add(explosion)

				bullet.kill()

		player_collide = pygame.sprite.spritecollide(p, enemy_group, True)
		if player_collide:
			x, y = p.rect.center
			explosion = Explosion(x, y, 2)
			explosion_group.add(explosion)

			x, y = player_collide[0].rect.center
			explosion = Explosion(x, y, 2)
			explosion_group.add(explosion)
			
			p.alive = False

		if pygame.sprite.spritecollide(p, fuel_group, True):
			current_fuel += 10
			if current_fuel >= 100:
				current_fuel = 100

		if pygame.sprite.spritecollide(p, powerup_group, True):
			powerup += 2


	fuel_color = RED if current_fuel <= 40 else GREEN
	pygame.draw.rect(win, fuel_color, (30, 30, current_fuel, 10), border_radius=4)
	pygame.draw.rect(win, WHITE, (30, 30, 100, 10), 2, border_radius=4)
	win.blit(plane_img, (10, 20))

	pygame.draw.rect(win, WHITE, (0,0, WIDTH, HEIGHT), 5, border_radius=4)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()