# Tic Tac Toe

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 28 October, 2021

import random
import pygame
from objects import Rect

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

# Rect class

box_list = []

for i in range(9):
	r = i // 3
	c = i % 3
	x = 20 + 70 * c + 16
	y = 220 + 70 * r + 16
	box = Rect(x, y, i)
	box_list.append(box)

# VARIABLES ******************************************************************

board = [' ' for i in range(9)]
players = ['X', 'O']
current_player = random.randint(0, 1)

running = True
while running:
	click_pos = None
	win.fill(GRAY)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			click_pos = event.pos

	pos = pygame.mouse.get_pos()
	for box in box_list:
		box.update(win)
		if box.active and click_pos:
			if box.rect.collidepoint(click_pos):
				box.active = False
				text = players[current_player]
				
				box.text = text
				if text == 'X':
					box.bgcolor = BLUE
				else:
					box.bgcolor = ORANGE

				board[box.index] = text
				current_player = (current_player + 1) % 2


	pygame.draw.rect(win, BLACK, (0, 0, WIDTH, HEIGHT), 5)
	clock.tick()
	pygame.display.update()
pygame.quit()