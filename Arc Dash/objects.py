import pygame
import random
import math

SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2
MAX_RAD = 120

pygame.font.init()
pygame.mixer.init()


class Player:
	def __init__(self, win):
		self.win = win
		self.reset()
		
	def update(self, player_alive, color, shadow_group):
		if player_alive:
			if self.x <= CENTER[0] - MAX_RAD or self.x >= CENTER[0] + MAX_RAD or \
				self.y <= CENTER[1] - MAX_RAD or self.y >= CENTER[1] + MAX_RAD:
					if self.dx:
						self.dx *= -1
					elif self.dy:
						self.dy *= -1

					shadow_group.empty()

			if self.index == 1 and self.y > CENTER[1]:
					self.reset_pos()
					self.can_move = True
			elif self.index == 2 and self.x < CENTER[0]:
					self.reset_pos()
					self.can_move = True
			elif self.index == 3 and self.y < CENTER[1]:
					self.reset_pos()
					self.can_move = True
			elif self.index == 4 and self.x > CENTER[0]:
					self.reset_pos()
					self.can_move = True

			self.x += self.dx
			self.y += self.dy

			self.rect = pygame.draw.circle(self.win, (255, 255, 255), (self.x, self.y), 6)
			pygame.draw.circle(self.win, color, (self.x, self.y), 3)

	def set_move(self, index):
		if self.can_move:
			self.index = index
			if index == 1:
				self.dy = -self.vel
			if index == 2:
				self.dx = self.vel
			if index == 3:
				self.dy = self.vel
			if index == 4:
				self.dx = -self.vel

			self.can_move = False

	def reset_pos(self):
		self.x = CENTER[0]
		self.y = CENTER[1]
		self.dx = self.dy = 0

	def reset(self):
		self.x = CENTER[0]
		self.y = CENTER[1]
		self.vel = 6

		self.index = None
		self.dx = self.dy = 0
		self.can_move = True

class Dot(pygame.sprite.Sprite):
	def __init__(self, x, y, win):
		super(Dot, self).__init__()
		
		self.x = x
		self.y = y
		self.color = (255, 255, 255)
		self.win = win

		self.rect = pygame.draw.circle(win, self.color, (x,y), 6)
		
	def update(self):
		pygame.draw.circle(self.win, self.color, (self.x,self.y), 6)
		self.rect = pygame.draw.circle(self.win, self.color, (self.x,self.y), 6)

class ShadowImage:
	def __init__(self):
		self.image = pygame.Surface((10, 100), pygame.SRCALPHA)
		self.image.fill((255, 255, 255, 100))
		self.rect = self.image.get_rect()

	def rotate(self, angle):
		rotated = pygame.transform.rotate(self.image, angle)
		self.rect = rotated.get_rect()
		return rotated


class Shadow(pygame.sprite.Sprite):
	def __init__(self, index, win):
		super(Shadow, self).__init__()
		
		self.index = index
		self.win = win
		self.color = (255, 255, 255)
		self.shadow = ShadowImage()


		if self.index == 1:
			self.image = self.shadow.rotate(0)
			self.x = CENTER[0] - 5
			self.y = CENTER[1] - MAX_RAD + 10
		if self.index == 2:
			self.image = self.shadow.rotate(90)
			self.x = CENTER[0] + 10
			self.y = CENTER[1] - 5
		if self.index == 3:
			self.image = self.shadow.rotate(0)
			self.x = CENTER[0] - 5
			self.y = CENTER[1] + 10
		if self.index == 4:
			self.image = self.shadow.rotate(-90)
			self.x = CENTER[0] - MAX_RAD + 10
			self.y = CENTER[1] - 5
		
	def update(self):
		self.win.blit(self.image, (self.x,self.y))

class Balls(pygame.sprite.Sprite):
	def __init__(self, pos, type_, inverter, win):
		super(Balls, self).__init__()
		
		self.initial_pos = pos
		self.color = (0,0,0)
		self.type = type_
		self.inverter = inverter
		self.win = win
		self.reset()

		self.rect = pygame.draw.circle(self.win, self.color, (self.x,self.y), 6)

	def update(self):
		dx = 0
		x = round(CENTER[0] + self.radius * math.cos(self.angle * math.pi / 180))
		y = round(CENTER[1] + self.radius * math.sin(self.angle * math.pi / 180))

		self.angle += self.dtheta
		if self.dtheta == 1 and self.angle >= 360:
			self.angle = 0
		elif self.dtheta == -1 and self.angle <= 0:
			self.angle = 360

		self.rect = pygame.draw.circle(self.win, self.color, (x,y), 6)

	def reset(self):
		self.x, self.y = self.initial_pos
		if self.type == 1:

			if self.x == CENTER[0]-105:
				self.angle = 180
			if self.x == CENTER[0]+105:
				self.angle = 0
			if self.x == CENTER[0]-45:
				self.angle = 180
			if self.x == CENTER[0]+45:
				self.angle = 0

			self.radius = abs(CENTER[0] - self.x) - 3
			self.dtheta = 1

		elif self.type == 2:
			
			if self.y == CENTER[1] - 75:
				self.angle = 90
			if self.y == CENTER[1] + 75:
				self.angle = 270

			self.radius = abs(CENTER[1] - self.y) - 3
			self.dtheta = -1


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
		self.shadow = self.font.render(text, anti_alias, (54,69,79))
		self.shadow_rect = self.image.get_rect(center=(x+2,y+2))
		
	def update(self, text=None, shadow=True):
		if text:
			self.image = self.font.render(f"{text}", False, self.color)
			self.rect = self.image.get_rect(center=(self.x,self.y))
			self.shadow = self.font.render(f"{text}", False, (54,69,79))
			self.shadow_rect = self.image.get_rect(center=(self.x+2,self.y+2))
		if shadow:
			self.win.blit(self.shadow, self.shadow_rect)
		self.win.blit(self.image, self.rect)

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