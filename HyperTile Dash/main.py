# Hyper Dash

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 29 July, 2021

import random
import pygame

from objects import Tile, Player, Particle

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2
# | pygame.SCALED | pygame.FULLSCREEN
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
pygame.display.set_caption('Arc Dash')

clock = pygame.time.Clock()
FPS = 60

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
GRAY = (32, 32, 32)

color_list = [RED, GREEN, BLUE, ORANGE, YELLOW, PURPLE]
color_index = 0
color = color_list[color_index]

death_color_list = [BLUE, ORANGE, YELLOW, PURPLE, RED, GREEN]
death_color_index = 0
death_color = death_color_list[color_index]

# FONTS ***********************************************************************

title_font = "Fonts/Aladin-Regular.ttf"
tap_to_play_font = "Fonts/BubblegumSans-Regular.ttf"
score_font = "Fonts/DalelandsUncialBold-82zA.ttf"
game_over_font = "Fonts/ghostclan.ttf"

# SOUNDS **********************************************************************

score_fx = pygame.mixer.Sound('Sounds/point.mp3')
death_fx = pygame.mixer.Sound('Sounds/dead.mp3')
score_page_fx = pygame.mixer.Sound('Sounds/score_page.mp3')

pygame.mixer.music.load('Sounds/hk.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.5)

# OBJECTS *********************************************************************

tile_group = pygame.sprite.Group()

for i in range(8):
	tile = Tile(i, 1, win)
	tile_group.add(tile)
	tile = Tile(i, 2, win)
	tile_group.add(tile)

particle_group = pygame.sprite.Group()
p = Player(win, tile_group)

# FUNCTIONS *******************************************************************

deadly_tiles_list = []

def get_index():
	if p.tile_type == 1:
		indices = [2*index+1 for index in range(8)]
	elif p.tile_type == 2:
		indices = [2*index for index in range(8)]

	index = random.choice(indices)
	return index

def generate_target_tile(color):
	for tile in tile_group:
		if not tile.is_deadly_tile:
			tile.color = WHITE
			tile.is_target_tile = False

	index = get_index()
	tile = tile_group.sprites()[index]
	if tile.is_deadly_tile:
		generate_target_tile(color)
	else:
		tile.color = color
		tile.is_target_tile = True

	return tile


def generate_deadly_tile(color):
	for tile in tile_group:
		if tile.is_deadly_tile:
			tile.color = color

	index = get_index()
	tile = tile_group.sprites()[index]
	if tile.is_target_tile:
		generate_deadly_tile(color)
	else:
		if tile.is_deadly_tile:
			generate_deadly_tile(color)
		else:
			tile.color = color
			tile.is_deadly_tile = True
			deadly_tiles_list.append(tile)

clicked = False
num_clicks = 0
index = None
target_tile = None
auto_generate_deadly_tile = True

player_alive = True
score = 0
highscore = 0

home_page = False
game_page = True
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

		if event.type == pygame.MOUSEBUTTONDOWN:
			if not clicked:
				if p.can_move:
					index = p.path_index
					tile = p.path_target_tile
					x = p.path_x
					y = p.path_y
					p.set_move(x, y, index)

				num_clicks += 1
				if num_clicks % 5 == 0:
					color_index += 1
					if color_index > len(color_list) - 1:
						color_index = 0
					color = color_list[color_index]

					death_color_index += 1
					if death_color_index > len(death_color_list) - 1:
						death_color_index = 0
					death_color = death_color_list[death_color_index]
					for tile in deadly_tiles_list:
						tile.color = death_color

		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = False

	if home_page:
		pass

	if score_page:
		tile_group.update()

	if game_page:

		if p.first_tile and auto_generate_deadly_tile:
			target_tile = generate_target_tile(color)
			generate_deadly_tile(death_color)
			auto_generate_deadly_tile = False

		p.update(color, player_alive)
		particle_group.update()
		tile_group.update()
		if player_alive:
			for tile in tile_group:
				collision = tile.check_collision(p)
				if collision and target_tile:
					if tile.is_deadly_tile:
						death_fx.play()
						for i in range(30):
							particle = Particle(x, y, WHITE, win)
							particle_group.add(particle)
						player_alive = False
					if tile.is_target_tile:
						score_fx.play()
						if len(deadly_tiles_list) > 0:
							tile = deadly_tiles_list.pop()
							tile.color = WHITE
							tile.is_deadly_tile = False
						else:
							for tile in tile_group:
								tile.is_deadly_tile = False

						target_tile = generate_target_tile(color)
					else:
						target_tile = generate_target_tile(color)
						generate_deadly_tile(death_color)

		if not player_alive and len(particle_group) == 0:
			game_page = False
			score_page = True
			score_page_fx.play()

			for tile in tile_group:
				tile.color = WHITE
				tile.is_target_tile = False
				tile.is_deadly_tile = False


	pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 5, border_radius=10)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()