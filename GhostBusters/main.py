import pygame

from player import Player
from enemies import Ghost
from particles import Trail
from projectiles import Bullet, Grenade

pygame.init()

WIDTH, HEIGHT = 640, 384
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('GhostBusters')

clock = pygame.time.Clock()
FPS = 30

# GROUPS **********************************************************************

trail_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# OBJECTS *********************************************************************

p = Player(100, 100)
moving_left = False
moving_right = False

g = Ghost(500, 184, win)
enemy_group.add(g)

# MAIN GAME *******************************************************************

running = True
while running:
	win.fill((12,12,12))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				moving_left = True
			if event.key == pygame.K_RIGHT:
				moving_right = True
			if event.key == pygame.K_UP:
				if not p.jump:
					p.jump = True
			if event.key == pygame.K_SPACE:
				x, y = p.rect.center
				direction = p.direction
				bullet = Bullet(x, y, direction, (240, 240, 240), 1, win)
				bullet_group.add(bullet)

				p.attack = True
			if event.key == pygame.K_g:
				if p.grenades:
					p.grenades -= 1
					grenade = Grenade(p.rect.centerx, p.rect.centery, p.direction, win)
					grenade_group.add(grenade)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				moving_left = False
			if event.key == pygame.K_RIGHT:
				moving_right = False
			
	if p.jump:
		t = Trail(p, (220, 220, 220), win)
		trail_group.add(t)

	bullet_group.update()
	grenade_group.update(p, enemy_group, explosion_group)
	explosion_group.update()
	trail_group.update()

	p.update(moving_left, moving_right)
	p.draw(win)

	enemy_group.update(bullet_group)
	enemy_group.draw(win)

	for bullet in bullet_group:
		enemy =  pygame.sprite.spritecollide(bullet, enemy_group, False)
		if enemy and bullet.type == 1:
			if not enemy[0].hit:
				enemy[0].hit = True
				enemy[0].health -= 50
			bullet.kill()
		if bullet.rect.colliderect(p):
			if bullet.type == 2:
				if not p.hit:
					p.hit = True
					p.health -= 20
					print(p.health)
				bullet.kill()

	clock.tick(FPS)
	pygame.display.update()

pygame.quit()