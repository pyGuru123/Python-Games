import pygame
from objects import Tetraminos, Button, draw_grid


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

### Fonts *********************************************************************
pygame.font.init()
score_font = pygame.font.Font('Fonts/Alternity-8w7J.ttf', 30)

### Events ********************************************************************

MOVE_DOWN = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_DOWN, 300)

### loading images ************************************************************

hud = pygame.image.load('Images/hud.jpg')
hud = pygame.transform.scale(hud, (300,80))
hud_rect = hud.get_rect()
hud_rect.x = 0
hud_rect.y = HEIGHT - 80

tetris_img = pygame.image.load('Images/tetris.png')
tetris_img = pygame.transform.scale(tetris_img, (200,120))
tetris_rect = hud.get_rect()
tetris_rect.x = 55
tetris_rect.y = 100

blue_tile = pygame.image.load('Images/b.png')
green_tile = pygame.image.load('Images/g.png')
red_tile = pygame.image.load('Images/r.png')
purple_tile = pygame.image.load('Images/p.png')

TILES = {1:blue_tile, 2:green_tile, 3:red_tile, 4:purple_tile}

### Buttons *******************************************************************
start_img = pygame.image.load('Images/start.png')
play_img = pygame.image.load('Images/play.png')
pause_img = pygame.image.load('Images/pause.png')
replay_img = pygame.image.load('Images/replay.png')
home_img = pygame.image.load('Images/home.png')

start_btn = Button(start_img, (80,40), 110, 260)
play_btn = Button(play_img, (24,24), 150, 430)
pause_btn = Button(pause_img, (24,24), 150, 430)
replay_btn  = Button(replay_img, (24,24), 195, 430)
home_btn  = Button(home_img, (24, 24), 240, 430)

running = True
can_move = False
game_started = False
score = 0
while running:
	win.fill(BLACK)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT and can_move:
				tetris.move_left()
			if event.key == pygame.K_RIGHT and can_move:
				tetris.move_right()
			if event.key == pygame.K_SPACE and can_move:
				tetris.rotate_shape()
			if event.key == pygame.K_p:
				can_move = not can_move

		if event.type == MOVE_DOWN and can_move:
				tetris.move_down()

	if not game_started:
		win.blit(tetris_img, tetris_rect)
		if start_btn.draw(win):
			game_started = True
			can_move = True
			matrix = [[0 for j in range(COLS)] for i in range(ROWS)]
			tetris = Tetraminos(matrix)
			tetris.create_tetramino()
	else:
		pygame.draw.rect(win, WHITE, (0,0, WIDTH, HEIGHT-80), 3)
		win.blit(hud, hud_rect)

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
					pygame.draw.rect(win, WHITE, (x * CELL, y * CELL, CELL, CELL), 1)

		y = ROWS - 1
		while y > 0:
			is_full = True
			for x in range(COLS):
				if matrix[y][x] == 0:
					is_full = False
					y -= 1
					break
			if is_full:
				can_move = False
				score += 10
				for cy in range(ROWS - 1, 0, -1):
					for cx in range(COLS):
						matrix[cy][cx] = matrix[cy-1][cx]
				can_move = True

		if can_move:
			state_btn = pause_btn
		else:
			state_btn = play_btn

		if state_btn.draw(win):
			can_move = not can_move

		if replay_btn.draw(win):
			matrix = [[0 for j in range(COLS)] for i in range(ROWS)]
			tetris = Tetraminos(matrix)
			tetris.create_tetramino()
			score = 0

		if home_btn.draw(win):
			score = 0
			game_started = False
			can_move = False

		img = score_font.render(f'{score}', True, WHITE)
		win.blit(img, (40, 420))

		

	pygame.display.update()
	clock.tick(30)

pygame.quit()