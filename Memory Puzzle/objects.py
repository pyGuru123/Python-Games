import random
import pygame

SCREEN = WIDTH, HEIGHT = 640, 520
ROWS, COLS = 8, 10
TILESIZE = 45

class Board:
	def __init__(self, imglist):
		self.image_list = imglist
		self.extended_imglist = 4 * [i for i in range(1, len(self.image_list) + 1)]

		self.board = None
		self.info_board = self.info_cards()

	def randomize_images(self):
		board = [[0 for j in range(COLS)] for i in range(ROWS)]
		for i in range(10):
			random.shuffle(self.extended_imglist)

		for r in range(ROWS):
			for c in range(COLS):
				index = r * COLS + c
				value = self.extended_imglist[index]
				image = self.image_list[value-1]
				x = c*TILESIZE + c * 10 + 20
				y = r*TILESIZE + r * 10 + 20
				card = Card(value, (r,c), image, (x, y))
				board[r][c] = card

		self.board = board

	def info_cards(self):
		board = [[0 for i in range(10)] for j in range(2)]

		for r in range(2):
			for c in range(COLS):
				value = r * COLS + c + 1
				image = self.image_list[value-1]
				x = c*TILESIZE + c * 10 + 20
				y = r*TILESIZE + r * 10 + 20
				card = InfoCard(value, (r,c), image, (x, y))
				board[r][c] = card

		return board

class Card:
	def __init__(self, value, index, image, pos):
		self.value = value
		self.index = index
		self.image = image
		self.pos = pos

		self.is_alive = True
		self.visible = False
		self.animate = False
		self.slide_left = True
		self.animation_complete = False

		self.rect = self.image.get_rect()
		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]

		self.cover_x = TILESIZE

	def on_click(self, win, speed=None):
		if self.visible:
			if self.slide_left:
				self.animation_complete = False
				if self.cover_x > 0:
					self.cover_x -= speed
				if self.cover_x <= 0:
					self.animate = False
			else:
				if self.cover_x < TILESIZE:
					self.cover_x += speed
				if self.cover_x >= TILESIZE:
					self.animate = False
					self.visible = False
					self.slide_left = False
					self.animation_complete = True

			win.blit(self.image, self.rect)
			rect =  (self.rect.x, self.rect.y, self.cover_x, TILESIZE)
			pygame.draw.rect(win, (255, 255, 255), rect)

class InfoCard:
	def __init__(self, value, index, image, pos):
		self.value = value
		self.index = index
		self.image = image
		self.pos = pos

		self.rect = self.image.get_rect()
		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]

class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()

		self.image = pygame.transform.scale(img, scale)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

	def draw(self, win, image=None):
		if image:
			self.image = image
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

def message_box(win, font, name, text):
	WIDTH = 540
	HEIGHT = 300
	x = 35
	y = 185 # depends on message box location
	pygame.draw.rect(win, (255,255,255), (25, 150, WIDTH, HEIGHT), border_radius=10)
	for word in text.split(' '):
		rendered = font.render(word, 0, (0,0,0))
		width = rendered.get_width()
		if x + width >= WIDTH:
			x = 35
			y += 25
		win.blit(rendered, (x, y))
		x += width + 5


	title = font.render(name, 0, (0,0,0))
	title_width = 120
	pygame.draw.rect(win, (255,255,255), (WIDTH // 2 - title_width // 2 + 10, 140, 
					title_width, 30), border_radius=10)
	win.blit(title, (WIDTH // 2 - title.get_width()//2 + 10, 145))