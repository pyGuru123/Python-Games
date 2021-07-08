import os
import pickle
import random
import pygame
from pygame import mixer
from pygame.locals import *

SIZE = WIDTH , HEIGHT= 288, 512
TILE_SIZE = 16
ROWS, COLS = HEIGHT // 16, WIDTH // 16

pygame.font.init()
score_font = pygame.font.SysFont('Bauhaus 93', 30)

# Colors

WHITE = (255,255,255)
BLUE = (30, 144, 255)

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
					if col in range(1,7) or col in range(9,15) or col in range(17,23) or col in range(25,46) or col in range(47,69):
						# dirt blocks
						img = pygame.transform.rotate(tiles[col-1], -90)
						rect = img.get_rect()
						rect.x = col_count * TILE_SIZE
						rect.y = row_count * TILE_SIZE
						tile = (img, rect)
						self.tile_list.append(tile)

					if col in (81, 82, 83, 84):
						# diamond
						img = pygame.transform.rotate(tiles[col-1], -90)
						diamond = Diamond(img, col_count * TILE_SIZE, row_count * TILE_SIZE)
						self.groups[0].add(diamond)

					if col in (72, 80, 87, 88):
						# spikes
						img = pygame.transform.rotate(tiles[col-1], -90)
						spike = Spike(img, col_count * TILE_SIZE, row_count * TILE_SIZE)
						self.groups[1].add(spike)
						
					if col in (70, 71, 78, 79):
						# plant
						img = pygame.transform.rotate(tiles[col-1], -90)
						plant = Plant(img, col_count * TILE_SIZE, row_count * TILE_SIZE)
						self.groups[2].add(plant)
					
					if col == 76:
						# board
						img = pygame.transform.rotate(tiles[col-1], -90)
						board = Board(img, col_count * TILE_SIZE, row_count * TILE_SIZE)
						self.groups[3].add(board)
					
					if col in (69, 77, 85):
						# chain
						img = pygame.transform.rotate(tiles[col-1], -90)
						chain = Chain(img, col_count * TILE_SIZE, row_count * TILE_SIZE)
						self.groups[4].add(chain)


				col_count += 1
			row_count += 1


	def draw(self):
		for tile in self.tile_list:
			self.win.blit(tile[0], tile[1])
	
					
def game_data(level):
	data = None
	if level == 1:
		data = (180, 20), (65, 290)
	if level == 2:
		data = (240, 40), (65, 450)
	if level == 3:
		data = (240, 40), (65, 20)
		
	return data
			
# Assets & Objects *******************************
			
