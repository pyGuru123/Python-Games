import math
import pygame

SCREEN = WIDTH, HEIGHT = 400, 400
CELLSIZE = 20
PADDING = 20
ROWS = COLS = (WIDTH - 2 * PADDING) // CELLSIZE
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Cell:
	def __init__(self, r, c):
		self.r = r
		self.c = c
		self.rect = pygame.Rect((self.c*CELLSIZE + PADDING, self.r*CELLSIZE + 
								PADDING, CELLSIZE, CELLSIZE))
		self.left = self.rect.left
		self.top = self.rect.top
		self.right = self.rect.right
		self.bottom = self.rect.bottom
		self.edges = [
					  [(self.left, self.top), (self.right, self.top)],
					  [(self.right, self.top), (self.right, self.bottom)],
					  [(self.right, self.bottom), (self.left, self.bottom)],
					  [(self.left, self.bottom), (self.left, self.top)]
					 ]
		self.sides = [False, False, False, False]
		self.winner = None

	def update(self, win):
		for index, side in enumerate(self.sides):
			if side:
				pygame.draw.line(win, WHITE, (self.edges[index][0]),
										(self.edges[index][1]), 1)

def distance(A, B):
	return math.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)

cells = []
for r in range(ROWS):
	for c in range(COLS):
		cell = Cell(r, c)
		cells.append(cell)

pos = None
up = False
right = False
bottom = False
left = False

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = event.pos
			print(pos)

		if event.type == pygame.MOUSEBUTTONUP:
			pos = None

	for r in range(ROWS+1):
		for c in range(COLS+1):
			pygame.draw.circle(win, WHITE, (c*CELLSIZE + PADDING, r*CELLSIZE + 
								PADDING), 2)
	for cell in cells:
		cell.update(win)
		if pos:
			if cell.rect.collidepoint(pos):
				pygame.draw.rect(win,BLUE,cell.rect, 1)

	pygame.display.update()

pygame.quit()