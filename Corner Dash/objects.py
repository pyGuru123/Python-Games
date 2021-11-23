import math
import random
import pygame

SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2

class Circle(pygame.sprite.Sprite):
	def __init__(self, i):
		super(Circle, self).__init__()
		self.i = i
		self.base = 0
		self.radius = 0
		self.theta = 0

		self.dt = 1
		self.rotate = True
		self.max_rotation = 30
		self.current_theta = 0

	def update(self, win):
		if self.radius < 120:
			self.radius += 5
		if self.radius == 120:
			if self.theta < 30:
				self.theta += 1

		if self.theta == 30 and self.rotate:
			if abs(self.base) > self.max_rotation:
				self.base = 0
				self.rotate = False
			
			self.base += self.dt

		self.angle = (self.base + self.i * self.theta) * math.pi / 180
		self.x = math.cos(self.angle) * self.radius + CENTER[0]
		self.y = math.sin(self.angle) * self.radius + CENTER[1]

		self.rect = pygame.draw.circle(win, (0,0,0), (self.x, self.y), 5)

class Square(pygame.sprite.Sprite):
	def __init__(self, x, y, image=None):
		super(Square, self).__init__()

		self.win = win
		self.color = (128, 128, 128)
		self.speed = 3
		self.angle = 0

		self.side = random.randint(15, 40)
		self.image = None
		if image:
			self.image = pygame.image.load(image)
			self.image = pygame.transform.scale(self.image, (self.side, self.side))
			self.rect = self.image.get_rect(center=(x, y))
		else:
			self.surface = pygame.Surface((self.side, self.side), pygame.SRCALPHA)
			self.surface.set_colorkey((200,200,200))
			self.rect = self.surface.get_rect(center=(x, y))

	def update(self, win):
		center = self.rect.center
		self.angle = (self.angle + self.speed) % 360
		if self.image:
			image = pygame.transform.rotate(self.image , self.angle)
			self.rect.x += random.randint(-1, 1)
		else:
			image = pygame.transform.rotate(self.surface , self.angle)
		self.rect = image.get_rect()
		self.rect.center = center

		self.rect.y += 1.5

		if self.rect.top >= HEIGHT:
			self.kill()

		if not self.image:
			pygame.draw.rect(self.surface, self.color, (0,0, self.side, self.side), 4)
		win.blit(image, self.rect)