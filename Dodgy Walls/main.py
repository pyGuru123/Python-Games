# Risky Walls

# Author : Prajjwal Pathak (pyguru)
# Date : Tuesday, 13 July, 2021

import pygame
import random

from objects import Bar, Dot, Player, Message

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
pygame.display.set_caption('Risky Walls')

clock = pygame.time.Clock()
FPS = 30

bg = pygame.image.load(f'Assets/bg4.jpg')
bg = pygame.transform.scale(bg, SCREEN)

frame_height = 150
frame = pygame.image.load(f'Assets/bg3.jpg')
frame = pygame.transform.scale(frame, (WIDTH - 10, frame_height))
frameX, frameY = 5, HEIGHT//2 - frame_height//2

# COLORS **********************************************************************

BLACK = (0, 0, 32)
WHITE = (255, 255, 255)

# FONTS ***********************************************************************


# Messages

score_font = "Fonts/EvilEmpire-4BBVK.ttf"


# GROUPS **********************************************************************

bar_group = pygame.sprite.Group()
dot_group = pygame.sprite.Group()

p = Player(win)

# VARIABLES *******************************************************************

bar_frequency = 1200
bar_heights = [height for height in range(60,100,10)]
pos = -1
pos_updater = 1
start_time = pygame.time.get_ticks()

clicked = False
score = 0

running = True
while running:
	clicked = False
	win.blit(bg, (0,0))
	win.blit(frame, (frameX, frameY))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			if not clicked:
				clicked = True
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False

	current_time = pygame.time.get_ticks()
	if current_time - start_time >= bar_frequency:
		bar_height = random.choice(bar_heights)
		pos = pos * -1

		if pos == -1:
			bar_y = frameY
			dot_y = frameY + bar_height + 20
		elif pos == 1:
			bar_y = frameY + frame_height - bar_height
			dot_y = frameY + frame_height - bar_height - 20

		bar = Bar(WIDTH, bar_y, bar_height, BLACK, win)
		dot = Dot(WIDTH + 10, dot_y, win)
		bar_group.add(bar)
		dot_group.add(dot)

		start_time = current_time

	bar_group.update(3)
	dot_group.update(3)
	p.update(clicked)
	pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 5, border_radius=10)

	for dot in dot_group:
		if dot.rect.colliderect(p):
			dot.kill()
			score += 1

	score_msg = Message(WIDTH//2, 100, 50, f"{score}", score_font, WHITE, win)
	score_msg.update()

	clock.tick(FPS)
	pygame.display.update()

pygame.quit()