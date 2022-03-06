import pygame

SCREEN = WIDTH, HEIGHT = 288, 512

class Background():
	def __init__(self):
		self.image = pygame.image.load('Assets/road.png')
		self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

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

	def draw(self, win):
		win.blit(self.image, (self.x, self.y1))
		win.blit(self.image, (self.x, self.y2))

	def reset(self):
		self.x = 0
		self.y1 = 0
		self.y2 = -HEIGHT

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, type):
		super(Player, self).__init__()
		self.image = pygame.image.load('Assets/cars/{type}.png')
		self.image = pygame.transform.scale(self.image, (48, 82))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, left, right):
		if left:
			self.rect.x -= 5
		if right:
			self.rect.y += 5

	def draw(self, win):
		win.blit(self.image, self.rect)

class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()
		
		self.scale = scale
		self.image = pygame.transform.scale(img, self.scale)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

	def update_image(self, img):
		self.image = pygame.transform.scale(img, self.scale)

	def draw(self, win):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False

		win.blit(self.image, self.rect)
		return action

# class Coin(pygame.sprite.Sprite):
# 	def __init__(self):
# 		super(Coin, self).__init__()

# 		self.images = []
# 		for i in range(1, 9):
# 			img = pygame.image.load(f'Assets/Coins/{i}.png')
# 			img = pygame.transform.scale(img, (22, 24))
# 			self.images.append(img)

# 		self.index = 0
# 		self.counter = 0

# 	def update(self):
# 		self.counter += 1
# 		if self.counter % 5 == 0:
# 			self.index = (self.index + 1) % len(self.images)

# 	def draw(self, win):
# 		win.blit(self.images[self.index], (100, 100))