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

		self.vel = 2

	def update(self, screen_scroll):
		if self.type == 1:
			self.rect.x += self.vel + screen_scroll
		elif self.type == 2:
			self.rect.x += screen_scroll
			self.rect.y += self.vel

		for wall in self.wall_list:			
			if wall[1].colliderect(self.rect):
				self.vel *= -1

	def draw(self, win):
		win.blit(self.image, self.rect)