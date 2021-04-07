import os
import pygame
from objects import Board

### SETUP *********************************************************************
pygame.init()
SCREEN = WIDTH, HEIGHT = 740, 520
win = pygame.display.set_mode(SCREEN)
pygame.display.set_caption('Memory Puzzle')

clock = pygame.time.Clock()
FPS = 30

ROWS, COLS = 8, 10
TILESIZE = 50

### COLORS ********************************************************************
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 25, 25)
WHITE = (255, 255, 255)

### LOADING IMAGES ************************************************************
img_list = []
for img in os.listdir('Assets/icons/'):
	image = pygame.image.load('Assets/icons/' + img)
	image = pygame.transform.scale(image, (TILESIZE,TILESIZE))
	img_list.append(image)

bg = pygame.image.load('Assets/bg.jpg')

### CREATING BOARD ************************************************************
board = Board(img_list)


### GAME VARIABLES ************************************************************
first_card = None
second_card = None
first_click_time = None
second_click_time = None

running = True
while running:
	win.blit(bg, (0,0))
	clicked = False

	x, y = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				clicked = True
				x, y = pygame.mouse.get_pos()

	### Polling time to hide cards
	if second_click_time:
		current_time = pygame.time.get_ticks()

		delta = current_time - second_click_time
		if delta >= 1000:
			if first_card.value == second_card.value:
				first_card.is_alive = False
				second_card.is_alive = False

			index = first_card.index
			fcard = board.board[index[0]][index[1]]
			fcard.animate = True
			fcard.slide_left = False
			first_card = None

			index = second_card.index
			scard = board.board[index[0]][index[1]]
			scard.animate = True
			scard.slide_left = False
			second_card = None

			first_click_time = None
			second_click_time = None
		else:
			clicked = False

	### Displaying cards
	for r in range(ROWS):
		for c in range(COLS):
			border = False
			card = board.board[r][c]
			if card.is_alive:
				xcord = card.rect.x
				ycord = card.rect.y

				if card.rect.collidepoint((x,y)):
					border = True
					if clicked:
						card.visible = True
						card.animate = True
						card.slide_left = True

						if not first_card:
							first_card = card
						else:
							second_card = card
							if second_card != first_card:
								second_click_time = pygame.time.get_ticks()
							else:
								second_card = None

				pygame.draw.rect(win, BLACK, (xcord+5, ycord+5,TILESIZE, TILESIZE))

				if not card.animate:
					if card.visible:
						win.blit(card.image, card.rect)
					else:
						pygame.draw.rect(win, WHITE, (xcord, ycord,TILESIZE, TILESIZE))

					if border:
						pygame.draw.rect(win, RED, (xcord, ycord,TILESIZE, TILESIZE), 2)
				else:
					card.on_click(win)

	pygame.display.flip()
	clock.tick(FPS)

pygame.quit()