import os
import pickle
import pygame
from pygame.locals import *

SIZE = WIDTH, HEIGHT = 192, 192
ROWS = 12
MAX_COLS = 150
TILE_SIZE = 16

scroll_speed = 0.5

class World:
	def __init__(self, win, data):
		self.tile_list  = []
		self.win = win
		self.world_data = data

		self.img_list = []
		for i in range(1,27):
			img = pygame.image.load(f'tiles/{i}.png')
			img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
			self.img_list.append(img)

	def draw(self, scroll_left, scroll_right, scroll):
		if scroll_left and scroll > 0:
			scroll -= 5 * scroll_speed
		if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
			scroll += 5 * scroll_speed

		for y, row in enumerate(self.world_data):
			for x, tile in enumerate(row):
				if tile >= 0:
					self.win.blit(self.img_list[tile], (x*TILE_SIZE - scroll, y*TILE_SIZE))

		return scroll



class Ball(pygame.sprite.Sprite):
	def __init__(self, win, pos):
		pygame.sprite.Sprite.__init__(self)
		self.reset(win, pos)

		self.speed = 3

	def update(self, pressed_keys, scroll_left, scroll_right):
		dx, dy = 0, 0

		# handling keyboard inputs
		if (pressed_keys[K_UP] or pressed_keys[K_SPACE]) and not self.jumped:
				self.vel_y = -10
				self.jumped = True
		if (pressed_keys[K_UP] or pressed_keys[K_SPACE]) == False:
			self.jumped = False
		if pressed_keys[K_LEFT]:
			dx -= self.speed
			scroll_left = True
		if pressed_keys[K_RIGHT]:
			dx += self.speed
			scroll_right = False


		# adding gravity
		self.vel_y += 1
		dy += self.vel_y


		self.rect.x += dx
		self.rect.y += dy
		if self.rect.y >= HEIGHT - 20:
			self.rect.y = HEIGHT - 20

		self.draw()
		return scroll_left, scroll_right

	def draw(self):
		self.win.blit(self.image, self.rect)

	def reset(self, win, pos):
		x, y = pos
		self.win = win

		self.image = pygame.image.load('assets/ball.png')
		self.rect = self.image.get_rect(center=(x,y))

		self.vel_y = 0
		self.jumped = False

# -------------------------------------------------------------------------------------------------
#											 Custom Functions

def load_level(level):
	game_level = f'levels/level{level}_data'
	data = None
	if os.path.exists(game_level):
		f = open(game_level, 'rb')
		data = pickle.load(f)
		f.close()

	return data