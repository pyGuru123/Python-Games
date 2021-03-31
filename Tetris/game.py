import pygame
from objects import Tetraminos, draw_grid


pygame.init()
SCREEN = WIDTH, HEIGHT = 300, 500
win = pygame.display.set_mode(SCREEN)
pygame.display.set_caption('Tetris')

CELL = 20
ROWS, COLS = (HEIGHT - 100) // CELL, WIDTH // CELL

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
VIOLET = (127, 0, 255)
INDIGO = (75, 0, 130)
BLUE = (0,0,205)
GREEN = (34,139,34)
YELLOW = (255,255,0)
ORANGE = (255,140,0)
RED = (255, 0, 0)

COLORS = {1:VIOLET, 2:INDIGO, 3:BLUE, 4:GREEN, 5:YELLOW, 6:ORANGE, 7:RED}

# tetris
matrix = [[0 for j in range(COLS)] for i in range(ROWS)]
tetris = Tetraminos(matrix)
tetris.create_tetramino()

running = True
while running:
	win.fill(BLACK)
	# draw_grid(win)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				tetris = Tetraminos(matrix)
				tetris.draw_grid()
			if event.key == pygame.K_LEFT:
				tetris.move_left()
			if event.key == pygame.K_RIGHT:
				tetris.move_right()
			if event.key == pygame.K_DOWN:
				tetris.move_down()

	for y in range(ROWS):
		for x in range(COLS):
			cell = matrix[y][x]
			if cell != 0:
				pygame.draw.rect(win, COLORS[cell], (x * CELL, y * CELL, CELL, CELL))

	pygame.display.update()

pygame.quit()