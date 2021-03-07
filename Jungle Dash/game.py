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

level = 3
level_dict = {
	(i+1):f'levels/level{i+1}_data' for i in range(3)
}

d = level_dict[level]
f = open(d, 'rb')
data = pickle.load(f)
f.close()

bg = pygame.image.load('assets/BG1.png')
sun = pygame.image.load('assets/sun.png')

water_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
forest_group = pygame.sprite.Group()
diamond_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
groups = [water_group, lava_group, forest_group, diamond_group, enemies_group]
world = World(win, data, groups)
player = Player(win, (10, 340), world, groups)

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
	enemies_group.update(player)
	game_over = player.update(pressed_keys, game_over)


	pygame.display.flip()
	clock.tick(FPS)

pygame.quit()