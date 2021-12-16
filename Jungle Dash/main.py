import os
import random
import pygame
from pygame.locals import *

from objects import World, Player, Button, draw_lines, load_level, draw_text, sounds

# Window setup
SIZE = WIDTH , HEIGHT= 1000, 650
tile_size = 50

pygame.init()
win = pygame.display.set_mode(SIZE)
pygame.display.set_caption('DASH')
clock = pygame.time.Clock()
FPS = 30


# background images
bg1 = pygame.image.load('assets/BG1.png')
bg2 = pygame.image.load('assets/BG2.png')
bg = bg1
sun = pygame.image.load('assets/sun.png')
jungle_dash = pygame.image.load('assets/jungle dash.png')
you_won = pygame.image.load('assets/won.png')


# loading level 1
level = 1
max_level = len(os.listdir('levels/'))
data = load_level(level)

player_pos = (10, 340)


# creating world & objects
water_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
forest_group = pygame.sprite.Group()
diamond_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
bridge_group = pygame.sprite.Group()
groups = [water_group, lava_group, forest_group, diamond_group, enemies_group, exit_group, platform_group,
			bridge_group]
world = World(win, data, groups)
player = Player(win, player_pos, world, groups)

# creating buttons
play= pygame.image.load('assets/play.png')
replay = pygame.image.load('assets/replay.png')
home = pygame.image.load('assets/home.png')
exit = pygame.image.load('assets/exit.png')
setting = pygame.image.load('assets/setting.png')

play_btn = Button(play, (128, 64), WIDTH//2 - WIDTH // 16, HEIGHT//2)
replay_btn  = Button(replay, (45,42), WIDTH//2 - 110, HEIGHT//2 + 20)
home_btn  = Button(home, (45,42), WIDTH//2 - 20, HEIGHT//2 + 20)
exit_btn  = Button(exit, (45,42), WIDTH//2 + 70, HEIGHT//2 + 20)


# function to reset a level
def reset_level(level):
	global cur_score
	cur_score = 0

	data = load_level(level)
	if data:
		for group in groups:
			group.empty()
		world = World(win, data, groups)
		player.reset(win, player_pos, world, groups)
# 10, 340
	return world

score = 0
cur_score = 0

main_menu = True
game_over = False
level_won = False
game_won = False
running = True
while running:
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False

	pressed_keys = pygame.key.get_pressed()

	# displaying background & sun image
	win.blit(bg, (0,0))
	win.blit(sun, (40,40))
	world.draw()
	for group in groups:
		group.draw(win)

	# drawing grid
	# draw_lines(win)

	if main_menu:
		win.blit(jungle_dash, (WIDTH//2 - WIDTH//8, HEIGHT//4))

		play_game = play_btn.draw(win)
		if play_game:
			main_menu = False
			game_over = False
			game_won = False
			score = 0

	else:
		
		if not game_over and not game_won:
			
			enemies_group.update(player)
			platform_group.update()
			exit_group.update(player)
			if pygame.sprite.spritecollide(player, diamond_group, True):
				sounds[0].play()
				cur_score += 1
				score += 1	
			draw_text(win, f'{score}', ((WIDTH//tile_size - 2) * tile_size, tile_size//2 + 10))
			
		game_over, level_won = player.update(pressed_keys, game_over, level_won, game_won)

		if game_over and not game_won:
			replay = replay_btn.draw(win)
			home = home_btn.draw(win)
			exit = exit_btn.draw(win)

			if replay:
				score -= cur_score
				world = reset_level(level)
				game_over = False
			if home:
				game_over = True
				main_menu = True
				bg = bg1
				level = 1
				world = reset_level(level)
			if exit:
				running = False

		if level_won:
			if level <= max_level:
				level += 1
				game_level = f'levels/level{level}_data'
				if os.path.exists(game_level):
					data = []
					world = reset_level(level)
					level_won = False
					score += cur_score

				bg = random.choice([bg1, bg2])
			else:
				game_won = True
				bg = bg1
				win.blit(you_won, (WIDTH//4, HEIGHT // 4))
				home = home_btn.draw(win)

				if home:
					game_over = True
					main_menu = True
					level_won = False
					level = 1
					world = reset_level(level)

	pygame.display.flip()
	clock.tick(FPS)

pygame.quit()