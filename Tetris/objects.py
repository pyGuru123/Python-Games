import pygame
import random
from pprint import pprint

SCREEN = WIDTH, HEIGHT = 300, 500
CELL = 20
ROWS, COLS = (HEIGHT - 100) // CELL, WIDTH // CELL

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Tetraminos:
	def __init__(self, matrix):
		self.matrix = matrix

		O = [[1,1],
			 [1,1]]

		I = [[1],
			 [1],
			 [1],
			 [1]]

		J = [[0,1],
			 [0,1],
			 [1,1]]

		L = [[1,0],
			 [1,0],
			 [1,1]]

		S = [[0,1,1],
			 [1,1,0]]

		T = [[1,1,1],
			 [0,1,0]]

		Z = [[1,1,0],
			 [0,1,1]]

		self.shape = random.choice([O,I,J,L,S,T,Z])
		self.width = len(self.shape[0])
		self.height = len(self.shape)
		self.x = random.randint(0,COLS-self.width)
		self.y = 0
		self.color = random.randint(1,7)

	def create_tetramino(self):
		self.draw_grid()

	def move_left(self):
		move_left = False
		if self.x > 0:
			for y in range(self.height):
				if self.matrix[self.y + y][self.x - 1] != 0:
					break
			else:
				move_left = True

		if move_left:
			self.erase_grid()
			self.x -= 1
			self.draw_grid()

	def move_right(self):
		move_right = False
		if self.x < COLS - self.width:
			for y in range(self.height):
				if self.matrix[self.y + y][self.x + self.width] != 0:
					break
			else:
				move_right = True

		if move_right:
			self.erase_grid()
			self.x += 1
			self.draw_grid()

	def move_down(self):
		if self.can_move_down():
			self.erase_grid()
			self.y += 1
			self.draw_grid()

	def can_move_down(self):
		move_down = False
		for i in range(self.width):
			r, c = self.y+self.height, self.x + i
			# if self.shape[self.height-1][i] == 1:
			if self.matrix[r][c] != 0:
				break
		else:
			move_down = True

		return move_down

	def draw_grid(self):
		for y in range(self.height):
			for x in range(self.width):
				r, c = self.y+y, self.x+x
				if self.shape[y][x] == 1:
					self.matrix[r][c] = self.color

		# pprint(self.matrix)

	def erase_grid(self):
		for y in range(self.height):
			for x in range(self.width):
				r, c = self.y + y, self.x + x
				if self.shape[y][x] == 1:
					self.matrix[r][c] = 0

def draw_grid(win):
		for i in range(ROWS + 1):
			pygame.draw.line(win, WHITE, (0, CELL * i), (WIDTH, CELL * i))
		for i in range(COLS):
			pygame.draw.line(win, WHITE, (CELL * i, 0), (CELL * i, HEIGHT - 100))