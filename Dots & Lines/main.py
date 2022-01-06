import math
import pygame

SCREEN = WIDTH, HEIGHT = 100, 100
CELLSIZE = 20
PADDING = 20
ROWS = COLS = (WIDTH - 3 * PADDING) // CELLSIZE
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

font = pygame.font.SysFont('cursive', 25)

class Cell:
	def __init__(self, r, c):
		self.r = r
		self.c = c
		self.index = self.r * ROWS + self.c

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

	def checkwin(self, winner):
		if not self.winner:
			if self.sides == [True]*4:
				self.winner = winner
				if winner == 'X':
					color = GREEN
				else:
					color = RED
				self.text = font.render(self.winner, True, color)

				return 1
		return 0

	def update(self, win):
		for index, side in enumerate(self.sides):
			if side:
				pygame.draw.line(win, WHITE, (self.edges[index][0]),
										(self.edges[index][1]), 2)

		if self.winner:
			win.blit(self.text, (self.rect.centerx-5, self.rect.centery-7))

cells = []
for r in range(ROWS):
	for c in range(COLS):
		cell = Cell(r, c)
		cells.append(cell)

pos = None
ccell = None
up = False
right = False
bottom = False
left = False

fillcount = 0
p1_score = 0
p2_score = 0
gameover = False

turn = 0
players = ['X', 'O']
player = players[turn]

running = True
while running:
	win.fill((0,0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = event.pos

		if event.type == pygame.MOUSEBUTTONUP:
			pos = None

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				up = True
			if event.key == pygame.K_RIGHT:
				right = True
			if event.key == pygame.K_DOWN:
				bottom = True
			if event.key == pygame.K_LEFT:
				left = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				up = False
			if event.key == pygame.K_RIGHT:
				right = False
			if event.key == pygame.K_DOWN:
				bottom = False
			if event.key == pygame.K_LEFT:
				left = False

			turn = (turn + 1) % len(players)
			player = players[turn]

	for r in range(ROWS+1):
		for c in range(COLS+1):
			pygame.draw.circle(win, WHITE, (c*CELLSIZE + PADDING, r*CELLSIZE + 
								PADDING), 2)
	for cell in cells:
		cell.update(win)
		if pos and cell.rect.collidepoint(pos):
			ccell = cell

	if ccell:
		index = ccell.index
		if up:
			ccell.sides[0] = True
			if index - ROWS >= 0:			
				cells[index-ROWS].sides[2] = True
		if right:
			ccell.sides[1] = True
			if (index + 1) % COLS > 0:
				cells[index+1].sides[3] = True
		if bottom:
			ccell.sides[2] = True
			if index + ROWS < len(cells):			
				cells[index+ROWS].sides[0] = True
		if left:
			ccell.sides[3] = True
			if (index % COLS) > 0:
				cells[index-1].sides[1] = True
		
		res = ccell.checkwin(player)
		if res:
			fillcount += res
			if player == 'X':
				p1_score += 1
			else:
				p2_score += 1
			if fillcount == ROWS * COLS:
				print(p1_score, p2_score)
				running = False

	pygame.display.update()

pygame.quit()