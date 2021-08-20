import math
import pygame
from particles import Explosion

WIDTH, HEIGHT = 640, 384

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direction, color, type_, win):
		super(Bullet, self).__init__()

		self.x = x
		self.y = y
		self.direction = direction
		self.color = color
		self.type = type_
		self.win = win

		self.speed = 10
		self.radius = 4
		
		self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.radius)

	def update(self):
		if self.direction == -1:
			self.x -= self.speed
		if self.direction == 0 or self.direction == 1:
			self.x += self.speed

		if self.x < 0 or self.x > WIDTH:
			self.kill()

		self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.radius)

class Grenade(pygame.sprite.Sprite):
	def __init__(self, x, y, direction, win):
		super(Grenade, self).__init__()

		self.x = x
		self.y = y
		self.direction = direction
		self.win = win

		self.speed = 10
		self.vel_y = -11
		self.timer = 15
		self.radius = 4

		if self.direction == 0:
			self.direction = 1

		pygame.draw.circle(self.win, (200, 200, 200), (self.x, self.y), self.radius+1)
		self.rect = pygame.draw.circle(self.win, (255, 50, 50), (self.x, self.y), self.radius)
		pygame.draw.circle(self.win, (0, 0, 0), (self.x, self.y), 1)

	def update(self, p, enemy_group, explosion_group):
		self.vel_y += 1
		dx = self.direction * self.speed
		dy = self.vel_y

		if self.rect.bottom + dy > 200:
			dy = 200 - self.rect.bottom 
			self.speed -= 1
			if self.speed <= 0:
				self.speed = 0

		if self.rect.left + dx < 0 or self.rect.right + dx > WIDTH:
			self.direction *= -1
			dx = self.direction * self.speed

		if self.speed == 0:
			self.timer -= 1
			if self.timer <= 0:
				for _ in range(30):
					explosion = Explosion(self.x, self.y, self.win)
					explosion_group.add(explosion)

				p_distance = math.sqrt((p.rect.centerx - self.x) ** 2 + (p.rect.centery - self.y) ** 2 )
				if p_distance <= 100:
					if p_distance > 80:
						p.health -= 20
					elif p_distance > 40:
						p.health -= 50
					elif p_distance >= 0:
						p.health -= 80
					p.hit = True

				for e in enemy_group:
					e_distance = math.sqrt((e.rect.centerx - self.x) ** 2 + (e.rect.centery - self.y) ** 2)
					if e_distance < 80:
						e.health -= 100

				self.kill()

		self.x += dx
		self.y += dy

		pygame.draw.circle(self.win, (200, 200, 200), (self.x, self.y), self.radius+1)
		self.rect = pygame.draw.circle(self.win, (255, 50, 50), (self.x, self.y), self.radius)
		pygame.draw.circle(self.win, (0, 0, 0), (self.x, self.y), 1)