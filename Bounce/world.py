import pygame
import pickle

NUM_TILES = 26
TILE_SIZE = 16

img_list = []
for index in range(1, NUM_TILES+1):
	img = pygame.image.load(f'Tiles/{index}.png')
	img_list.append(img)

class World:
	def __init__(self, objects_group):
		self.objects_group = objects_group

		self.wall_list = []

	def generate_world(self, data, win):
		for y, row in enumerate(data):
			for x, tile in enumerate(row):
				if tile >= 0:
					img = img_list[tile-1]
					rect = img.get_rect()
					rect.x = x * TILE_SIZE
					rect.y = y * TILE_SIZE
					tile_data = (img, rect)

					if tile in (1, 2, 3, 4, 5):
						self.wall_list.append(tile_data)

	def draw_world(self, win, screen_scroll):
		for tile in self.wall_list:
			tile[1][0] += screen_scroll
			win.blit(tile[0], tile[1])



def load_level(level):
	file = f'Levels/level{level}_data'
	with open(file, 'rb') as f:
		data = pickle.load(f)
		for y in range(len(data)):
			for x in range(len(data[0])):
				if data[y][x] >= 0:
					data[y][x] += 1
	return data, len(data[0])
