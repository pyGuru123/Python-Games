# Tic Tac Toe

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 28 October, 2021

import random
import pygame
from objects import Rect
from logic import isBoardFull, check_win

pygame.init()
SCREEN = WIDTH, HEIGHT = (288, 512)

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 60

# COLORS *********************************************************************

WHITE = (225,225,225)
BLACK = (0, 0, 0)
GRAY = (32, 33, 36)
BLUE = (0, 90, 156)
ORANGE = (208, 91, 3)
YELLOW = (255,255,0)

# Rect class *****************************************************************

box_list = []

for i in range(9):
	r = i // 3
	c = i % 3
	x = 20 + 70 * c + 16
	y = 220 + 70 * r + 16
	box = Rect(x, y, i)
	box_list.append(box)

# BOARD **********************************************************************

board = ['#'] + [' ' for i in range(9)]
players = ['X', 'O']
current_player = random.randint(0, 1)
text = players[current_player]

# FONTS **********************************************************************

scoreX = '-'
scoreO = '-'

font1 = pygame.font.Font('Fonts/PAPYRUS.ttf', 17)
font2 = pygame.font.Font('Fonts/CHILLER.ttf', 30)
imgX = font1.render(f'X    {scoreX}', True, WHITE)
imgO = font1.render(f'O    {scoreO}', True, WHITE)

tic_tac_toe = font2.render('Tic Tac Toe', True, WHITE)

# VARIABLES ******************************************************************

result = None
line_pos = None

running = True
while running:
	click_pos = None
	win.fill(GRAY)

	pygame.draw.rect(win, BLUE, (10, 10, WIDTH-20, 50), border_radius=20)
	pygame.draw.rect(win, WHITE, (10, 10, WIDTH-20, 50), 2, border_radius=20)
	win.blit(tic_tac_toe, (WIDTH//2-tic_tac_toe.get_width()//2,17))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			click_pos = event.pos

	for box in box_list:
		box.update(win)
		if box.active and click_pos:
			if box.rect.collidepoint(click_pos):
				box.active = False
				
				box.text = text
				if text == 'X':
					box.bgcolor = BLUE
				else:
					box.bgcolor = ORANGE

				board[box.index+1] = text
				current_player = (current_player + 1) % 2
				text = players[current_player]

	check_winner = check_win(board, "X")
	if check_winner[0]:
		result = 'X Won'
		line_pos = check_winner[1]
	check_winner = check_win(board, "O")
	if check_winner[0]:
		result = 'O Won'
		line_pos = check_winner[1]
	if line_pos:
		starting = box_list[int(line_pos[0]) - 1].rect.center
		ending = box_list[int(line_pos[-1]) - 1].rect.center

		pygame.draw.line(win, WHITE, starting, ending, 5)

	if result:
		if box_list[-1].rect.bottom <= 500:
			for box in box_list:
				box.rect.y += 1

	if isBoardFull(board) or result:
		for box in box_list:
			box.active = False

	if text == 'X':
		pygame.draw.rect(win, BLUE, (35, 150, 80, 30), border_radius=10)
	elif text == 'O':
		pygame.draw.rect(win, ORANGE, (165, 150, 80, 30), border_radius=10)

	win.blit(imgX, (60, 152))
	win.blit(imgO, (180, 152))
	pygame.draw.rect(win, WHITE, (35, 150, 80, 30), 1, border_radius=10)
	pygame.draw.rect(win, WHITE, (165, 150, 80, 30), 1, border_radius=10)

	pygame.draw.rect(win, BLACK, (0, 0, WIDTH, HEIGHT), 5, border_radius=10)
	clock.tick()
	pygame.display.update()
pygame.quit()