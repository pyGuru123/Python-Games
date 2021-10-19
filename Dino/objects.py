import pygame

SCREEN = WIDTH, HEIGHT = (600, 200)

class Ground():
	def __init__(self):
		self.image = pygame.image.load('Assets/ground.png')
		self.rect = self.image.get_rect()

		self.width = self.image.get_width()
		self.x1 = 0
		self.x2 = self.width
		self.y = 150

	def update(self, speed):
		self.x1 -= speed
		self.x2 -= speed

		if self.x1 <= -self.width:
			self.x1 = self.width

		if self.x2 <= -self.width:
			self.x2 = self.width

	def draw(self, win):
		win.blit(self.image, (self.x1, self.y))
		win.blit(self.image, (self.x2, self.y))


class Dino():
	def __init__(self, x, y):

		self.running_list = []
		for i in range(3, 5):
			img = pygame.image.load(f'Assets/Dino/{i}.png')
			img = pygame.transform.scale(img, (60, 64))
			self.running_list.append(img)

		self.index = 0
		self.image = self.running_list[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.counter = 0

	def update(self):
		self.counter += 1
		if self.counter >= 6:
			self.index = (self.index + 1) % len(self.running_list)
			self.image = self.running_list[self.index]
			self.counter = 0

	def draw(self, win):
		win.blit(self.image, self.rect)