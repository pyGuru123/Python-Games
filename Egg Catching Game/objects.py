import pygame
import random

# Setup *****************************************

SCREEN = WIDTH, HEIGHT = 600, 960
xoffset, yoffset = 70, 100

BLACK = (0,0,0)
RED = (255, 0, 0)

x_list = [120, 260, 400, 520]

# Classes ***************************************

class Egg(pygame.sprite.Sprite):
	def __init__(self, x, y, win):
		super(Egg, self).__init__()
		
		self.win = win
		self.image = pygame.image.load('Assets/egg.png')
		self.image = pygame.transform.scale(self.image, (60,80))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
	def update(self, speed):
		self.rect.y += speed
		self.win.blit(self.image, self.rect)
		
class Basket:
		def __init__(self, x, y, win):
			self.win = win
			self.image = pygame.image.load('Assets/basket.png')
			self.image = pygame.transform.scale(self.image, (120,60))
			self.rect = self.image.get_rect()
			self.rect.x = x
			self.rect.y = y

		def update(self):
			self.win.blit(self.image, self.rect)
			
		def check_collision(self, rect):
			return self.rect.colliderect(rect)
			
class Splash(pygame.sprite.Sprite):
		def __init__(self, x, y, win):
			super(Splash, self).__init__()
			self.win = win
			self.image = pygame.image.load('Assets/splash.png')
			self.image = pygame.transform.scale(self.image, (80,60))
			self.rect = self.image.get_rect()
			self.rect.x = x
			self.rect.y = y

			self.count = 0

		def update(self):
			self.count += 1
			if self.count >= 50:
				self.kill()
				
			self.win.blit(self.image, self.rect)
			
class ScoreText(pygame.sprite.Sprite):
	def __init__(self, text, font, pos, win):
		super(ScoreText, self).__init__()
		
		self.win = win
		self.image = font.render(text, True, (0, 100, 0))
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]
		
		self.counter = 0

	def update(self):
		self.counter += 1
		if self.counter >= 30:
			self.kill()
			
		self.win.blit(self.image, self.rect)
			
class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()
		
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

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
		
# Functions *************************************
		
def getEggPos():
	x= random.choice(x_list)
	y = yoffset + 160
	return x, y

def display_score(score, font, pos):
	score_img = font.render(f'Score : {score}', True, (34, 139, 34))
	score_rect = score_img.get_rect()
	score_rect.x = pos[0]
	score_rect.y = pos[1]
	
	return score_img, score_rect