class Assets(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		super(Assets, self).__init__()

		self.image = img
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
			
class Diamond(Assets):
	def __init__(self, img, x, y):
		super(Diamond, self).__init__(img, x, y)

class Spike(Assets):
	def __init__(self, img, x, y):
		super(Spike, self).__init__(img, x, y)
		
class Plant(Assets):
	def __init__(self, img, x, y):
		super(Plant, self).__init__(img, x, y)

class Board(Assets):
	def __init__(self, img, x, y):
		super(Board, self).__init__(img, x, y)
		
class Chain(Assets):
	def __init__(self, img, x, y):
		super(Chain, self).__init__(img, x, y)
		
class Portal():
		def __init__(self, x, y, win):
			self.win = win
			self.im_list = []
			self.index = 0
			
			for i in range(1,10):
				img = pygame.transform.rotate(pygame.image.load(f"Assets/portal/{i}.gif"), -90)
				img = pygame.transform.scale(img, (24,24))
				self.im_list.append(img)
			
			self.rect = self.im_list[self.index].get_rect()
			self.rect.x = x
			self.rect.y = y
			self.cooldown = 2
			self.counter = 0
				
		def update(self):
				self.counter += 1
				if self.counter >= self.cooldown:
					self.index += 1
					self.counter = 0
				if self.index > 8:
					self.index = 0
				
				image = self.im_list[self.index]
				self.win.blit(image, self.rect)
					
				
		
# Sound effects

pygame.mixer.init()
diamond_fx =  pygame.mixer.Sound('Sounds/coin_fx.wav')
chain_fx =  pygame.mixer.Sound('Sounds/chain_fx.mp3')
death_fx =  pygame.mixer.Sound('Sounds/death_fx.wav')
		
# Player ******************************************

class Player():
		def __init__(self, win, pos, world, groups):
			self.reset(win, pos, world, groups)
			
		def update(self, pressed_keys, game_over):
			dx = 0
			dy = 0
			walk_cooldown = 5
			
			collide = pygame.sprite.spritecollideany(self, self.groups[4], False)
			if collide:
				self.on_chain = True
				self.vel_x = 0
				self.direction = 2
				if not self.shift:
					y = collide.rect.center[1]
					x = self.rect.x
					self.rect.x = x
					self.rect.y = y - self.width // 2 + 2
			else:
				self.on_chain = False
				self.shift = False
			
			if pressed_keys[0] and self.on_chain:
				# Up
				dx = 1
				chain_fx.play()
				self.counter += 1
			if pressed_keys[1] and self.on_chain:
				# Down
				dx = -1
				chain_fx.play()
				self.counter += 1
			if pressed_keys[2] and self.on_chain:
				self.vel_x = -5
				self.vel_y = -5
				self.shift = True
				self.on_chain = False
			if pressed_keys[3] and self.on_chain:
				self.vel_x = -5
				self.vel_y = 5
				self.shift = True
				self.on_chain = False
				
			if pressed_keys[0] and not self.jumped and not self.in_air:
				# Jump
				self.vel_x = -9
				self.jumped = True
			if not pressed_keys[0]:
				self.jumped = False
			if pressed_keys[2] and not self.on_chain:
				# Left
				dy = -1
				self.counter += 1
				self.direction = -1
			if pressed_keys[3] and not self.on_chain:
				# Right
				dy = 1
				self.counter += 1
				self.direction = 1
				
			if pressed_keys[2] == False and pressed_keys[3] == False and not self.on_chain:
				self.counter = 0
				self.index = 0
				self.image = self.image_right[self.index]
				
				if self.direction == -1:
					self.image = self.image_left[self.index]
				if self.direction == 1:
					self.image = self.image_right[self.index]
			
			if self.counter > walk_cooldown:
				self.counter = 0
				self.index += 1
				
				if self.index >= len(self.image_right):
					self.index = 0
					
				if self.direction == -1:
					self.image = self.image_left[self.index]
				if self.direction == 1:
					self.image = self.image_right[self.index]
				if self.direction == 2:
					self.image = self.image_up[self.index]
					
			# Gravity
			if not self.on_chain:
				self.vel_x += 1
				if self.vel_x >= 3:
					self.vel_x = 3
				dx -= self.vel_x
				
			if self.vel_y >= 0:
				dy = 1
				self.vel_y -= 1
			
			# Platform collision
			self.in_air = True
			for tile in self.world.tile_list:
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					dy = 0
					
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					# check if below the ground
					if self.vel_x > 0:
						dx = tile[1].right - self.rect.left
						self.vel_x = 0
						self.in_air = False
					elif self.vel_x <= 0:
						dx = tile[1].left - self.rect.right
						self.vel_x = 0
			
			self.rect.x += dx
			self.rect.y += dy
			
			# Collect Diamond
			if pygame.sprite.spritecollide(self, self.groups[0], True):
				diamond_fx.play()
			# Spike Collision
			if pygame.sprite.spritecollide(self, self.groups[1], False):
				death_fx.play()
				game_over = True
			
			self.win.blit(self.image, self.rect)
			return game_over
			
		def reset(self, win, pos, world, groups):
			self.win = win
			self.pos = pos
			self.world = world
			self.groups = groups
			
			self.image_right = []
			self.image_left = []
			self.image_up = []
			self.index = 0
			self.counter = 0
			
			for imindex in range(1,37):
				img = pygame.image.load(f"Assets/sara/{imindex}.png")
				img = pygame.transform.rotate(img, -90)
				img = pygame.transform.scale(img, (22, 15))
				if imindex in range(1,10):
					self.image_up.append(img)
				if imindex in range(10, 19):
					self.image_right.append(img)
				if imindex in range(28, 37):
					self.image_left.append(img)
					
			self.image = self.image_right[self.index]
			self.rect = self.image.get_rect()
			self.rect.x = pos[0]
			self.rect.y = pos[1]
			self.width = self.image.get_width()
			self.height = self.image.get_height()
			self.direction = 1
			self.vel_x = 0
			self.vel_y = 0
			self.jumped = False
			self.shift = False
			self.in_air = True
			self.on_chain = False
			
class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()

		self.scale = scale
		self.image = pygame.transform.scale(img, self.scale)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False
		
	def update_image(self, img):
		self.image = pygame.transform.scale(img, self.scale)

	def draw(self, win):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False

		win.blit(self.image, self.rect)
		return action

# Functions **************************************

def draw_lines(win):
	for row in range(HEIGHT // tile_size + 1):
		pygame.draw.line(win, WHITE, (0, tile_size*row), (WIDTH, tile_size*row), 2)
	for col in range(WIDTH // tile_size):
		pygame.draw.line(win, WHITE, (tile_size*col, 0), (tile_size*col, HEIGHT), 2)


def load_level(level):
	game_level = f'levels/level{level}_data'
	data = None
	if os.path.exists(game_level):
		f = open(game_level, 'rb')
		data = pickle.load(f)
		f.close()

	return data