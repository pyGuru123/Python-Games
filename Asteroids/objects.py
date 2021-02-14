import random
import pygame
from pygame.locals import (RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT)

class Rocket(pygame.sprite.Sprite):
	def __init__(self, winsize):
		super(Rocket, self).__init__()

		self.winwidth, self.winheight = winsize
		self.surf = pygame.image.load('assets/rocket.png').convert()
		self.surf.set_colorkey((0,0,0), RLEACCEL)
		self.rect = self.surf.get_rect(center=(250,self.winheight * 0.80))

		self.speed = 5

	def update(self, pressed_keys):
		if pressed_keys[K_UP]:
			self.rect.move_ip(0, -self.speed)
		elif pressed_keys[K_DOWN]:
			self.rect.move_ip(0, self.speed)
		elif pressed_keys[K_LEFT]:
			self.rect.move_ip(-self.speed, 0)
		elif pressed_keys[K_RIGHT]:
			self.rect.move_ip(self.speed, 0)

		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > self.winwidth:
			self.rect.right = self.winwidth
		if self.rect.top < self.winheight * 0.60:
			self.rect.top = self.winheight * 0.60
		if self.rect.bottom > self.winheight:
			self.rect.bottom = self.winheight

class Bullet(pygame.sprite.Sprite):
	def __init__(self, pos, winsize):
		super(Bullet,self).__init__()

		self.winwidth, self.winheight = winsize
		self.surf = pygame.image.load('assets/bullet1.png').convert()
		self.surf.set_colorkey((0,0,0), RLEACCEL)
		self.rect = self.surf.get_rect(center=(pos[0]+32, pos[1]-10))

	def update(self):
		self.rect.move_ip(0,-5)
		if self.rect.bottom < 0:
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, pos):
		super(Explosion, self).__init__()

		self.images = []
		for i in range(17):
			file = f'assets/explosion/Explosion{i}.png'
			image = pygame.image.load(file)
			# image.set_colorkey((255,255,255), RLEACCEL)
			self.images.append(image)

		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.images[0].get_rect(center=pos)

	def update(self):
		self.index += 1
		if self.index > len(self.images) - 2:
			self.kill()
		self.image = self.images[self.index]

class Asteroid(pygame.sprite.Sprite):
	def __init__(self, type, winsize):
		super(Asteroid, self).__init__()

		self.winwidth, self.winheight = winsize

		asteroid_types = {i:f'assets/asteroid{i}.png' for i in range(1,4)}
		img = asteroid_types.get(type)

		self.surf = pygame.image.load(img).convert()
		self.surf.set_colorkey((0,0,0), RLEACCEL)
		self.rect = self.surf.get_rect(center=(
				random.randint(40, self.winwidth-40),
				-random.randint(50, 150)
			))

	def update(self):
		self.rect.move_ip(0, 5)
		if self.rect.top > self.winheight:
			self.kill()

		