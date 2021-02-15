import random
import pygame
from pygame.locals import (RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, 
									 K_w, K_s, K_a, K_d)

class Rocket(pygame.sprite.Sprite):
	def __init__(self, winsize):
		super(Rocket, self).__init__()

		self.winwidth, self.winheight = winsize
		self.surf = pygame.image.load('assets/rocket.png').convert()
		self.surf.set_colorkey((0,0,0), RLEACCEL)
		self.rect = self.surf.get_rect(center=(250,self.winheight * 0.50))

		self.speed = 5
		self.dirlist = ['top', 'right', 'bottom', 'left']
		self.dirindex = 0
		self.dir = self.dirlist[self.dirindex]

	def update(self, pressed_keys):
		if pressed_keys[K_UP] or pressed_keys[K_w]:
			self.rect.move_ip(0, -self.speed)
		elif pressed_keys[K_DOWN] or pressed_keys[K_s]:
			self.rect.move_ip(0, self.speed)
		elif pressed_keys[K_LEFT] or pressed_keys[K_a]:
			self.rect.move_ip(-self.speed, 0)
		elif pressed_keys[K_RIGHT] or pressed_keys[K_d]:
			self.rect.move_ip(self.speed, 0)

		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > self.winwidth:
			self.rect.right = self.winwidth
		if self.rect.top < 0:
			self.rect.top = 0
		if self.rect.bottom > self.winheight:
			self.rect.bottom = self.winheight

	def rotate_left(self):
		self.dirindex -= 1
		if self.dirindex < -3:
			self.dirindex = 0 
		self.dir = self.dirlist[self.dirindex]
		self.rotate_center(90)

	def rotate_right(self):
		self.dirindex += 1
		if self.dirindex > 3:
			self.dirindex = 0 
		self.dir = self.dirlist[self.dirindex]
		self.rotate_center(-90)

	def rotate_center(self, angle):
		orig_rect = self.surf.get_rect()
		rot_image = pygame.transform.rotate(self.surf, angle)
		self.rot_rect = orig_rect.copy()
		self.rot_rect.center = rot_image.get_rect().center
		self.surf = rot_image.subsurface(self.rot_rect).copy()

class Bullet(pygame.sprite.Sprite):
	def __init__(self, pos, dir_, winsize):
		super(Bullet,self).__init__()

		self.pos = pos
		self.dir = dir_
		self.winwidth, self.winheight = winsize

		imglist = [f'assets/bullets/b{i}.png' for i in range(1,11)]
		bullet = random.choice(imglist)

		self.surf = pygame.image.load(bullet).convert()
		self.surf.set_colorkey((0,0,0), RLEACCEL)

		position = self.get_bullet_pos(self.pos)
		self.rect = self.surf.get_rect(center=position)

	def get_bullet_pos(self, pos):
		if self.dir == 'top':
			pos = (pos[0]+32, pos[1]-10)
		elif self.dir == 'left':
			pos = (pos[0]-10, pos[1]+32)
		elif self.dir == 'right':
			pos = (pos[0]+74, pos[1]+32)
		elif self.dir == 'bottom':
			pos = (pos[0]+32, pos[1]+74)

		return pos

	def update(self):
		if self.dir == 'top':
			self.rect.move_ip(0,-5)
			if self.rect.bottom < 0:
				self.kill()
		elif self.dir == 'left':
			self.rect.move_ip(-5,0)
			if self.rect.right < 0:
				self.kill()
		elif self.dir == 'bottom':
			self.rect.move_ip(0,5)
			if self.rect.top > self.winheight:
				self.kill()
		elif self.dir == 'right':
			self.rect.move_ip(5,0)
			if self.rect.left > self.winwidth:
				self.kill()

class Asteroid(pygame.sprite.Sprite):
	def __init__(self, type, winsize):
		super(Asteroid, self).__init__()

		self.winwidth, self.winheight = winsize

		asteroid_types = {i:f'assets/asteroids/asteroid{i}.png' for i in range(1,6)}
		img = asteroid_types.get(type)

		self.dirlist = ['top', 'bottom', 'left', 'right']
		self.dir = random.choice(self.dirlist)
		
		self.surf = pygame.image.load(img).convert()
		self.surf.set_colorkey((0,0,0), RLEACCEL)

		pos = self.initial_pos()
		if self.dir in ('top', 'bottom'):
			if pos[0] < self.winwidth / 2:
				self.x = random.choice([0,0,0,1,2,3,4,5])
			elif pos[0] >= self.winwidth / 2:
				self.x = random.choice([0,0,0,-1,-2,-3,-4,-5])
		elif self.dir in ('left', 'right'):
			if pos[1] < self.winheight / 2:
				self.y = random.choice([0,0,0,1,2,3,4,5])
			elif pos[1] >= self.winheight / 2:
				self.y = random.choice([0,0,0,-1,-2,-3,-4,-5])

		self.rect = self.surf.get_rect(center=pos)

	def initial_pos(self):
		if self.dir == 'top':
			pos = (
				random.randint(20, self.winwidth-20),
				-random.randint(50, 150)
			)
		elif self.dir == 'bottom':
			pos = (
				random.randint(20, self.winwidth-20),
				random.randint(self.winheight+50, self.winheight+100)
			)
		elif self.dir == 'left':
			pos = (
				random.randint(-20, 0),
				random.randint(0, self.winheight)
			)
		elif self.dir == 'right':
			pos = (
				random.randint(self.winwidth+20, self.winwidth+70),
				random.randint(0, self.winheight)
			)

		return pos

	def update(self):
		if self.dir == 'top':
			self.rect.move_ip(self.x, 5)
			if self.rect.top > self.winheight:
				self.kill()
		elif self.dir == 'bottom':
			self.rect.move_ip(self.x, -5)
			if self.rect.bottom < 0:
				self.kill()
		elif self.dir == 'left':
			self.rect.move_ip(5, self.y)
			if self.rect.left > self.winwidth:
				self.kill()
		elif self.dir == 'right':
			self.rect.move_ip(-5, self.y)
			if self.rect.right < 0:
				self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, pos):
		super(Explosion, self).__init__()

		self.images = []
		for i in range(17):
			file = f'assets/explosion/Explosion{i}.png'
			image = pygame.image.load(file)
			self.images.append(image)

		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.images[0].get_rect(center=pos)

	def update(self):
		self.index += 1
		if self.index > len(self.images) - 2:
			self.kill()
		self.image = self.images[self.index]