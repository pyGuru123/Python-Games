import pygame
from objects import Tetraminos, draw_grid


### GAME Setup ****************************************************************
pygame.init()
SCREEN = WIDTH, HEIGHT = 300, 480
win = pygame.display.set_mode(SCREEN)
pygame.display.set_caption('Tetris')

clock = pygame.time.Clock()

CELL = 20
ROWS, COLS = (HEIGHT - 80) // CELL, WIDTH // CELL

### colors  *******************************************************************
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

### Events ********************************************************************

MOVE_DOWN = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_DOWN, 300)

### loading images ************************************************************

hud = pygame.image.load('Images/hud.jpg')
hud = pygame.transform.scale(hud, (300,80))
hud_rect = hud.get_rect()
hud_rect.x = 0
hud_rect.y = HEIGHT - 80

blue_tile = pygame.image.load('Images/b.png')
green_tile = pygame.image.load('Images/g.png')
red_tile = pygame.image.load('Images/r.png')
purple_tile = pygame.image.load('Images/p.png')

TILES = {1:blue_tile, 2:green_tile, 3:red_tile, 4:purple_tile}

### Objects *******************************************************************
matrix = [[0 for j in range(COLS)] for i in range(ROWS)]
tetris = Tetraminos(matrix)
tetris.create_tetramino()

running = True
while running:
	win.fill(BLACK)
	pygame.draw.rect(win, WHITE, (0,0, WIDTH, HEIGHT-80), 3)
	win.blit(hud, hud_rect)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				tetris.move_left()
			if event.key == pygame.K_RIGHT:
				tetris.move_right()
			if event.key == pygame.K_SPACE:
				tetris.rotate_shape()

		if event.type == MOVE_DOWN:
				tetris.move_down()

	if tetris.on_tetris:
		tetris = Tetraminos(matrix)
		tetris.draw_grid()

	for y in range(ROWS):
		for x in range(COLS):
			cell = matrix[y][x]
			if cell != 0:
				tile = TILES[cell]
				rect = tile.get_rect()
				rect.x = x * CELL
				rect.y = y * CELL
				win.blit(tile, rect)
				# pygame.draw.rect(win, COLORS[cell], (x * CELL, y * CELL, CELL, CELL))
				pygame.draw.rect(win, WHITE, (x * CELL, y * CELL, CELL, CELL), 1)


	pygame.display.update()
	clock.tick(30)

pygame.quit()