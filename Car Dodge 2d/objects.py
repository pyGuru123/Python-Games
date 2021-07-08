import pygame
import random

# Setup *****************************************

SCREEN = WIDTH, HEIGHT = 540, 960
xoffset, yoffset = 60, 50

BLACK = (0,0,0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

speed = 20

dir_dict = {
	'Up' : pygame.Rect(xoffset + 360, yoffset + HEIGHT + 10, 100, 100),
	'Down' : pygame.Rect(xoffset + 360, yoffset + HEIGHT + 110, 100, 100),
	'Right' :  pygame.Rect(xoffset + 460, yoffset + HEIGHT + 110, 100, 100),
	'Left' : pygame.Rect(xoffset + 260, yoffset + HEIGHT + 110, 100, 100)
}

x_list = [170, 260, 360, 455]

# Classes ***************************************

class Background:
	def __init__(self, win):
		self.win = win

		self.image = pygame.image.load('Assets/road2.png')
		self.image = pygame.transform.scale(self.image, (WIDTH + 90, HEIGHT+100))
		self.rect = self.image.get_rect()
		self.height = self.rect.height - 60
		
		self.reset()
		self.move = True
		
	def update(self):
		if self.move: 
			self.y1 += speed
			self.y2 += speed
			if self.y1 >= self.height:
				self.y1 = -self.height
			if self.y2 >= self.height:
				self.y2 = -self.height
			
		self.win.blit(self.image, (self.x1, self.y1 + yoffset), (15, 0, xoffset + WIDTH, yoffset + HEIGHT))
		self.win.blit(self.image, (self.x2, self.y2 + yoffset), (15, 0, xoffset + WIDTH, yoffset + HEIGHT))
		
	def reset(self):
		self.x1 = xoffset
		self.x2 = xoffset
		self.y1 = 0
		self.y2 = -self.height
			
		

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, win):
		super(Player, self).__init__()
		
		self.win = win
		self.image = pygame.image.load('Assets/car.png')
	#	self.image = pygame.transform.scale(self.image, (90,140))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
	def update(self, pos, speed):
		if pos:
			if dir_dict['Up'].collidepoint(pos):
				if self.rect.y >= yoffset + 250:
					self.rect.y -= speed
			if dir_dict['Down'].collidepoint(pos):
				if self.rect.y <= yoffset + HEIGHT - 200:
					self.rect.y += speed
			if dir_dict['Left'].collidepoint(pos):
				if self.rect.x >= xoffset + 100:
					self.rect.x -= speed
			if dir_dict['Right'].collidepoint(pos):
				if self.rect.x <= xoffset + WIDTH - 115:
					self.rect.x += speed

		self.win.blit(self.image, self.rect)
		
class Enemy(pygame.sprite.Sprite):
	def __init__(self, win):
		super(Enemy, self).__init__()
		self.win = win
		
		cars_list = []
		for i in range(6):
			img = f'Assets/car{i+1}.png'
			sprite = pygame.image.load(img)
			sprite = pygame.transform.flip(sprite, False, True)
			cars_list.append(sprite)
			
		self.image = random.choice(cars_list)
		self.rect = self.image.get_rect()
		self.rect.x = random.choice(x_list)
		self.rect.y = -60
		self.lane = x_list.index(self.rect.x)
		
	def update(self, speed):
		self.rect.y += speed
		self.win.blit(self.image, self.rect)

class Roadblock(pygame.sprite.Sprite):
	def __init__(self, win):
		super(Roadblock, self).__init__()
		self.win = win

		rb_list = []

		self.img1 = pygame.image.load('Assets/roadblock.png')
		self.img1 = pygame.transform.scale(self.img1, (100,70))
		self.img2 = pygame.image.load('Assets/barrel.png')
		self.img2 = pygame.transform.scale(self.img2, (60,90))

		self.im_list = [self.img1, self.img2]
		self.image = random.choice(self.im_list)
		self.rect = self.image.get_rect()
		self.rect.x = random.choice(x_list)
		if self.im_list.index(self.image) == 1:
			self.rect.x += 20
		self.rect.y = -300
		
	def update(self, speed):
		self.rect.y += speed
		self.win.blit(self.image, self.rect)
		
