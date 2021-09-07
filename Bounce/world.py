import pygame
import pickle

from enemies import Enemy

NUM_TILES = 28
TILE_SIZE = 16

img_list = []
for index in range(1, NUM_TILES+1):
	img = pygame.image.load(f'Tiles/{index}.png')
	img_list.append(img)

class World:
	def __init__(self, objects_group):
		self.objects_group = objects_group

		self.wall_list = []
		self.ramp_list = []
		self.water_list = []

	def generate_world(self, data, win):
		for y, row in enumerate(data):
			for x, tile in enumerate(row):
				if tile >= 0:
					img = img_list[tile-1]
					rect = img.get_rect()
					rect.x = x * TILE_SIZE
					rect.y = y * TILE_SIZE
					tile_data = (img, rect)

					if tile == 1:
						self.wall_list.append(tile_data)
					if tile in (4, 7):
						ramp = Ramp(x*TILE_SIZE, y*TILE_SIZE, 1, tile_data)
						self.ramp_list.append(ramp)
					if tile in (5, 8):
						ramp = Ramp(x*TILE_SIZE, y*TILE_SIZE, 2, tile_data)
						self.ramp_list.append(ramp)
					if tile == 6:
						self.water_list.append(tile_data)
					if tile in (11, 21):
						spike = Spikes(x*TILE_SIZE, y*TILE_SIZE, tile_data)
						self.objects_group[0].add(spike)
					if tile == 16:
						exit = Exit(x*TILE_SIZE, y*TILE_SIZE)
						self.objects_group[4].add(exit)
					if tile == 19:
						checkpoint = Checkpoint(x*TILE_SIZE, y*TILE_SIZE)
						self.objects_group[5].add(checkpoint)
					if tile == 20:
						life = Life(x*TILE_SIZE, y*TILE_SIZE, tile_data)
						self.objects_group[6].add(life)
					if tile == 23:
						inflator = Inflator(x*TILE_SIZE, y*TILE_SIZE, tile_data)
						self.objects_group[1].add(inflator)
					if tile in (12, 13, 22):
						deflator = Deflator(x*TILE_SIZE, y*TILE_SIZE, tile_data)
						self.objects_group[2].add(deflator)
					if tile == 27:
						enemy = Enemy(x*TILE_SIZE, y*TILE_SIZE, 1, self.wall_list)
						self.objects_group[3].add(enemy)
					if tile == 28:
						enemy = Enemy(x*TILE_SIZE, y*TILE_SIZE, 2, self.wall_list)
						self.objects_group[3].add(enemy)

	def update(self, screen_scroll):
		for tile in self.wall_list:
			tile[1][0] += screen_scroll
		for ramp in self.ramp_list:
			ramp.update(screen_scroll)
		for tile in self.water_list:
			tile[1][0] += screen_scroll

	def draw(self, win):
		for tile in self.wall_list:
			win.blit(tile[0], tile[1])
		for ramp in self.ramp_list:
			ramp.draw(win)
		for tile in self.water_list:
			win.blit(tile[0], tile[1])


class Asset(pygame.sprite.Sprite):
	def __init__(self, x, y, tile_data):
		super(Asset, self).__init__()

		self.image = tile_data[0]
		self.rect = tile_data[1]
		self.rect.x = x
		self.rect.y = y

	def update(self, screen_scroll):
		self.rect.x += screen_scroll

	def draw(self, win):
		win.blit(self.image, self.rect)

class Spikes(Asset):
	def __init__(self, x, y, tile_data):
		super(Spikes, self).__init__(x, y, tile_data)

class Inflator(Asset):
	def __init__(self, x, y, tile_data):
		super(Inflator, self).__init__(x, y, tile_data)

class Deflator(Asset):
	def __init__(self, x, y, tile_data):
		super(Deflator, self).__init__(x, y, tile_data)

class Life(Asset):
	def __init__(self, x, y, tile_data):
		super(Life, self).__init__(x, y, tile_data)


class Ramp(pygame.sprite.Sprite):
	def __init__(self, x, y, type_, tile_data):
		super(Ramp, self).__init__()

		self.type = type_
		self.image = tile_data[0]
		self.rect = tile_data[1]
		self.rect.x = x
		self.rect.y = y

	def update(self, screen_scroll):
		self.rect.x += screen_scroll

	def draw(self, win):
		win.blit(self.image, self.rect)

class Checkpoint(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Checkpoint, self).__init__()

		self.checkpoint_orig = pygame.image.load('Assets/checkpoint1.png')
		self.checkpoint_catched = pygame.image.load('Assets/checkpoint2.png')
		self.image = self.checkpoint_orig
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.catched = False

	def update(self, screen_scroll):
		if self.catched:
			self.image = self.checkpoint_catched

		self.rect.x += screen_scroll

	def draw(self, win):
		win.blit(self.image, self.rect)


class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Exit, self).__init__()

		self.image = pygame.image.load('Assets/Exit/tile0.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.index = 0
		self.open = False
		self.counter = 0

	def update(self, screen_scroll):
		if self.open:
			self.counter += 1
			if self.counter % 5 == 0:
				if self.index < 11:
					self.index += 1
					self.image = pygame.image.load(f'Assets/Exit/tile{self.index}.png')

		self.rect.x += screen_scroll

	def draw(self, win):
		win.blit(self.image, self.rect)


# Level Loading Function ******************************************************

def load_level(level):
	file = f'Levels/level{level}_data'
	with open(file, 'rb') as f:
		data = pickle.load(f)
		for y in range(len(data)):
			for x in range(len(data[0])):
				if data[y][x] >= 0:
					data[y][x] += 1
	return data, len(data[0])
