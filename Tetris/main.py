import pygame
import random

pygame.init()
SCREEN = WIDTH, HEIGHT = 380, 500
CELLSIZE = 20
ROWS = HEIGHT // CELLSIZE
COLS = WIDTH // CELLSIZE

# COLORS

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Tetramino:
	# matrix
	# 0   1   2   3
	# 4   5   6   7
	# 8   9   10  11
	# 12  13  14  15

	FIGURES = {
		'I' : [[1, 5, 9, 13], [4, 5, 6, 7]],
        'Z' : [[4, 5, 9, 10], [2, 6, 5, 9]],
        'S' : [[6, 7, 9, 10], [1, 5, 6, 10]],
        'L' : [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        'J' : [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        'T' : [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        'O' : [[1, 2, 5, 6]]
	}

	TYPES = ['I', 'Z', 'S', 'L', 'J', 'T', 'O']

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.type = random.choice(self.TYPES)
		self.shape = self.FIGURES[self.type]
		self.color = random.randint(1, 4)
		self.rotation = 0

	def image(self):
		return self.shape[self.rotation]

	def rotate(self):
		self.rotation = (self.rotation + 1) % len(self.figure)

class Tetris:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.score = 0
		self.board = [[0 for j in range(cols)] for i in range(rows)]
		self.next = None

	def new_figure(self):
		if not self.next:
			self.next = Tetramino(5, 0)
		self.figure = self.next
		self.next = Tetramino(5, 0)

	def intersects(self):
		intersection = False
		for i in range(4):
			for j in range(4):
				if i * 4 + j in self.figure.image():
					if i + self.figure.y > self.rows - 1 or \
					if j + self.figure.x > self.cols - 1 or \
					if j + self.figure.x < 0 or \
					if self.board[i + self.figure.y][j + self.figure.x] > 0:
						intersection = True
		return intersection

	def remove_line(self):
		for y in range(self.rows, 0, -1):
			is_full = True
			for x in range(0, self.cols):
				if self.board[y][x] == 0:
					is_full = False
			if is_full:
				del self.board[y]
				self.board.insert(0, [0 for i in range(self.cols)])
				self.score += 1

	def freeze(self):
		for i in range(4):
			for j in range(4):
				if i * 4 + j in self.figure.image():
					self.board[i + self.figure.y][j + self.figure.x] = self.figure.color
		self.remove_line()
		self.new_figure()
		if self.intersects():
			pass 

	def go_space(self):
		while not self.intersects():
			self.figure.y += 1
		self.figure.y -= 1
		self.freeze()

	def go_down(self):
		self.figure.y += 1
		if self.intersects():
			self.figure.y -= 1
			self.freeze()

	def go_side(self, dx):
		self.figure.x += dx
		if self.intersects():
			self.figure.x -=  dx
			self.freeze()

	def rotate(self):
		rotation = self.figure.rotation
		self.figure.rotate()
		if self.intersects():
			self.figure.rotation = rotation

		
# t = Tetramino(1, 2)
# print(t.image())