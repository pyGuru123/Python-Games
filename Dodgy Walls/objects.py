import pygame
import random

SCREEN = WIDTH, HEIGHT = 288, 512

pygame.font.init()
pygame.mixer.init()

dash_fx = pygame.mixer.Sound('Sounds/dash.mp3')
flip_fx = pygame.mixer.Sound('Sounds/flip.mp3')

class Player:
	def __init__(self, win):
		self.win = win
		
		self.image = pygame.image.load('Assets/rect.png')
		self.image = pygame.transform.scale(self.image, (16,16))
		self.reset()

		self.dy = 4
		self.frame_top = HEIGHT//2 - 75
		self.frame_bottom = HEIGHT//2 + 75
		
	def update(self, show_player, clicked):
		if show_player:
			self.rect.y += self.dy

			if clicked:
				if self.rect.y > self.frame_top and self.rect.y < self.frame_bottom:
					self.dy *= -1
					flip_fx.play()

			if self.rect.bottom >= self.frame_bottom:
				self.dy *= -1
				self.rect.bottom = self.frame_bottom - 1
				dash_fx.play()
			if self.rect.top <= self.frame_top:
				self.dy *= -1
				self.rect.top = self.frame_top + 1
				dash_fx.play()

			self.win.blit(self.image, self.rect)
		
	def reset(self):
		self.x = 145
		self.y = 270
		self.rect = self.image.get_rect(center=(self.x,self.y))

class Bar(pygame.sprite.Sprite):
	def __init__(self, x, y, height, color, win):
		super(Bar, self).__init__()
		
		self.rect = pygame.Rect(x, y, 20, height, border_radius = 8)
		self.win = win
		self.color = color
		
	def update(self, speed):
		self.rect.x -= speed
		if self.rect.x <= 0:
			self.kill()
		self.win.fill(self.color, self.rect)


class Dot(pygame.sprite.Sprite):
	def __init__(self, x, y, win):
		super(Dot, self).__init__()
		
		self.x = x
		self.y = y
		self.color = (255, 255, 255)
		self.win = win

		self.rect = pygame.draw.circle(win, self.color, (x,y), 6)
		
	def update(self, speed):
		self.x -= speed
		if self.x <= 0:
			self.kill()
		
		pygame.draw.circle(self.win, self.color, (self.x,self.y), 6)
		self.rect = pygame.draw.circle(self.win, self.color, (self.x,self.y), 6)

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
			if self.size <= 50 or self.size >= 60:
				self.inc *= -1
				
			if self.size == 50:
				self.animate = False
		self.image = self.font.render(f"{score}", False, self.color)
		shadow = self.font.render(f"{score}", True,(54, 69, 79) )	
		
		self.win.blit(shadow, self.shadow_rect)
		self.win.blit(self.image, self.rect)


class Message:
	def __init__(self, x, y, size, text, font, color, win):
		self.win = win
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
		
	def update(self):
		self.win.blit(self.shadow, self.shadow_rect)
		self.win.blit(self.image, self.rect)


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