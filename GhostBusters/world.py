import pickle
import pygame

from enemies import Ghost

NUM_TILES = 60
TILE_SIZE = 16

img_list = []
for index in range(1, NUM_TILES+1):
	img = pygame.image.load(f'Tiles/{index}.png')
	img_list.append(img)

class World:
	def __init__(self, objects_group):
		self.objects_group = objects_group

		self.ground_list = []
		self.rock_list = []
		self.decor_list = []

	def generate_world(self, data, win):
		for y, row in enumerate(data):
			for x, tile in enumerate(row):
				if tile >= 0:
					img = img_list[tile-1]
					rect = img.get_rect()
					rect.x = x * TILE_SIZE
					rect.y = y * TILE_SIZE
					tile_data = (img, rect)

					if tile in (0, 1, 2, 3, 4, 5, 6, 11):
						self.ground_list.append(tile_data)

					if tile in (7, 14, 18, 19, 20, 21, 25, 26, 27, 28, 32, 33, 34, 35, 42, 43, 44, 45):
						self.rock_list.append(tile_data)

					if tile in (8, 9, 10, 13, 15, 16, 17, 23, 24, 30, 31, 37, 38, 39, 40, 46, 47, 48, 49, 50, 51):
						self.decor_list.append(tile_data)

					if tile == 12:
						exit = Exit(x*TILE_SIZE, y*TILE_SIZE, tile_data)
						self.objects_group[4].add(exit)

					if tile == 41:
						water = Water(x*TILE_SIZE, y*TILE_SIZE, tile_data)
						self.objects_group[0].add(water)

					if tile in (52, 53, 56, 57):
						diamond = Diamond(x*TILE_SIZE, y*TILE_SIZE, tile_data)
						self.objects_group[1].add(diamond)

					if tile in (54, 55, 58, 59):
						potion = Potion(x*TILE_SIZE, y*TILE_SIZE, tile_data)
						self.objects_group[2].add(potion)

					if tile == 60:
						enemy = Ghost(x*TILE_SIZE, y*TILE_SIZE, win)
						self.objects_group[3].add(enemy)

	def draw_world(self, win, screen_scroll):
		for tile in self.ground_list:
			tile[1][0] += screen_scroll
			win.blit(tile[0], tile[1])
		for tile in self.rock_list:
			tile[1][0] += screen_scroll
			win.blit(tile[0], tile[1])
		for tile in self.decor_list:
			tile[1][0] += screen_scroll
			win.blit(tile[0], tile[1])


class Ladder(pygame.sprite.Sprite):
	def __init__(self, x, y, tile_data):
		super(Ladder, self).__init__()

		self.image = tile_data[0]
		self.rect = tile_data[1]
		self.rect.x = x
		self.rect.y = y

	def update(self, screen_scroll):
		self.rect.x += screen_scroll

	def draw(self, win):
		win.blit(self.image, self.rect)

class Water(pygame.sprite.Sprite):
	def __init__(self, x, y, tile_data):
		super(Water, self).__init__()

		self.image = tile_data[0]
		self.rect = tile_data[1]
		self.rect.x = x
		self.rect.y = y

	def update(self, screen_scroll):
		self.rect.x += screen_scroll

	def draw(self, win):
		win.blit(self.image, self.rect)

class Diamond(pygame.sprite.Sprite):
	def __init__(self, x, y, tile_data):
		super(Diamond, self).__init__()

		self.image = tile_data[0]
		self.rect = tile_data[1]
		self.rect.x = x
		self.rect.y = y

	def update(self, screen_scroll):
		self.rect.x += screen_scroll

	def draw(self, win):
		win.blit(self.image, self.rect)

class Potion(pygame.sprite.Sprite):
	def __init__(self, x, y, tile_data):
		super(Potion, self).__init__()

		self.image = tile_data[0]
		self.rect = tile_data[1]
		self.rect.x = x
		self.rect.y = y

	def update(self, screen_scroll):
		self.rect.x += screen_scroll

	def draw(self, win):
		win.blit(self.image, self.rect)

class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y, tile_data):
		super(Exit, self).__init__()

		self.image = pygame.transform.scale(tile_data[0], (24,24)) 
		self.rect = tile_data[1]
		self.rect.x = x
		self.rect.y = y - 8

	def update(self, screen_scroll):
		self.rect.x += screen_scroll

	def draw(self, win):
		win.blit(self.image, self.rect)

def load_level(level):
	file = f'Levels/level{level}_data'
	with open(file, 'rb') as f:
		data = pickle.load(f)
		for y in range(len(data)):
			for x in range(len(data[0])):
				if data[y][x] >= 0:
					data[y][x] += 1
	return data, len(data[0])