import random
import pygame

SCREEN = WIDTH, HEIGHT = 640, 520
ROWS, COLS = 8, 10
TILESIZE = 50

class Board:
	def __init__(self, imglist):
		self.image_list = imglist
		self.extended_imglist = 4 * [i for i in range(1, len(self.image_list) + 1)]
		
		self.board = self.randomize_images()

	def randomize_images(self):
		board = [[0 for j in range(COLS)] for i in range(ROWS)]
		for i in range(10):
			random.shuffle(self.extended_imglist)

		for r in range(ROWS):
			for c in range(COLS):
				index = r * ROWS + c
				value = self.extended_imglist[index]
				image = self.image_list[value-1]
				x = c*TILESIZE + c * 10 + 20
				y = r*TILESIZE + r * 10 + 20
				card = Card(value, (r,c), image, (x, y))
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

		self.rect = self.image.get_rect()
		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]

		self.cover_x = TILESIZE

	def on_click(self, win):
		if self.visible:
			if self.slide_left:
				if self.cover_x > 0:
					self.cover_x -= 5
				if self.cover_x == 0:
					self.animate = False
			else:
				if self.cover_x < TILESIZE:
					self.cover_x += 5
				if self.cover_x == TILESIZE:
					self.animate = False
					self.visible = False

			win.blit(self.image, self.rect)
			rect =  (self.rect.x, self.rect.y, self.cover_x, TILESIZE)
			pygame.draw.rect(win, (255, 255, 255), rect)