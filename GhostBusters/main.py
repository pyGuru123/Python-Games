import pygame

from world import World, load_level
from player import Player
from enemies import Ghost
from particles import Trail
from projectiles import Bullet, Grenade

pygame.init()

WIDTH, HEIGHT = 640, 384
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('GhostBusters')
TILE_SIZE = 16

clock = pygame.time.Clock()
FPS = 30

# IMAGES **********************************************************************

BG1 = pygame.transform.scale(pygame.image.load('assets/BG1.png'), (WIDTH, HEIGHT))
BG2 = pygame.transform.scale(pygame.image.load('assets/BG2.png'), (WIDTH, HEIGHT))
BG3 = pygame.transform.scale(pygame.image.load('assets/BG3.png'), (WIDTH, HEIGHT))

# GROUPS **********************************************************************

trail_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
diamond_group = pygame.sprite.Group()
potion_group = pygame.sprite.Group()


objects_group = [water_group, diamond_group, potion_group, enemy_group]

# OBJECTS *********************************************************************

p = Player(250, 50)
moving_left = False
moving_right = False

# LEVEL VARIABLES **************************************************************

ROWS = 24
COLS = 40
SCROLL_THRES = 200

level = 1
level_length = 0
screen_scroll = 0

# WORLD ***********************************************************************

world_data, level_length = load_level(level)
w = World(objects_group)
w.generate_world(world_data, win)

# MAIN GAME *******************************************************************

running = True
while running:
	win.blit(BG1, (0,0))
	win.blit(BG2, (0,-50))
	win.blit(BG3, (0,0))
	w.draw_world(win, screen_scroll)

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
			
	# Updating Objects ********************************************************

	bullet_group.update(screen_scroll, w)
	grenade_group.update(screen_scroll, p, enemy_group, explosion_group, w)
	explosion_group.update(screen_scroll)
	trail_group.update()
	water_group.update(screen_scroll)
	water_group.draw(win)
	diamond_group.update(screen_scroll)
	diamond_group.draw(win)
	potion_group.update(screen_scroll)
	potion_group.draw(win)

	enemy_group.update(screen_scroll, bullet_group, p)
	enemy_group.draw(win)

	if p.jump:
		t = Trail(p, (220, 220, 220), win)
		trail_group.add(t)

	screen_scroll = 0
	p.update(moving_left, moving_right, w)
	p.draw(win)

	if (p.rect.right >= WIDTH - SCROLL_THRES) or p.rect.left <= SCROLL_THRES:
		dx = p.dx
		p.rect.x -= dx
		screen_scroll = -dx


	# Collision Detetction ****************************************************

	if pygame.sprite.spritecollide(p, diamond_group, True):
		pass

	potion = pygame.sprite.spritecollide(p, potion_group, False)
	if potion:
		if p.health < 100:
			potion[0].kill()
			p.health += 15
			if p.health > 100:
				p.health = 100


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