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
		self.health = 100
		self.alive = True
		self.width = self.image.get_width()


	def update(self, moving_left, moving_right):
		if self.alive:
			if moving_left and self.rect.x > 2:
				self.rect.x -= self.speed

			if moving_right and self.rect.x < WIDTH - self.width:
				self.rect.x += self.speed

			if self.health <= 0:
				self.alive = False

			self.counter += 1
			if self.counter >= 2:
				self.index = (self.index + 1) % len(self.image_list)
				self.image = self.image_list[self.index]
				self.counter = 0

	def draw(self, win):
		if self.alive:
			win.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y, type_):
		super(Enemy, self).__init__()

		self.type = type_
		self.image_list = []
		for i in range(2):
			if type_ == 1:
				img = pygame.image.load(f'Assets/Enemies/enemy1-{i+1}.png')
			if type_ == 2:
				img = pygame.image.load(f'Assets/Enemies/enemy2-{i+1}.png')
			if type_ == 3:
				img = pygame.image.load(f'Assets/Enemies/enemy3-{i+1}.png')
			if type_ == 4:
				img = pygame.image.load(f'Assets/Choppers/chopper1-{i+1}.png')
			if type_ == 5:
				img = pygame.image.load(f'Assets/Choppers/chopper2-{i+1}.png')

			w, h = img.get_width(), img.get_height()
			height = (100 * h) // w
			img = pygame.transform.scale(img, (100, height))

			self.image_list.append(img)

		self.index = 0
		self.image = self.image_list[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.frame_dict = {1:3, 2:3, 3:3, 4:5, 5:4}
		self.frame_fps = self.frame_dict[type_]

		self.counter = 0
		self.bullet_counter = 0
		self.speed = 1
		self.health = 100

	def shoot(self, enemy_bullet_group):
		if self.type in (1, 4, 5):
			x, y = self.rect.center
			b = Bullet(x, y, self.type)
			enemy_bullet_group.add(b)
		if self.type in (2, 3):
			x, y = self.rect.center
			b = Bullet(x-25, y+10, self.type)
			enemy_bullet_group.add(b)
			b = Bullet(x+25, y+10, self.type)
			enemy_bullet_group.add(b)


	def update(self, enemy_bullet_group, explosion_group):
		self.rect.y += self.speed
		if self.rect.top >= HEIGHT:
			self.kill()

		if self.health <= 0:
			x, y = self.rect.center
			explosion = Explosion(x, y, 2)
			explosion_group.add(explosion)

			self.kill()

		self.bullet_counter += 1
		if self.bullet_counter >= 60:
			self.shoot(enemy_bullet_group)
			self.bullet_counter = 0

		self.counter += 1
		if self.counter >= self.frame_fps:
			self.index = (self.index + 1) % len(self.image_list)
			self.image = self.image_list[self.index]
			self.counter = 0

	def draw(self, win):
		win.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, type_):
		super(Bullet, self).__init__()
		
		if type_ == 1:
			self.image = pygame.image.load(f'Assets/Bullets/1.png')
			self.image = pygame.transform.scale(self.image, (20, 40))
		if type_ == 2:
			self.image = pygame.image.load(f'Assets/Bullets/2.png')
			self.image = pygame.transform.scale(self.image, (15, 30))
		if type_ == 3:
			self.image = pygame.image.load(f'Assets/Bullets/3.png')
			self.image = pygame.transform.scale(self.image, (20, 40))
		if type_ in (4, 5):
			self.image = pygame.image.load('Assets/Bullets/4.png')
			self.image = pygame.transform.scale(self.image, (20, 20))
		if type_ == 6:
			self.image = pygame.image.load('Assets/Bullets/red_fire.png')
			self.image = pygame.transform.scale(self.image, (15, 30))

		self.rect = self.image.get_rect(center=(x, y))
		if type_ == 6:
			self.speed = -3
		else:
			self.speed = 3

		self.damage_dict = {1:5, 2:10, 3:15, 4:25, 5:25, 6:20}
		self.damage = self.damage_dict[type_]

	def update(self):
		self.rect.y += self.speed
		if self.rect.bottom <= 0:
			self.kill()

	def draw(self, win):
		win.blit(self.image, self.rect)


class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, type_):
		super(Explosion, self).__init__()

		self.img_list = []
		if type_ == 1:
			self.length = 3
		elif type_ == 2:
			self.length = 8

		for i in range(self.length):
			img = pygame.image.load(f'Assets/Explosion{type_}/{i+1}.png')
			w, h = img.get_size()
			width = int(w * 0.40)
			height = int(h * 0.40)
			img = pygame.transform.scale(img, (width, height))
			self.img_list.append(img)

		self.index = 0
		self.image = self.img_list[self.index]
		self.rect = self.image.get_rect(center=(x, y))

		self.counter = 0

	def update(self):
		self.counter += 1
		if self.counter >= 7:
			self.index += 1
			if self.index >= len(self.img_list):
				self.kill()
			else:
				self.image = self.img_list[self.index]
				self.counter = 0

	def draw(self, win):
		win.blit(self.image, self.rect)