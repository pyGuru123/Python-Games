import os
import random
import pygame
from pygame.locals import *

SIZE = WIDTH , HEIGHT= 1000, 650
tile_size = 50

WHITE = (255,255,255)


# loading images
dead_img = pygame.image.load('assets/ghost.png')
game_over_img = pygame.image.load('assets/gover.png')
game_over_img = pygame.transform.scale(game_over_img, (300,250))
game_over_rect = game_over_img.get_rect(center=(WIDTH//2, HEIGHT//2 - HEIGHT//6))

# creates background
class World:
	def __init__(self, win, data, groups):
		self.tile_list  = []
		self.win = win
		self.groups = groups

		tiles = []
		for t in sorted(os.listdir('tiles/'), key=lambda s: int(s[:-4])):
			tile = pygame.image.load('tiles/' + t)
			tiles.append(tile)

		row_count = 0
		for row in data:
			col_count = 0
			for col in row:
				if col > 0:
					if col in range(1,14):
						# dirt blocks
						img = pygame.transform.scale(tiles[col-1], (tile_size, tile_size))
						rect = img.get_rect()
						rect.x = col_count * tile_size
						rect.y = row_count * tile_size
						tile = (img, rect)
						self.tile_list.append(tile)

					if col == 14:
						# bush
						bush = Forest('bush',col_count * tile_size, row_count * tile_size + tile_size // 2)
						self.groups[2].add(bush)

					if col == 15:
						# lava
						lava = Fluid('lava', col_count * tile_size, row_count * tile_size + tile_size // 2)
						self.groups[1].add(lava)
					if col == 17:
						# diamond
						diamond = Diamond(col_count * tile_size, row_count * tile_size)
						self.groups[3].add(diamond)
					if col == 19:
						# water block
						water = Fluid('water', col_count * tile_size, row_count * tile_size + tile_size // 2)
						self.groups[1].add(water)
					if col == 20:
						# tree
						tree = Forest('tree', (col_count-1) * tile_size + 10, (row_count-2) * tile_size + 5)
						self.groups[2].add(tree)


				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			self.win.blit(tile[0], tile[1])

# -------------------------------------------------------------------------------------------------
#											 Creates Player
class Player:
	def __init__(self, win, pos, world, groups):
		self.reset(win, pos, world, groups)

	def update(self, pressed_keys, game_over):
		dx = 0
		dy = 0
		walk_cooldown = 3


		if not game_over:
			if (pressed_keys[K_UP] or pressed_keys[K_SPACE]) and not self.jumped and not self.in_air:
				self.vel_y = -15
				self.jumped = True
			if (pressed_keys[K_UP] or pressed_keys[K_SPACE]) == False:
				self.jumped = False
			if pressed_keys[K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1
			if pressed_keys[K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1

			if pressed_keys[K_LEFT] == False and pressed_keys[K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				self.image = self.img_right[self.index]

				if self.direction == 1:
					self.image = self.img_right[self.index]
				elif self.direction == -1:
					self.image = self.img_left[self.index]

			if self.counter > walk_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.img_right):
					self.index = 0

				if self.direction == 1:
					self.image = self.img_right[self.index]
				elif self.direction == -1:
					self.image = self.img_left[self.index]


			# add gravity
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			# check for colision
			self.in_air = True
			for tile in self.world.tile_list:
				# check for collision in x direction
				if tile[1].colliderect(self.rect.x+dx, self.rect.y, self.width, self.height):
					dx = 0
					
				# check for collision in y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					# check if below the ground
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False

			if pygame.sprite.spritecollide(self, self.groups[0], False):
				game_over  = True
			if pygame.sprite.spritecollide(self, self.groups[1], False):
				game_over  = True

			# updating player position
			self.rect.x += dx
			self.rect.y += dy
			# if self.rect.x == self.width:
			# 	self.rect.x = self.width
			if self.rect.x >= WIDTH - self.width:
				self.rect.x = WIDTH - self.width


		elif game_over:
			self.image = dead_img
			if self.rect.top > 0:
				self.rect.y -= 5

			self.win.blit(game_over_img, game_over_rect)


		# displaying player on window
		self.win.blit(self.image, self.rect)
		# pygame.draw.rect(self.win, (255, 255, 255), self.rect, 1)
	
		return game_over

	def reset(self, win, pos, world, groups):
		x, y  = pos
		self.win = win
		self.world = world
		self.groups = groups

		self.img_right = []
		self.img_left = []
		self.index = 0
		self.counter = 0

		for i in range(6):
			img = pygame.image.load(f'player/walk{i+1}.png')
			img_right = pygame.transform.scale(img, (45,70))
			img_left = pygame.transform.flip(img_right, True, False)
			self.img_right.append(img_right)
			self.img_left.append(img_left)

		self.image = self.img_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.direction = 1
		self.vel_y = 0
		self.jumping = False
		self.in_air = True


class Fluid(pygame.sprite.Sprite):
	def __init__(self, type_, x, y):
		super(Fluid, self).__init__()

		if type_ == 'water':
			img = pygame.image.load('tiles/19.png')
		elif type_ == 'lava':
			img = pygame.image.load('tiles/15.png')

		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2 + tile_size // 4))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Forest(pygame.sprite.Sprite):
	def __init__(self, type_, x, y):
		super(Forest, self).__init__()

		if type_ == 'bush':
			img = pygame.image.load('tiles/14.png')
			self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 0.50)))

		if type_ == 'tree':
			img = pygame.image.load('tiles/20.png')
			self.image = pygame.transform.scale(img, (3*tile_size, 3 * tile_size))

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Diamond(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Diamond, self).__init__()

		img_list = [f'assets/d{i+1}.png' for i in range(4)]
		img = pygame.image.load(random.choice(img_list))
		self.image = pygame.transform.scale(img, (tile_size, tile_size))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Button(pygame.sprite.Sprite):
	pass



# -------------------------------------------------------------------------------------------------
#											 Creates Grid
def draw_lines(win):
	for row in range(HEIGHT // tile_size + 1):
		pygame.draw.line(win, WHITE, (0, tile_size*row), (WIDTH, tile_size*row), 2)
	for col in range(WIDTH // tile_size):
		pygame.draw.line(win, WHITE, (tile_size*col, 0), (tile_size*col, HEIGHT), 2)