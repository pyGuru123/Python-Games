import pygame
import random

SCREEN = WIDTH, HEIGHT = 288, 512

pygame.font.init()
pygame.mixer.init()

flip_fx = pygame.mixer.Sound('Sounds/dash.mp3')

class Player:
	def __init__(self, win):
		self.win = win
		
		self.image = pygame.image.load('Assets/rect.png')
		self.image = pygame.transform.scale(self.image, (16,16))
		self.reset()

		self.dy = 5
		self.frame_top = HEIGHT//2 - 75
		self.frame_bottom = HEIGHT//2 + 75
		
	def update(self, clicked):
		self.rect.y += self.dy

		if clicked:
			self.dy *= -1

		if self.rect.bottom >= self.frame_bottom:
			self.dy *= -1
			self.rect.bottom = self.frame_bottom - 1
			flip_fx.play()
		if self.rect.top <= self.frame_top:
			self.dy *= -1
			self.rect.top = self.frame_top + 1
			flip_fx.play()

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