import math
import random
import pygame

SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2

def get_circle_position(angle, radius=115):
	angle = angle * math.pi / 180
	x = math.cos(angle) * radius + CENTER[0]
	y = math.sin(angle) * radius + CENTER[1]

	return x, y

def rotate_image(image, rect, angle):
	center = rect.center
	angle = (angle + 2) % 360
	img = pygame.transform.rotate(image , angle)
	rect = img.get_rect()
	rect.center = center

	return img, rect, angle

class Ball(pygame.sprite.Sprite):
	def __init__(self, pos, radius, angle, win):
		super(Ball, self).__init__()
		
		self.initial_pos = pos
		self.radius = radius
		self.initial_angle = angle
		self.win = win
		self.reset()

		self.rect = pygame.draw.circle(self.win, (25, 25, 25), (self.x,self.y), 6)

	def update(self, color, rotate):
		if self.alive:
				x = round(CENTER[0] + self.radius * math.cos(self.angle * math.pi / 180))
				y = round(CENTER[1] + self.radius * math.sin(self.angle * math.pi / 180))

				if rotate:
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
		self.alive = True
		self.x, self.y = self.initial_pos
		self.angle = self.initial_angle
		self.dtheta = -2

		self.pos_list = []
		self.step = 0

class Line(pygame.sprite.Sprite):
	def __init__(self, type, win):
		super(Line, self).__init__()

		self.win = win
		self.x = WIDTH // 2
		self.height = 120

		if type == 1:
			self.y = 136
		if type == 2:
			self.y = 256

		self.rect = pygame.draw.line(self.win, (0,0,0), (self.x, self.y),
					(self.x, self.y+self.height), 2)

	def update(self, color):
		pygame.draw.line(self.win, (70,70,70), (self.x, self.y),
					(self.x, self.y+self.height), 5)
		self.rect = pygame.draw.line(self.win, color, (self.x, self.y),
					(self.x, self.y+self.height), 2)

class Circle(pygame.sprite.Sprite):
	def __init__(self, x, y, type, win):
		super(Circle, self).__init__()

		self.x, self.y = x, y
		self.win = win
		self.radius = 7

		self.d = random.randint(4, 8) / 10
		if type == 1:
			self.dx = -self.d
			self.dy = -self.d
		if type == 2:
			self.dx = self.d
			self.dy = -self.d
		if type == 3:
			self.dx = self.d
			self.dy = self.d
		if type ==4:
			self.dx = -self.d
			self.dy = self.d

		self.distance = 0

	def update(self):
		self.x += self.dx
		self.y += self.dy
		self.distance += self.d

		if self.distance >= 55:
			self.dx *= -1
			self.dy *= -1
			self.distance = 0

		self.rect = pygame.draw.circle(self.win, (30, 30, 30), (self.x, self.y), self.radius)

class Square(pygame.sprite.Sprite):
	def __init__(self, win):
		super(Square, self).__init__()

		self.win = win
		self.color = (128, 128, 128)
		self.speed = 3
		self.angle = 0

		self.side = random.randint(15, 40)
		x = random.randint(self.side, WIDTH-self.side)
		y = 0

		self.surface = pygame.Surface((self.side, self.side), pygame.SRCALPHA)
		self.surface.set_colorkey((200,200,200))
		self.rect = self.surface.get_rect(center=(x, y))

	def update(self):
		center = self.rect.center
		self.angle = (self.angle + self.speed) % 360
		image = pygame.transform.rotate(self.surface , self.angle)
		self.rect = image.get_rect()
		self.rect.center = center

		self.rect.y += 1.5

		if self.rect.top >= HEIGHT:
			self.kill()

		pygame.draw.rect(self.surface, self.color, (0,0, self.side, self.side), 4)
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
		self.shadow_rect = self.image.get_rect(center=(x+3, y+3))
		
	def update(self, score):
		if self.animate:
			self.size += self.inc
			self.font = pygame.font.Font(self.style, self.size)
			if self.size <= 50 or self.size >= 55:
				self.inc *= -1
				
			if self.size == 50:
				self.animate = False
		self.image = self.font.render(f"{score}", False, self.color)
		shadow = self.font.render(f"{score}", True, (54, 69, 79) )	
		
		self.win.blit(shadow, self.shadow_rect)
		self.win.blit(self.image, self.rect)

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

class BlinkingText(Message):
	def __init__(self, x, y, size, text, font, color, win):
		super(BlinkingText, self).__init__(x, y, size, text, font, color, win)
		self.index = 0
		self.show = True

	def update(self):
		self.index += 1
		if self.index % 40 == 0:
			self.show = not self.show

		if self.show:
			self.win.blit(self.image, self.rect)
