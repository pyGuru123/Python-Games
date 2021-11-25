import math
import random
import pygame

SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2

MAX_RADIUS = 120
MIN_RADIUS = 90

class Circle(pygame.sprite.Sprite):
	def __init__(self, i):
		super(Circle, self).__init__()
		self.i = i
		self.base = 0
		self.radius = 0
		self.theta = 0
		self.angle = 0

		self.dt = 1
		self.rotate = True
		self.max_rotation = 30
		self.complete = False
		self.shrink = False

		self.image = pygame.image.load('Assets/circle.png')
		self.rect = self.image.get_rect()

	def update(self, shrink):
		self.shrink = shrink

		if not self.complete:
			if self.radius < MAX_RADIUS:
				self.radius += 5
			if self.radius == MAX_RADIUS:
				if self.theta < 30:
					self.theta += 1
				else:
					self.complete = True
			self.angle = (self.base + self.i * self.theta) * math.pi / 180

		if self.complete:
			if self.shrink:
				self.radius -= 1
				if self.radius < MIN_RADIUS:
					self.radius = MIN_RADIUS
			else:
				self.radius += 1
				if self.radius > MAX_RADIUS:
					self.radius = MAX_RADIUS

			if self.rotate and self.radius in (MAX_RADIUS, MIN_RADIUS):
				if abs(self.base) > self.max_rotation:
					self.base = 0
					self.rotate = False
				
				self.base += self.dt
				self.angle += math.radians(self.dt)

		self.x = math.cos(self.angle) * self.radius + CENTER[0]
		self.y = math.sin(self.angle) * self.radius + CENTER[1]

		self.rect = self.image.get_rect(center=(self.x, self.y))
		self.mask = pygame.mask.from_surface(self.image)

	def draw(self, win):
		win.blit(self.image, self.rect)

class Player():
	def __init__(self):
		self.reset()

		self.image = pygame.image.load('Assets/player.png')
		self.rect = self.image.get_rect()

	def reset(self):
		self.radius = 30
		self.theta = 0
		self.rotate = True
		self.speed = 5
		self.dr = self.speed
		self.alive = True

	def update(self, rotate):
		if not rotate:
			self.rotate = False
		if self.rotate:
			self.theta = (self.theta + 2 ) % 360
		else:
			self.radius += self.dr
			if self.radius <= 30:
				self.dr *= -1
				self.rotate = True

		angle = self.theta * math.pi / 180
		self.x = math.cos(angle) * self.radius + CENTER[0]
		self.y = math.sin(angle) * self.radius + CENTER[1]

		self.rect = self.image.get_rect(center=(self.x, self.y))
		self.mask = pygame.mask.from_surface(self.image)

	def draw(self, win):
		win.blit(self.image, self.rect)

class Dot():
	def __init__(self):
		self.radius = 8

	def update(self, x, y, win, color):
		pygame.draw.circle(win, color, (x, y), self.radius)


class Snowflake(pygame.sprite.Sprite):
	def __init__(self, x, y, image=None):
		super(Snowflake, self).__init__()

		self.color = (128, 128, 128)
		self.speed = 3
		self.angle = 0

		self.side = random.randint(15, 40)
		self.image = None
		if image:
			self.image = pygame.image.load(image)
			self.image = pygame.transform.scale(self.image, (self.side, self.side))
			self.rect = self.image.get_rect(center=(x, y))
		else:
			self.surface = pygame.Surface((self.side, self.side), pygame.SRCALPHA)
			self.surface.set_colorkey((200,200,200))
			self.rect = self.surface.get_rect(center=(x, y))

	def update(self, win):
		center = self.rect.center
		self.angle = (self.angle + self.speed) % 360
		if self.image:
			image = pygame.transform.rotate(self.image , self.angle)
			self.rect.x += random.randint(-1, 1)
		else:
			image = pygame.transform.rotate(self.surface , self.angle)
		self.rect = image.get_rect()
		self.rect.center = center

		self.rect.y += 1.5

		if self.rect.top >= HEIGHT:
			self.kill()

		if not self.image:
			pygame.draw.rect(self.surface, self.color, (0,0, self.side, self.side), 4)
		win.blit(image, self.rect)

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


class ScoreCard:
	def __init__(self, x, y, size, style, color,  win):
		self.size = size
		self.color = color
		self.win = win

		self.inc = 1
		self.animate = False
		
		self.style = style
		self.font= pygame.font.Font(self.style, self.size)

		self.image = self.font.render("0", True, self.color)
		self.rect = self.image.get_rect(center=(x,y))
		self.shadow_rect = self.image.get_rect(center=(x+2, y+2))
		
	def update(self, score):
		if self.animate:
			self.size += self.inc
			self.font = pygame.font.Font(self.style, self.size)
			if self.size <= 50 or self.size >= 55:
				self.inc *= -1
				
			if self.size == 50:
				self.animate = False
		self.image = self.font.render(f"{score}", False, self.color)
		shadow = self.font.render(f"{score}", True, (54, 69, 79))
		
		self.win.blit(shadow, self.shadow_rect)
		self.win.blit(self.image, self.rect)
