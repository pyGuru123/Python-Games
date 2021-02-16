import math
import random
import pygame
from pygame.locals import (RLEACCEL, K_SPACE)

class Dino(pygame.sprite.Sprite):
	def __init__(self):
		super(Dino, self).__init__()

		self.isRunning = True
		self.isJumping = False
		self.isDead = False

		self.runlist = [f'assets/dino/Run{i+1}.png' for i in range(8)]
		self.jumplist = [f'assets/dino/Jump{i+1}.png' for i in range(12)]
		self.deadlist = [f'assets/dino/Dead{i+1}.png' for i in range(8)]

		self.runindex = 0
		self.jumpindex = 0
		self.deadindex = 0

		self.jumpcount = 0
		self.jumpvalues = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,
						   3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,
						   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
						   0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,
						  -2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,
						  -3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]

		self.hitdict = {0:90, 1:80, 2:80, 3:80 }

		self.image = pygame.image.load(self.runlist[self.runindex]).convert()
		self.image.set_colorkey((0,0,0), RLEACCEL)

		self.x, self.y = 180, 340
		self.rect = self.image.get_rect(center=(self.x, self.y))

	def update(self, pressed_keys):
		if pressed_keys[K_SPACE] and not self.isDead:
			if not self.isJumping:
				self.isJumping = True
				self.jumpindex = 0
				self.isRunning = False
				
		if self.isJumping:
			self.jumpindex += 0.20
			if self.jumpcount > 108:
				self.isJumping = False
				self.isRunning = True
				self.jumpindex = 0
				self.jumpcount = 0
				self.runindex = 0
			else:
				self.y -= self.jumpvalues[self.jumpcount] * 2.5

				index = math.floor(self.jumpindex)
				img = self.jumplist[index]
				self.image = pygame.image.load(img)
				self.rect = self.image.get_rect(center=(self.x, self.y))

				self.jumpcount += 2
		
		elif self.isRunning:
			self.runindex += 0.40
			if self.runindex > len(self.runlist) - 1:
				self.runindex = 0
			index = math.floor(self.runindex)
			img = self.runlist[index]
			self.image = pygame.image.load(img)

		elif self.isDead:
			self.deadindex += 0.20
			if self.deadindex > len(self.deadlist) - 1:
				self.deadindex = len(self.deadlist) - 1
			index = math.floor(self.deadindex)
			img = self.deadlist[index]
			self.image = pygame.image.load(img)

	def is_collided_with(self, sprite):
		distance = self.hitdict[sprite.type]
		x = self.rect[0] + self.rect[2] // 2
		y = self.rect[1] + self.rect[3] // 2
		x1 = sprite.rect[0] + sprite.rect[2] // 2
		y1 = sprite.rect[1] + sprite.rect[3] // 2

		return math.sqrt((x1-x) ** 2 + (y1 - y) ** 2) <= distance

	def is_dead(self):
		self.isJumping = False
		self.isRunning = False
		self.isDead = True



class Cactus(pygame.sprite.Sprite):
	def __init__(self):
		super(Cactus, self).__init__()

		cactuslist = [f'assets/Cactus/c{i+1}.png' for i in range(4)]
		bg = random.choice(cactuslist)
		self.type = cactuslist.index(bg)
		xpos = random.choice(range(900, 1000))

		self.surf = pygame.image.load(bg).convert()
		self.surf.set_colorkey((0,0,0), RLEACCEL)
		self.rect = self.surf.get_rect(center=(xpos,345))

	def update(self):
		self.rect.move_ip(-5,0)
		if self.rect.right < 0:
			self.kill()

class Cloud(pygame.sprite.Sprite):
	def __init__(self):
		super(Cloud, self).__init__()

		cloudlist = [f'assets/clouds/c{i+1}.png' for i in range(3)]
		bg = random.choice(cloudlist)
		xpos = random.choice(range(900, 1000))

		self.surf = pygame.image.load(bg).convert()
		self.surf.set_colorkey((0,0,0), RLEACCEL)
		self.rect = self.surf.get_rect(center=(xpos,100))

	def update(self):
		self.rect.move_ip(-5,0)
		if self.rect.right < 0:
			self.kill()
