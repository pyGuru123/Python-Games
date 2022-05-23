 # HyperTiles Dash

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 29 July, 2021

import random
import pygame

from objects import *

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

# COLORS **********************************************************************


color_list = [RED, GREEN, BLUE, ORANGE, YELLOW, PURPLE]
color_index = 0
color = color_list[color_index]

death_color_list = [BLUE, ORANGE, YELLOW, PURPLE, RED, GREEN]
death_color_index = 0
death_color = death_color_list[color_index]

# FONTS ***********************************************************************

# OBJECTS *********************************************************************

tile_group = pygame.sprite.Group()

for i in range(8):
	tile = Tile(i, 1, win)
	tile_group.add(tile)
	tile = Tile(i, 2, win)
	tile_group.add(tile)

particle_group = pygame.sprite.Group()
skull_group = pygame.sprite.Group()
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
sound_on = True

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

		if event.type == pygame.MOUSEBUTTONDOWN and home_page:
			home_page = False
			game_page = True
			score_page = False

			player_alive = True
			p.reset()
			p.reset_path_variables()

			for tile in tile_group:
				tile.color = WHITE

		if event.type == pygame.MOUSEBUTTONDOWN  and game_page:
			if not clicked:
				if p.can_move:
					dash_fx.play()

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
		tile_group.update()
		HyperTile.update()
		dash.update()
		tap_to_play.update()

	if score_page:
		tile_group.update()
		final_score.update(score, color)
		best_msg.update()
		high_score_msg.update(highscore)

		if home_btn.draw(win):
			home_page = True
			score_page = False
			game_page = False
			score = 0
			score_msg = Message(WIDTH//2, HEIGHT//2, 50, f'{score}', score_font, (100, 100, 100), win)
			
		if replay_btn.draw(win):
			home_page = False
			score_page = False
			game_page = True
			score = 0
			score_msg = Message(WIDTH//2, HEIGHT//2, 50, f'{score}', score_font, (100, 100, 100), win)

			player_alive = True
			p.reset()
			p.reset_path_variables()

			for tile in tile_group:
				tile.color = WHITE

		if sound_btn.draw(win):
			sound_on = not sound_on
			
			if sound_on:
				sound_btn.update_image(sound_on_img)
				pygame.mixer.music.play(loops=-1)
			else:
				sound_btn.update_image(sound_off_img)
				pygame.mixer.music.stop()

	if game_page:

		if p.first_tile and auto_generate_deadly_tile:
			target_tile = generate_target_tile(color)
			generate_deadly_tile(death_color)
			auto_generate_deadly_tile = False

		if score and score % 3 == 0 and len(skull_group) == 0 and player_alive:
			type_ = random.randint(1, 2)
			print(type_)
			y = random.randint(200, HEIGHT - 190)
			if type_ == 1:
				x = 0			
			elif type_ == 2:
				x = WIDTH + 5
			skull = SkullCircle(x, y, type_, death_color, win)
			skull_group.add(skull)

		score_msg.update(score)
		particle_group.update()
		skull_group.update()
		p.update(color, player_alive)
		tile_group.update()

		if pygame.sprite.spritecollide(p, skull_group, False) and player_alive:
			deadly_tile_fx.play()
			x, y = p.x, p.y
			for i in range(20):
				particle = Particle(x, y, color, win)
				particle_group.add(particle)
			player_alive = False
			skull_group.empty()

		if player_alive:
			for tile in tile_group:
				collision = tile.check_collision(p)
				if collision and target_tile:
					if tile.is_deadly_tile:
						deadly_tile_fx.play()
						for i in range(30):
							particle = Particle(x, y, color, win)
							particle_group.add(particle)
						player_alive = False
					if tile.is_target_tile:
						for i in range(10):
							particle = Particle(x, y, color, win)
							particle_group.add(particle)
						target_tile_fx.play()
						score += 1
						if highscore <= score:
							highscore = score

						if len(deadly_tiles_list) > 0:
							tile = deadly_tiles_list.pop()
							tile.color = WHITE
							tile.is_deadly_tile = False
						else:
							for tile in tile_group:
								tile.is_deadly_tile = False

						target_tile = generate_target_tile(color)
					else:
						for i in range(10):
							particle = Particle(x, y, color, win)
							particle_group.add(particle)
						empty_tile_fx.play()
						target_tile = generate_target_tile(color)
						generate_deadly_tile(death_color)

		if not player_alive and len(particle_group) == 0:
			game_page = False
			score_page = True
			score_page_fx.play()

			deadly_tiles_list.clear()

			for tile in tile_group:
				tile.color = random.choice(color_list)
				tile.is_target_tile = False
				tile.is_deadly_tile = False

			final_score = Message(WIDTH//3, HEIGHT//2 - 20, 90, f'{score}', score_font, WHITE, win)


	pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 5, border_radius=10)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()
