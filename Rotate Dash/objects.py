import math
import random
import pygame

SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2

class Ball(pygame.sprite.Sprite):
	def __init__(self, pos, radius, angle, win):
		super(Ball, self).__init__()
		
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

class Line(pygame.sprite.Sprite):
	def __init__(self, type, win):
		super(Line, self).__init__()

		self.win = win
		self.x = WIDTH // 2
		self.height = 120

		if type == 1:
			self.y = 136
		if type == 2:
			self.y = 256

		self.rect = pygame.draw.line(self.win, (0,0,0), (self.x, self.y),
					(self.x, self.y+self.height), 2)

	def update(self):
		pygame.draw.line(self.win, (70,70,70), (self.x, self.y),
					(self.x, self.y+self.height), 5)
		self.rect = pygame.draw.line(self.win, (0,0,0), (self.x, self.y),
					(self.x, self.y+self.height), 2)