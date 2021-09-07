import os
import pygame

from player import Ball
from world import World, load_level
from texts import Message

pygame.init()
WIDTH, HEIGHT = 192, 212
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
BLUE2 = (0, 0, 255)
WHITE = (255, 255, 255)

# FONTS ***********************************************************************

health_font = "Fonts/ARCADECLASSIC.TTF"


health_text = Message(40, WIDTH + 10, 19, "x3", health_font, WHITE, win)

# LOADING IMAGES **************************************************************

ball_image = pygame.image.load('Assets/ball.png')


# GROUPS **********************************************************************

spikes_group = pygame.sprite.Group()
inflator_group = pygame.sprite.Group()
deflator_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
checkpoint_group = pygame.sprite.Group()
health_group = pygame.sprite.Group()

objects_groups = [spikes_group, inflator_group, deflator_group, enemy_group, exit_group, 
					checkpoint_group, health_group]
collision_groups = [inflator_group, deflator_group]

# RESET ***********************************************************************

level = 1

def reset_level_data(level):
	for group in objects_groups:
		group.empty()

	# LOAD LEVEL WORLD

	world_data, level_length = load_level(level)
	w = World(objects_groups)
	w.generate_world(world_data, win)

	return world_data, level_length, w

def reset_player_data(level):
	if level == 1:
		x = WIDTH // 2
		y = 50
	if level == 2:
		x = 64
		y = 50

	p = Ball(x, y)
	moving_left = False
	moving_right = False

	return p, moving_left, moving_right

world_data, level_length, w = reset_level_data(level)
p, moving_left, moving_right = reset_player_data(level)

# VARIABLES *******************************************************************

moving_left = False
moving_right = False
SCROLL_THRES = 80
screen_scroll = 0
level_scroll = 0
reset_level = False
MAX_LEVEL = 2
checkpoint = None
health = 3

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

	w.update(screen_scroll)
	w.draw(win)

	spikes_group.update(screen_scroll)
	spikes_group.draw(win)
	health_group.update(screen_scroll)
	health_group.draw(win)
	inflator_group.update(screen_scroll)
	inflator_group.draw(win)
	deflator_group.update(screen_scroll)
	deflator_group.draw(win)
	exit_group.update(screen_scroll)
	exit_group.draw(win)
	checkpoint_group.update(screen_scroll)
	checkpoint_group.draw(win)
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

	if len(exit_group) > 0:
		exit = exit_group.sprites()[0]
		if not exit.open:
			if abs(p.rect.x - exit.rect.x) <= 80:
				exit.open = True

		if p.rect.colliderect(exit.rect) and exit.index == 11:
			checkpoint = None
			if level < MAX_LEVEL:
				level += 1
				reset_level = True

	cp = pygame.sprite.spritecollide(p, checkpoint_group, False)
	if cp:
		checkpoint = cp[0]
		if not checkpoint.catched:
			checkpoint.catched = True
			checkpoint_pos = p.rect.center
			checkpoint_screen_scroll = screen_scroll
			checkpoint_level_scroll = level_scroll

	if pygame.sprite.spritecollide(p, spikes_group, False):
		reset_level = True

	if pygame.sprite.spritecollide(p, health_group, True):
		health += 1

	if pygame.sprite.spritecollide(p, enemy_group, False):
		reset_level = True

	if reset_level:
		if health > 0:
			if checkpoint:
				checkpoint_dx = level_scroll - checkpoint_level_scroll
				w.update(checkpoint_dx)
				for group in objects_groups:
					group.update(checkpoint_dx)
				p.rect.center = checkpoint_pos
				level_scroll = checkpoint_level_scroll
			else:
				world_data, level_length, w = reset_level_data(level)
				p, moving_left, moving_right = reset_player_data(level)
				level_scroll = 0

			screen_scroll = 0
			reset_level = False
			health -= 1
		else:
			running = False

	# Drawing info bar
	pygame.draw.rect(win, (25, 25, 25), (0, HEIGHT-20, WIDTH, 20))
	pygame.draw.rect(win, (255, 255,255), (0, 0, WIDTH, HEIGHT), 1, border_radius=5)
	pygame.draw.rect(win, (255, 255,255), (0, 0, WIDTH, WIDTH), 2, border_radius=5)

	win.blit(ball_image, (5, WIDTH + 2))
	health_text.update(f'x{health}', shadow=False)

	clock.tick(FPS)
	pygame.display.update()

pygame.quit()