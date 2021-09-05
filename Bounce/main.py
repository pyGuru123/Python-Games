import os
import pygame

from player import Ball
from world import World, load_level

pygame.init()
WIDTH, HEIGHT = 192, 192
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption('Bounce')

clock = pygame.time.Clock()
FPS = 30

# GAME VARIABLES **************************************************************
ROWS = 12
MAX_COLS = 150
TILE_SIZE = 16

# COLORS **********************************************************************

BLUE = (175, 207, 240)

# GROUPS **********************************************************************

spikes_group = pygame.sprite.Group()
inflator_group = pygame.sprite.Group()
deflator_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

objects_groups = [spikes_group, inflator_group, deflator_group, enemy_group]
collision_groups = [inflator_group, deflator_group]

# RESET ***********************************************************************

level = 1

def reset_level(level):
	spikes_group.empty()
	inflator_group.empty()
	deflator_group.empty()
	enemy_group.empty()

	# LOAD LEVEL WORLD

	world_data, level_length = load_level(level)
	w = World(objects_groups)
	w.generate_world(world_data, win)

	return world_data, level_length, w

def reset_player():
	p = Ball(WIDTH//2, 50)
	moving_left = False
	moving_right = False

	return p, moving_left, moving_right

world_data, level_length, w = reset_level(level)
p, moving_left, moving_right = reset_player()

# VARIABLES *******************************************************************

moving_left = False
moving_right = False
screen_scroll = 0
level_scroll = 0
SCROLL_THRES = 80

running = True
while running:
	win.fill(BLUE)


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

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				moving_left = False
			if event.key == pygame.K_RIGHT:
				moving_right = False

	w.draw_world(win, screen_scroll)

	spikes_group.update(screen_scroll)
	spikes_group.draw(win)
	inflator_group.update(screen_scroll)
	inflator_group.draw(win)
	deflator_group.update(screen_scroll)
	deflator_group.draw(win)
	enemy_group.update(screen_scroll)
	enemy_group.draw(win)

	screen_scroll = 0
	p.update(moving_left, moving_right, w, collision_groups)
	p.draw(win)

	if ((p.rect.right >= WIDTH - SCROLL_THRES) and level_scroll < (level_length * 16) - WIDTH) \
			or ((p.rect.left <= SCROLL_THRES) and level_scroll > 0):
			dx = p.dx
			p.rect.x -= dx
			screen_scroll = -dx
			level_scroll += dx

	if pygame.sprite.spritecollide(p, spikes_group, False):
		world_data, level_length, w = reset_level(level)
		p, moving_left, moving_right = reset_player()
		screen_scroll = 0
		level_scroll = 0

	if pygame.sprite.spritecollide(p, enemy_group, False):
		world_data, level_length, w = reset_level(level)
		p, moving_left, moving_right = reset_player()
		screen_scroll = 0
		level_scroll = 0


	pygame.draw.rect(win, (255, 255,255), (0, 0, WIDTH, HEIGHT), 2, border_radius=5)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()