class Coin(pygame.sprite.Sprite):
	def __init__(self, win):
		super(Coin, self).__init__()
		self.win = win

		self.image = pygame.image.load('Assets/coin.png')
		self.image = pygame.transform.scale(self.image, (64, 64))
		self.rect = self.image.get_rect()
		self.rect.x =  random.choice(x_list) + 15
		self.rect.y = -420
		
	def update(self, speed):
		self.rect.y += speed
		self.win.blit(self.image, self.rect)
		


class Counter(pygame.sprite.Sprite):
	def __init__(self, win, font):
		super(Counter, self).__init__()

		self.win = win
		self.font = font
		self.index = 1
		self.count = 3
		self.image = self.font.render(f'{self.count}', True, (255, 255, 255))

	def update(self):
		if self.index % 15 == 0:
			self.count -= 1

		self.index += 1

		if self.count > 0:
			self.image = self.font.render(f'{self.count}', True, (255, 255, 255))
			self.win.blit(self.image, (xoffset + WIDTH // 2 - self.image.get_width() / 2 + 40,yoffset + HEIGHT // 2 - self.image.get_height() / 2))
			
			
class Draw:
	def __init__(self, win):
		self.win = win

	def top_black_bar(self):
		pygame.draw.rect(self.win, BLACK, (xoffset, 0, WIDTH + 100, yoffset))
		
	def bottom_black_bar(self):
		pygame.draw.rect(self.win, BLACK, (xoffset, yoffset + HEIGHT, WIDTH + 100, 390))
		
	def replay_black_bar(self):
		pygame.draw.rect(self.win, BLACK, (xoffset, yoffset + HEIGHT + 390, WIDTH + 100, 100))
		
	def border(self):
		pygame.draw.rect(self.win, WHITE, (xoffset - 10, yoffset - 10, xoffset + WIDTH+ 20, yoffset + HEIGHT + 190), 3, border_radius=12)
		
	def controller(self, image):
		self.win.blit(image, (xoffset + WIDTH // 2 - image.get_width() // 2 + 150, yoffset + HEIGHT + 10))
		
	def coin_hud(self, image):
		self.win.blit(image, (xoffset + 30, yoffset + HEIGHT + 20))
		
	def car_hud(self, image):
		self.win.blit(image, (xoffset + 10, yoffset + HEIGHT + 100))
	
	def horn_hud(self, speedometer, image):
		self.win.blit(speedometer, (xoffset +WIDTH - 270, yoffset + HEIGHT + 16))
		self.win.blit(image, (xoffset +WIDTH - 50, yoffset + HEIGHT + 20))
			
	def update_score(self, score, dodges, speed, font):
			coin_score = font.render(f' {score}', True, (255, 0, 0))
			self.win.blit(coin_score, (xoffset + 140, yoffset + HEIGHT + 20))
			
			car_dodge = font.render(f' {dodges}', True, (255, 0, 0))
			self.win.blit(car_dodge, (xoffset + 140, yoffset + HEIGHT + 110))
			
			speed_val = font.render(f' {speed}', True, (255, 0, 0))
			self.win.blit(speed_val, (xoffset + 205, yoffset + HEIGHT + 18))
			
	def score_box(self, coin_img, car_img, speedometer, score, dodges, speed, font):
		self.win.blit(coin_img, (xoffset + 30, yoffset + HEIGHT + 60))
		self.win.blit(speedometer, (xoffset + 190, yoffset + HEIGHT + 50))
		self.win.blit(car_img, (xoffset + 375, yoffset + HEIGHT + 50))
		
		
		coin_score = font.render(f' {score}', True, (255, 0, 0))
		self.win.blit(coin_score, (xoffset + 100, yoffset + HEIGHT + 60))
		
		speed_val = font.render(f' {speed}', True, (255, 0, 0))
		self.win.blit(speed_val, (xoffset + 285, yoffset + HEIGHT + 60))
			
		car_dodge = font.render(f' {dodges}', True, (255, 0, 0))
		self.win.blit(car_dodge, (xoffset + 510, yoffset + HEIGHT + 60))