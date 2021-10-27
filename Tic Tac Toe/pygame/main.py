# Tic Tac Toe

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 28 October, 2021

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
ORANGE = (255, 165, 0)

# Rect class

rect_list = []

for i in range(9):
	r = i // 3
	c = i % 3
	x = 20 + 70 * c + 16
	y = 220 + 70 * r + 16
	rect = Rect(x, y, i)
	rect_list.append(rect)

# VARIABLES ******************************************************************

board = ['#'] + [' ' for i in range(9)]

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
	for r in rect_list:
		r.update(win)
		if r.rect.collidepoint(pos):
			r.update(win, BLUE, 5)

		if click_pos:
			if r.rect.collidepoint(click_pos):
				r.active = False
				board[r.index] = 'X'
				print(board)


	pygame.draw.rect(win, ORANGE, (0, 0, WIDTH, HEIGHT), 5)
	clock.tick()
	pygame.display.update()
pygame.quit()