import random
import pygame
from objects import Player

pygame.init()
SCREEN = WIDTH, HEIGHT = 1024, 636
win = pygame.display.set_mode(SCREEN)
pygame.display.set_caption('Snake & Ladder')

clock = pygame.time.Clock()
FPS = 30

### LOADING IMAGES ************************************************************
bg_img = pygame.image.load('Assets/bg1.jpg')
bg_img = pygame.transform.scale(bg_img, SCREEN)

board_img = pygame.image.load('Assets/board1.jpg')
board_img = pygame.transform.scale(board_img, (612, 612))

p = Player(1)

steps_to_move = 0
dice_result = None
first_move_time = None
second_move_time = None

running = True
while running:
	win.blit(bg_img, (0,0))
	# win.fill((0,0,0))
	win.blit(board_img, (370,12))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				steps = random.choices(population=range(1,7), 
									   weights=[0.18,0.18,0.18,0.18,0.18,0.10],
									   k = 1)
				dice_result = steps[0]
				print(dice_result)
				first_move_time = pygame.time.get_ticks()
				steps_to_move = p.move(dice_result)

	if steps_to_move:
		second_move_time = pygame.time.get_ticks()
		delta = second_move_time - first_move_time
		if delta >= 300:
			steps_to_move = p.move(steps_to_move)
			first_move_time = pygame.time.get_ticks()
	elif (not steps_to_move) and dice_result:
		p.first_move = True
		first_move_time = None
		second_move_time = None

	win.blit(p.image, p.rect)
	
	pygame.display.update()
	clock.tick(FPS)

pygame.quit()