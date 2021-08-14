import pygame
import random
import math

SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2

pygame.font.init()
pygame.mixer.init()

class Balls(pygame.sprite.Sprite):
	def __init__(self, pos, radius, angle, win):
		super(Balls, self).__init__()
		
		self.initial_pos = pos
		self.radius = radius
		self.initial_angle = angle
		self.win = win
		self.reset()

		self.rect = pygame.draw.circle(self.win, (25, 25, 25), (self.x,self.y), 6)

	def update(self, color):
		x = round(CENTER[0] + self.radius * math.cos(self.angle * math.pi / 180))
		y = round(CENTER[1] + self.radius * math.sin(self.angle * math.pi / 180))

		self.angle += self.dtheta

		self.step += 1
		if self.step % 5 == 0:
			self.pos_list.append((x,y))
		if len(self.pos_list) > 5:
			self.pos_list.pop(0)

		pygame.draw.circle(self.win, (255, 255, 255), (x,y), 7)
		self.rect = pygame.draw.circle(self.win, color, (x,y), 6)

		for index, pos in enumerate(self.pos_list):
			if index < 3:
				radius = 1
			else:
				radius = 2
			pygame.draw.circle(self.win, color, pos, radius)

	def reset(self):
		self.x, self.y = self.initial_pos
		self.angle = self.initial_angle
		self.dtheta = -2

		self.pos_list = []
		self.step = 0

class Coins(pygame.sprite.Sprite):
	def __init__(self, y, win):
		super(Coins, self).__init__()

		self.y = y
		self.win = win
		self.size = 15

		self.x = WIDTH + 20
		self.dx = -1
		self.s = 1

		self.rect = pygame.draw.rect(self.win, (255, 255, 255), (self.x, self.y, self.size, self.size))

	def update(self, color):
		self.x += self.dx
		if self.x < -20:
			self.kill()

		pygame.draw.rect(self.win, (200, 200, 200), (self.x+self.s, self.y+self.s, self.size, self.size))
		self.rect = pygame.draw.rect(self.win, color, (self.x, self.y, self.size, self.size))
		pygame.draw.circle(self.win, (255,255,255), self.rect.center, 2)

class Tiles(pygame.sprite.Sprite):
	def __init__(self, y, type_, win):
		super(Tiles, self).__init__()

		self.x = WIDTH+10
		self.y = y
		self.type = type_
		self.win = win

		self.angle = 0
		self.dtheta = 0
		self.dx = -1

		if self.type == 1:
			width = 50
			height = 20
		elif self.type == 2:
			width = 20
			height = 50
		elif self.type == 3:
			width = 50
			height = 20
			self.dtheta = 2


		self.image = pygame.Surface((width, height), pygame.SRCALPHA)
		pygame.draw.rect(self.image, (255, 255, 255), (0, 0, width, height), border_radius=8)
		self.rect = self.image.get_rect(center=(self.x, self.y))

	def rotate(self):
		image = pygame.transform.rotozoom(self.image, self.angle, 1)
		rect = image.get_rect(center=self.rect.center)

		return image, rect

	def update(self):
		self.rect.x += self.dx
		if self.rect.right < 0:
			self.kill()
		
		self.angle += self.dtheta
		image, self.rect = self.rotate()

		self.win.blit(image, self.rect)


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


class Message:
	def __init__(self, x, y, size, text, font, color, win):
		self.win = win
		self.color = color
		self.x, self.y = x, y
		if not font:
			self.font = pygame.font.SysFont("Verdana", size)
			anti_alias = True
		else:
			self.font = pygame.font.Font(font, size)
			anti_alias = False
		self.image = self.font.render(text, anti_alias, color)
		self.rect = self.image.get_rect(center=(x,y))
		if self.color == (200, 200, 200):
				self.shadow_color = (255, 255, 255)
		else:
			self.shadow_color = (54,69,79)
		self.shadow = self.font.render(text, anti_alias, self.shadow_color)
		self.shadow_rect = self.image.get_rect(center=(x+2,y+2))
		
	def update(self, text=None, color=None, shadow=True):
		if text:
			if not color:
				color = self.color
			self.image = self.font.render(f"{text}", False, color)
			self.rect = self.image.get_rect(center=(self.x,self.y))
			self.shadow = self.font.render(f"{text}", False, self.shadow_color)
			self.shadow_rect = self.image.get_rect(center=(self.x+2,self.y+2))
		if shadow:
			self.win.blit(self.shadow, self.shadow_rect)
		self.win.blit(self.image, self.rect)

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