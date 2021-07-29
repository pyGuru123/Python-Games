import pygame
import random
import math

SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2
TILE_Y = 100

pygame.font.init()
pygame.mixer.init()

skull_image = pygame.image.load('Assets/skull.png')
skull_image = pygame.transform.scale(skull_image, (15,15))


class Tile(pygame.sprite.Sprite):
	def __init__(self, index, type_, win):
		super(Tile, self).__init__()

		self.index = index
		self.type = type_
		self.win = win

		self.width = 20
		self.height = 60
		self.gap = 10
		self.color = (255, 255, 255)
		self.is_deadly = False
		
		self.x = index * self.width + (index + 2) * self.gap + 9
		if self.type == 1:
			self.y = TILE_Y
		elif self.type == 2:
			self.y = HEIGHT - 1.5 * TILE_Y

		self.rect = pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))

	def update(self):
		pygame.draw.rect(self.win, (12, 12, 12), (self.x+3, self.y+3, self.width, self.height))
		self.rect = pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))
		
		if self.is_deadly:
			self.win.blit(skull_image, (self.x + self.width//2 - 8, self.y + self.height//2 - 8))


class Player:
	def __init__(self, win):
		self.win = win
		self.reset()

	def shadow(self):
		pygame.draw.circle(self.win, (12, 12, 12), (self.x, self.y), self.shadow_radius)
		self.counter += 1
		if self.counter % 5 == 0:
			self.shadow_radius += self.dr
			if self.shadow_radius >= 25 or self.shadow_radius <= 16:
				self.dr *= -1

	def update(self, color):
		if self.y + self.radius < TILE_Y + 60 - 1:
			self.y = TILE_Y + 60 + self.radius - 1
			self.reset_pos()
			self.can_move = True
		elif self.y + self.radius > HEIGHT - 1.5 * TILE_Y + 1:
			self.y = HEIGHT - 1.5 * TILE_Y - self.radius + 1
			self.reset_pos()
			self.can_move = True

				
		self.x += self.dx * self.vel
		self.y += self.dy * self.vel

		self.rect = pygame.draw.circle(self.win, color, (self.x, self.y), self.radius)
		pygame.draw.circle(self.win, (255, 255, 255), (self.x, self.y), 6)
		pygame.draw.circle(self.win, (0, 0, 0), (self.x, self.y), 3)

	def set_move(self, x, y, index, type_):
		if self.can_move:
			self.index = index
			self.type = type_
			dx = x - self.x
			dy = y - self.y
			angle = math.atan2(dy, dx)
			self.dx = math.cos(angle)
			self.dy = math.sin(angle)

			self.can_move = False

	def reset_pos(self):
		self.x = self.index * 20 + (self.index + 2) * 10 + 20
		self.dx = self.dy = 0

	def reset(self):
		self.radius = 10
		self.shadow_radius = 20

		self.x = 5 * 20 + 7 * 10 + 20
		self.y = TILE_Y + 60 + self.radius
		self.vel = 8

		self.counter = 0
		self.dr = 1
		self.dx = self.dy = 0
		self.can_move = True

		self.rect = pygame.draw.circle(self.win, (0,0,0), (self.x, self.y), 10)

class Path:
	def __init__(self, p, tile_group, win):
		self.player = p
		self.tile_group = tile_group
		self.win = win
		self.d = 10
		self.di = 1
		self.index = -1

		self.points = []
		self.counter = 0

	def reset(self):
		self.index = -1
		self.points = []
		self.counter = 0

	def get_direction(self):
		self.points.clear()
		tile = self.tile_group.sprites()[self.index]
		x = tile.rect.centerx
		if self.player.type == 1:
			y = tile.rect.bottom
		elif self.player.type == 2:
			y = tile.rect.top
		dx = x - self.player.x
		dy = y - self.player.y
		angle = math.atan2(dy, dx)
		thetax = math.cos(angle)
		thetay = math.sin(angle)

		for i in range(5):
			pointx = self.player.x + thetax * self.d * i
			pointy = self.player.y + thetay * self.d * i
			self.points.append((pointx, pointy))

	def update(self):
		if self.index == -1:
			self.index = self.player.index
			self.get_direction()

		self.counter += 1
		if self.counter % 25 == 0:
			self.index += self.di
			if self.index > 7:
				self.index = 6
				self.di *= -1
			if self.index < 0:
				self.index = 1
				self.di *= -1

			self.get_direction()
			
		for index, point in enumerate(self.points):
			pygame.draw.circle(self.win, (255, 255, 255), point, 5-index)

