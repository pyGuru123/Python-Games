import pygame
import random

SCREEN = WIDTH, HEIGHT = 288, 512

BLUE = (53, 81, 92)
RED = (255, 0, 0)

class Road():
	def __init__(self):
		self.image = pygame.image.load('Assets/road.png')
		self.image = pygame.transform.scale(self.image, (WIDTH-60, HEIGHT))

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
		self.x = 30
		self.y1 = 0
		self.y2 = -HEIGHT

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, type):
		super(Player, self).__init__()
		self.image = pygame.image.load(f'Assets/cars/{type+1}.png')
		self.image = pygame.transform.scale(self.image, (48, 82))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, left, right):
		if left:
			self.rect.x -= 5
			if self.rect.x <= 40:
				self.rect.x = 40
		if right:
			self.rect.x += 5
			if self.rect.right >= 250:
				self.rect.right = 250

	def draw(self, win):
		win.blit(self.image, self.rect)

class Nitro:
	def __init__(self, x, y):
		self.image = pygame.image.load('Assets/nitro.png')
		self.image = pygame.transform.scale(self.image, (42, 42))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.gas = 0

	def update(self, nitro_on):
		if nitro_on:
			self.gas -= 1
			if self.gas <= 0:
				self.gas = 0
		else:
			self.gas += 1
			if self.gas >= 359:
				self.gas = 359

	def draw(self, win):
		win.blit(self.image, self.rect)
		if self.gas and self.gas < 360:
			pygame.draw.arc(win, (255, 255, 255), self.rect, 0, self.gas, 2)


class Tree(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Tree, self).__init__()

		type = random.randint(1, 4)
		self.image = pygame.image.load(f'Assets/trees/{type}.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, speed):
		self.rect.y += speed

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

class Particle(pygame.sprite.Sprite):
	def __init__(self, x, y, size):
		super(Particle, self).__init__()
		self.x = x
		self.y = y
		self.size = random.randint(2, 5)
		self.color = random.choice([BLUE, RED])
		self.life = 60
		self.x_vel = random.random() * random.choice([1, -1])
		self.y_vel = random.randrange(0, 2)
		self.lifetime = 0
			
	def update(self, win):
		self.size -= 0.1
		self.lifetime += 1
		if self.lifetime <= self.life:
			self.x += self.x_vel
			self.y += self.y_vel
			s = int(self.size)
			pygame.draw.rect(win, self.color, (self.x, self.y,s,s))
		else:
			self.kill()

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