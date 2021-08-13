import pygame
import random
import math

SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2

pygame.font.init()
pygame.mixer.init()

tile = pygame.image.load('Assets/tile.png')

class Balls(pygame.sprite.Sprite):
	def __init__(self, pos, radius, angle, win):
		super(Balls, self).__init__()
		
		self.initial_pos = pos
		self.radius = radius
		self.initial_angle = angle
		self.win = win
		self.reset()

		self.rect = pygame.draw.circle(self.win, (25, 25, 25), (self.x,self.y), 6)

	def update(self, color):
		x = round(CENTER[0] + self.radius * math.cos(self.angle * math.pi / 180))
		y = round(CENTER[1] + self.radius * math.sin(self.angle * math.pi / 180))

		self.angle += self.dtheta

		self.step += 1
		if self.step % 5 == 0:
			self.pos_list.append((x,y))
		if len(self.pos_list) > 5:
			self.pos_list.pop(0)

		pygame.draw.circle(self.win, (255, 255, 255), (x,y), 7)
		self.rect = pygame.draw.circle(self.win, color, (x,y), 6)

		for index, pos in enumerate(self.pos_list):
			if index < 3:
				radius = 1
			else:
				radius = 2
			pygame.draw.circle(self.win, color, pos, radius)

	def reset(self):
		self.x, self.y = self.initial_pos
		self.angle = self.initial_angle
		self.dtheta = -2

		self.pos_list = []
		self.step = 0

class Coins(pygame.sprite.Sprite):
	def __init__(self, y, win):
		super(Coins, self).__init__()

		self.y = y
		self.win = win
		self.size = 15

		self.x = WIDTH + 20
		self.dx = -1
		self.s = 1

		self.rect = pygame.draw.rect(self.win, (255, 255, 255), (self.x, self.y, self.size, self.size))

	def update(self, color):
		self.x += self.dx
		if self.x < -20:
			self.kill()

		pygame.draw.rect(self.win, (200, 200, 200), (self.x+self.s, self.y+self.s, self.size, self.size))
		self.rect = pygame.draw.rect(self.win, color, (self.x, self.y, self.size, self.size))
		pygame.draw.circle(self.win, (255,255,255), self.rect.center, 2)

class Tiles(pygame.sprite.Sprite):
	def __init__(self, y, type_, win):
		super(Tiles, self).__init__()

		self.x = WIDTH+10
		self.y = y
		self.type = type_
		self.win = win

		self.angle = 0
		self.dtheta = 0
		self.dx = -1

		if self.type == 1:
			width = 60
			height = 20
		elif self.type == 2:
			width = 20
			height = 40
		elif self.type == 3:
			width = 40
			height = 20
			self.dtheta = -1


		self.image = pygame.Surface((width, height))
		# pygame.draw.rect(self.image, (255, 255, 255), (self.x, self.y, width, height), border_radius=5)
		self.rect = self.image.get_rect(center=(self.x, self.y))

	def rotate(self):
		image = pygame.transform.rotozoom(self.image, self.angle, 1)
		rect = image.get_rect(center=self.rect.center)

		return image, rect

	def update(self):
		self.rect.x += self.dx
		if self.rect.right < 0:
			self.kill()
		
		self.angle += self.dtheta
		image, self.rect = self.rotate()

		self.win.blit(image, self.rect)
