import pygame
import random
import math

SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2

pygame.font.init()
pygame.mixer.init()

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