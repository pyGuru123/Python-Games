import math
import random
import pygame
from pygame.locals import (RLEACCEL, K_SPACE, K_UP, K_DOWN)

pygame.mixer.init()
jump_sound = pygame.mixer.Sound("music/jump.wav")
die_sound = pygame.mixer.Sound("music/die1.flac")

class Dino(pygame.sprite.Sprite):
	def __init__(self):
		super(Dino, self).__init__()

		self.isRunning = True
		self.isJumping = False
		self.isDucking = False
		self.isDead = False

		self.runlist = [f'assets/dino/Run{i+1}.png' for i in range(8)]
		self.jumplist = [f'assets/dino/Jump{i+1}.png' for i in range(12)]
		self.deadlist = [f'assets/dino/Dead{i+1}.png' for i in range(8)]
		self.ducklist = [f'assets/dino/Duck{i+1}.png' for i in range(10)]

		self.runindex = 0
		self.jumpindex = 0
		self.deadindex = 0
		self.duckindex = 0

		self.jumpcount = 0
		self.jumpvalues = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,
						   3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,
						   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
						   0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,
						  -2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,
						  -3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]

		self.hitdict = {0:85, 1:85, 2:85, 3:85 }

		self.image = pygame.image.load(self.runlist[self.runindex]).convert()
		self.image.set_colorkey((0,0,0), RLEACCEL)

		self.x, self.y = 180, 340
		self.rect = self.image.get_rect(center=(self.x, self.y))

	def update(self, pressed_keys):
		if (pressed_keys[K_SPACE] or pressed_keys[K_UP]):
			if not self.isDead and not self.isDucking:
				if not self.isJumping:
					self.isJumping = True
					self.jumpindex = 0
					self.isRunning = False
					jump_sound.play()

		elif pressed_keys[K_DOWN] and not self.isDead and not self.isJumping:
			if not self.isDucking:
				self.isDucking = True
				self.isJumping = False
				self.isRunning = False
				self.jumpindex = 0
				self.runindex = 0
				self.duckindex = 0
				
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

		elif self.isDucking:
			self.rect = self.image.get_rect(center=(self.x, 350))
			self.duckindex += 0.20
			if self.duckindex > len(self.ducklist) - 1:
				self.duckindex = 0
				self.runindex = 0
				self.isDucking = False
				self.isRunning = True
				self.rect = self.image.get_rect(center=(self.x, 335))
			index = math.floor(self.duckindex)
			img = self.ducklist[index]
			self.image = pygame.image.load(img)

		
		elif self.isRunning:
			if self.rect.bottom != 390:
				self.rect.move(130,390)
			self.runindex += 0.40
			if self.runindex > len(self.runlist) - 1:
				self.runindex = 0
			index = math.floor(self.runindex)
			img = self.runlist[index]
			self.image = pygame.image.load(img)

		elif self.isDead:
			if self.rect.bottom < 390:
				self.rect.move_ip(2, 5)
			else:
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
		die_sound.play()

class Ptera(pygame.sprite.Sprite):
	def __init__(self):
		super(Ptera, self).__init__()

		self.pteralist = [f'assets/Ptera/t{i+1}.png' for i in range(4)]
		self.index = 0
		xpos = random.choice(range(830, 930))

		self.surf = pygame.image.load(self.pteralist[self.index]).convert()
		self.surf.set_colorkey((0,0,0), RLEACCEL)
		self.rect = self.surf.get_rect(center=(xpos,272))

	def update(self, speed):
		self.rect.move_ip(speed,0)
		if self.rect.right < 0:
			self.kill()

		self.index += 0.20
		if self.index > len(self.pteralist) - 1:
			self.index = 0
		index = math.floor(self.index)
		img = self.pteralist[index]
		self.surf = pygame.image.load(img)


class Cactus(pygame.sprite.Sprite):
	def __init__(self):
		super(Cactus, self).__init__()

		cactuslist = [f'assets/Cactus/c{i+1}.png' for i in range(4)]
		bg = random.choice(cactuslist)
		self.type = cactuslist.index(bg)
		posdict = {0:340, 1:325, 2:340, 3:325}
		ypos = posdict[self.type]
		xpos = random.choice(range(730, 830))

		self.surf = pygame.image.load(bg).convert()
		self.surf.set_colorkey((0,0,0), RLEACCEL)
		self.rect = self.surf.get_rect(center=(xpos,ypos))

	def update(self, speed):
		self.rect.move_ip(speed,0)
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

	def update(self, speed):
		self.rect.move_ip(speed,0)
		if self.rect.right < 0:
			self.kill()

class GameOptions(pygame.sprite.Sprite):
	def __init__(self):
		super(GameOptions, self).__init__()

		self.dino_wall = pygame.image.load('assets/dino-wall.png').convert()
		self.dino_wall.set_colorkey((0,0,0), RLEACCEL)
		self.dino_rect = self.dino_wall.get_rect(center=(200,230))

		self.dino_run = pygame.image.load('assets/dino_run.png')
		self.dino_run_rect = self.dino_run.get_rect(center=(520,110))

		self.start = pygame.image.load('assets/game_start.png').convert()
		self.start.set_colorkey((0,0,0), RLEACCEL)
		self.start_rect = self.dino_run.get_rect(center=(500,330))

		self.game_over = pygame.image.load('assets/game_over.png').convert()
		self.game_over.set_colorkey((0,0,0), RLEACCEL)
		self.game_over_rect = self.game_over.get_rect(center=(350,150))

		self.replay = pygame.image.load('assets/replay.png').convert()
		self.replay.set_colorkey((0,0,0), RLEACCEL)
		self.replay_rect = self.replay.get_rect(center=(380,280))

	def update(self, mode='start'):
		pass