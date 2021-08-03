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
		self.is_target_tile = False
		self.is_deadly_tile = False
		
		self.x = index * self.width + (index + 2) * self.gap + 9
		if self.type == 1:
			self.y = TILE_Y
		elif self.type == 2:
			self.y = HEIGHT - int(1.5 * TILE_Y)

		self.rect = pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))

	def highlight(self):
		pygame.draw.rect(self.win, (255, 70, 70), (self.x, self.y, self.width, self.height), 2)

	def check_collision(self, p):
		if self.rect.colliderect(p.rect):
			p.x = self.rect.x + self.width // 2
			if self.type == 1:
				p.y = TILE_Y + self.height + p.radius + 1
			elif self.type == 2:
				p.y = HEIGHT - int(1.5 * TILE_Y) - p.radius

			p.dx = p.dy = 0
			p.can_move = True
			p.tile_type = self.type

			if not p.first_tile:
				p.first_tile = True

			return True

		return False

	def update(self):
		pygame.draw.rect(self.win, (12, 12, 12), (self.x+3, self.y+3, self.width, self.height))
		self.rect = pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))
		
		if self.is_deadly_tile:
			self.win.blit(skull_image, (self.x + self.width//2 - 8, self.y + self.height//2 - 8))

class Player:
	def __init__(self, win, tile_group):
		self.win = win
		self.tile_group = tile_group
		self.reset()
		self.reset_path_variables()

	def reset(self):
		self.radius = 10
		self.shadow_radius = 20
		self.first_tile = False

		self.x = WIDTH + 10
		self.y = HEIGHT // 2 - 100 
		self.vel = 8
		self.tile_type = None

		self.counter = 0
		self.dr = 1
		self.dx = self.dy = 0
		self.can_move = True
		self.new_tile = True

		self.set_move(159, HEIGHT - int(1.5 * TILE_Y), 4)
		self.rect = pygame.draw.circle(self.win, (0,0,0), (self.x, self.y), 10)

	def reset_path_variables(self):
		self.path_d = 10
		self.path_di = 1
		self.path_index = -1

		self.path_points = []
		self.path_counter = 0

		self.path_x = 0
		self.path_y = 0

	def get_path_direction(self):
		self.path_points.clear()
		if self.tile_type == 1:
			index = 2 * self.path_index + 1
			self.path_y = HEIGHT - int(1.5 * TILE_Y)
		else:
			index = 2 * self.path_index
			self.path_y = TILE_Y + 60
		self.path_target_tile = self.tile_group.sprites()[index]
		self.path_x = self.path_target_tile.rect.centerx

		dx = self.path_x - self.x
		dy = self.path_y - self.y
		angle = math.atan2(dy, dx)
		thetax = math.cos(angle)
		thetay = math.sin(angle)

		for i in range(5):
			pointx = self.x + thetax * self.path_d * i
			pointy = self.y + thetay * self.path_d * i
			self.path_points.append((pointx, pointy))


	def draw_path(self, color):
		if self.path_index == -1:
			self.path_index = self.index
			self.get_path_direction()

		self.path_counter += 1
		if self.path_counter % 15 == 0:
			self.path_index += self.path_di
			if self.path_index > 7:
				self.path_index = 6
				self.path_di *= -1
			if self.path_index < 0:
				self.path_index = 1
				self.path_di *= -1

			self.get_path_direction()
			
		for index, point in enumerate(self.path_points):
			pygame.draw.circle(self.win, color, point, 5-index)

	def update(self, color, player_alive):
		if player_alive:
			if self.can_move:
				self.draw_shadow()
				self.draw_path(color)
					
			self.x += self.dx * self.vel
			self.y += self.dy * self.vel

			self.rect = pygame.draw.circle(self.win, color, (self.x, self.y), self.radius)
			pygame.draw.circle(self.win, (255, 255, 255), (self.x, self.y), 6)
			pygame.draw.circle(self.win, (0, 0, 0), (self.x, self.y), 3)

	def draw_shadow(self):
		pygame.draw.circle(self.win, (12, 12, 12), (self.x, self.y), self.shadow_radius)
		self.counter += 1
		if self.counter % 5 == 0:
			self.shadow_radius += self.dr
			if self.shadow_radius >= 25 or self.shadow_radius <= 16:
				self.dr *= -1

	def set_move(self, x, y, index):
		if self.can_move:
			self.index = index
			dx = x - self.x
			dy = y - self.y
			angle = math.atan2(dy, dx)
			self.dx = math.cos(angle)
			self.dy = math.sin(angle)

			self.can_move = False
			self.new_tile = False
			self.path_index = -1

class Particle(pygame.sprite.Sprite):
	def __init__(self, x, y, color, win):
		super(Particle, self).__init__()
		self.x = x
		self.y = y
		self.color = color
		self.win = win
		self.size = random.randint(4,7)
		xr = (-3,3)
		yr = (-3,3)
		f = 2
		self.life = 40
		self.x_vel = random.randrange(xr[0], xr[1]) * f
		self.y_vel = random.randrange(yr[0], yr[1]) * f
		self.lifetime = 0
			
	def update (self):
		self.size -= 0.1
		self.lifetime += 1
		if self.lifetime <= self.life:
			self.x += self.x_vel
			self.y += self.y_vel
			s = int(self.size)
			pygame.draw.rect(self.win, self.color, (self.x, self.y,s,s))
		else:
			self.kill()