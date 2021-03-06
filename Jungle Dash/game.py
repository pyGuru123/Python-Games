import pickle
import pygame
from pygame.locals import *

from objects import World, Player, draw_lines

SIZE = WIDTH , HEIGHT= 1000, 650
tile_size = 50

pygame.init()
win = pygame.display.set_mode(SIZE)
pygame.display.set_caption('DASH')
clock = pygame.time.Clock()
FPS = 30
 
bg = pygame.image.load('assets/BG.png')
sun = pygame.image.load('assets/sun.png')

f = open('levels/level1_data', 'rb')
data = pickle.load(f)
f.close()

water_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
forest_groups = pygame.sprite.Group()
diamond_groups = pygame.sprite.Group()
groups = [water_group, lava_group, forest_groups, diamond_groups]
world = World(win, data, groups)
player = Player(win, (100, 440), world, groups)

game_over = False
running = True
while running:
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False

	pressed_keys = pygame.key.get_pressed()

	# displaying background & sun image
	win.blit(bg, (0,0))
	win.blit(sun, (40,40))

	# drawing grid
	# draw_lines(win)

	world.draw()
	for group in groups:
		group.draw(win)
	game_over = player.update(pressed_keys, game_over)


	pygame.display.flip()
	clock.tick(FPS)

pygame.quit()