import pygame
import random
import math

SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2
MAX_RAD = 120

pygame.font.init()
pygame.mixer.init()


class Player:
	def __init__(self, win):
		self.win = win
		self.reset()
		
	def update(self, color):
		pygame.draw.circle(self.win, (255, 255, 255), (self.x, self.y), 6)
		pygame.draw.circle(self.win, color, (self.x, self.y), 3)

	def reset(self):
		self.x = CENTER[0]
		self.y = CENTER[1]

		self.dx, self.dy = 1, 1

class Dot(pygame.sprite.Sprite):
	def __init__(self, x, y, win):
		super(Dot, self).__init__()
		
		self.x = x
		self.y = y
		self.color = (255, 255, 255)
		self.win = win

		self.rect = pygame.draw.circle(win, self.color, (x,y), 6)
		
	def update(self):
		pygame.draw.circle(self.win, self.color, (self.x,self.y), 6)
		self.rect = pygame.draw.circle(self.win, self.color, (self.x,self.y), 6)

class ShadowImage:
	def __init__(self):
		self.image = pygame.Surface((10, 100), pygame.SRCALPHA)
		self.image.fill((255, 255, 255, 128))
		self.rect = self.image.get_rect()

	def rotate(self, angle):
		rotated = pygame.transform.rotate(self.image, angle)
		self.rect = rotated.get_rect()
		return rotated


class Shadow(pygame.sprite.Sprite):
	def __init__(self, index, win):
		super(Shadow, self).__init__()
		
		self.index = index
		self.win = win
		self.color = (255, 255, 255)
		self.shadow = ShadowImage()


		if self.index == 1:
			self.image = self.shadow.rotate(0)
			self.x = CENTER[0] - 5
			self.y = CENTER[1] - MAX_RAD + 10
		if self.index == 2:
			self.image = self.shadow.rotate(90)
			self.x = CENTER[0] + 10
			self.y = CENTER[1] - 5
		if self.index == 3:
			self.image = self.shadow.rotate(0)
			self.x = CENTER[0] - 5
			self.y = CENTER[1] + 10
		if self.index == 4:
			self.image = self.shadow.rotate(-90)
			self.x = CENTER[0] - MAX_RAD + 10
			self.y = CENTER[1] - 5
		
	def update(self):
		self.win.blit(self.image, (self.x,self.y))

class Balls(pygame.sprite.Sprite):
	def __init__(self, pos, type_, win):
		super(Balls, self).__init__()
		
		self.initial_pos = pos
		self.color = (0,0,0)
		self.type = type_
		self.win = win
		self.reset()

		self.rect = pygame.draw.circle(self.win, self.color, (self.x,self.y), 6)

	def update(self):
		dx = 0
		x = round(CENTER[0] + self.radius * math.cos(self.angle * math.pi / 180))
		y = round(CENTER[1] + self.radius * math.sin(self.angle * math.pi / 180))

		self.angle += self.dtheta
		if self.dtheta == 1 and self.angle >= 360:
			self.angle = 0
		elif self.dtheta == -1 and self.angle <= 0:
			self.angle = 360

		self.rect = pygame.draw.circle(self.win, self.color, (x,y), 6)

	def reset(self):
		self.x, self.y = self.initial_pos
		if self.type == 1:

			if self.x == CENTER[0]-105:
				self.angle = 180
			if self.x == CENTER[0]+105:
				self.angle = 0
			if self.x == CENTER[0]-45:
				self.angle = 180
			if self.x == CENTER[0]+45:
				self.angle = 0

			self.radius = abs(CENTER[0] - self.x) - 3
			self.dtheta = 1

		elif self.type == 2:
			
			if self.y == CENTER[1] - 75:
				self.angle = 90
			if self.y == CENTER[1] + 75:
				self.angle = 270

			self.radius = abs(CENTER[1] - self.y) - 3
			self.dtheta = -1
		