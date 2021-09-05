import pygame

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y, type_, wall_list):
		super(Enemy, self).__init__()
		self.type = type_
		self.wall_list = wall_list
		self.size = 16

		self.image = pygame.image.load('Assets/enemy.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.speed = 2
		if self.type == 1:
			self.vel = (self.speed, 0)
		elif self.type == 2:
			self.vel = (0, self.speed)

		self.dir = 1

	def update(self, screen_scroll):
		dx = (self.vel[0] * self.dir) + screen_scroll
		dy = (self.vel[1] * self.dir)

		for wall in self.wall_list:
			if self.type == 1 and wall[1].colliderect(self.rect.x + dx, self.rect.y, self.size, self.size):
				self.dir *= -1
				dx = 0
			if self.type == 2 and wall[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				self.dir *= -1
				dy = 0
				
		self.rect.x += dx
		self.rect.y += dy

	def draw(self, win):
		win.blit(self.image, self.rect)