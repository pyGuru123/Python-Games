import pygame
import math
import random

SCREEN = WIDTH, HEIGHT = 288, 512
left = 100
top = 150
right = WIDTH - left
bottom = HEIGHT- top
mid = HEIGHT // 2

class Line(pygame.sprite.Sprite):
	def __init__(self, start, end):
		super(Line, self).__init__()
		
		self.x1 = start[0]
		self.y1 = start[1]
		self.x2 = end[0]
		self.y2 = end[1]
		
		self.active = False
		self.counter = 0
		
	def get_center(self):
		return self.rect.centerx, self.rect.centery
	
	def update(self, win, color=None):
		if not color:
			if self.active:
				color = (252,76,2)
				self.counter += 1
				if self.counter % 30 == 0:
					self.active = False
					self.counter = 0
			else:
				color = (0,0,0)
			
		self.rect = pygame.draw.line(win, color, (self.x1, self.y1), (self.x2, self.y2) , 5)
		
class Player(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Player, self).__init__()
		self.x = x
		self.y = y
		self.index = 0
		self.di = 1
		self.alive
		
	def update_index(self):
		self.index = (self.index + self.di) % 6
		if self.index == -1:
			self.index = 5
		
	def update(self, line, color, win):
		if self.alive:
			rect = line.rect
			self.rect = pygame.draw.circle(win, color, (self.x, self.y), 5)
			pygame.draw.circle(win, (255,255,255), (self.x, self.y), 2)
			
			dx =  rect.centerx - self.x
			dy =  rect.centery - self.y 
			angle = math.atan2(dy, dx)
			thetax = math.cos(angle)
			thetay = math.sin(angle)
				
			self.x += thetax
			self.y += thetay
				
			if self.rect.collidepoint((rect.centerx, rect.centery)):
				self.update_index()
				line.active = True
		
class Ball(pygame.sprite.Sprite):
	def __init__(self, win):
		super(Ball, self).__init__()
		
		self.positions = [
			([30, HEIGHT//2], [WIDTH-30, HEIGHT//2]),
			([WIDTH-30, HEIGHT//2], [30, HEIGHT//2] ),
			([left-7, top+5], [right+7, bottom-5]),
			([right+7, bottom-5], [left-7, top+5]),
			([right+7, top+5], [left-7, bottom-5]),
			([left-7, bottom-5], [right+7, top+5])
		]
		
		self.pos = random.randint(0, len(self.positions)-1)
		self.position = self.positions[self.pos]
		self.start = self.position[0]
		self.end = self.position[1]
		self.rect = pygame.draw.circle(win, (0,0,0), self.start, 5)
		
	def update(self, win):
		dx =  self.end[0] - self.start[0]
		dy =  self.end[1] - self.start[1]
		angle = math.atan2(dy, dx)
		thetax = math.cos(angle)
		thetay = math.sin(angle)
		
		self.start[0] += thetax
		self.start[1] += thetay
		
		if self.rect.collidepoint(self.end):
			self.kill()
		
		self.rect = pygame.draw.circle(win, (0,0,0), self.start, 5)
		
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