import math
import random
import pygame

SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2

class Circle(pygame.sprite.Sprite):
	def __init__(self, i):
		super(Circle, self).__init__()
		self.radius = 0
		self.theta = 25
		self.i = i

	def update(self, win):
		if self.radius < 120:
			self.radius += 3
		if self.radius == 120:
			if self.theta < 30:
				self.theta += 0.2
			else:
				self.theta = int(30)

		angle = self.i * self.theta * math.pi / 180
		self.x = math.cos(angle) * self.radius + CENTER[0]
		self.y = math.sin(angle) * self.radius + CENTER[1]

		self.rect = pygame.draw.circle(win, (0,0,0), (self.x, self.y), 5)
