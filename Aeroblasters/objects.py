import pygame

SCREEN = WIDTH, HEIGHT = 288, 512

class Background:
	def __init__(self, win):
		self.win = win

		self.image = pygame.image.load('Assets/bg.png')
		self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
		self.rect = self.image.get_rect()
		
		self.reset()
		self.move = True
		
	def update(self, speed):
		if self.move: 
			self.y1 += speed
			self.y2 += speed
			if self.y1 >= HEIGHT:
				self.y1 = -HEIGHT
			if self.y2 >= HEIGHT:
				self.y2 = -HEIGHT
			
		self.win.blit(self.image, (self.x, self.y1))
		self.win.blit(self.image, (self.x, self.y2))
		
	def reset(self):
		self.x = 0
		self.y1 = 0
		self.y2 = -HEIGHT


class Player:
	def __init__(self, x, y):
		
		self.image_list = []
		for i in range(2):
			img = pygame.image.load(f'Assets/player{i+1}.png')
			img = pygame.transform.scale(img, (100, 86))
			self.image_list.append(img)

		self.index = 0
		self.image = self.image_list[self.index]
		self.rect = self.image.get_rect(center=(x, y))

		self.counter = 0
		self.speed = 3
		self.width = self.image.get_width()

	def update(self, moving_left, moving_right):
		if moving_left and self.rect.x > 2:
			self.rect.x -= self.speed

		if moving_right and self.rect.x < WIDTH - self.width:
			self.rect.x += self.speed

		self.counter += 1
		if self.counter >= 2:
			self.index = (self.index + 1) % len(self.image_list)
			self.image = self.image_list[self.index]
			self.counter = 0

	def draw(self, win):
		win.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y, type_):
		super(Enemy, self).__init__()

		self.image_list = []
		for i in range(2):
			if type_ == 1:
				img = pygame.image.load(f'Assets/chopper1-{i+1}.png')
				img = pygame.transform.scale(img, (100, 136))
			if type_ == 2:
				img = pygame.image.load(f'Assets/chopper2-{i+1}.png')
				img = pygame.transform.scale(img, (100, 114))
			self.image_list.append(img)

		self.index = 0
		self.image = self.image_list[self.index]
		self.rect = self.image.get_rect(center=(x, y))

		self.counter = 0
		self.speed = 2

	def shoot(self):
		pass

	def update(self):
		self.rect.y += self.speed
		if self.rect.top >= HEIGHT:
			self.kill()

		self.counter += 1
		if self.counter >= 5:
			self.index = (self.index + 1) % len(self.image_list)
			self.image = self.image_list[self.index]
			self.counter = 0

	def draw(self, win):
		win.blit(self.image, self.rect)