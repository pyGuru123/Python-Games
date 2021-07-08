import pygame
import pickle
from pygame.locals import *

# SETUP *****************************************

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
win = pygame.display.set_mode(SCREEN, pygame.SCALED | pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 45

t = 16
ROWS, COLS = HEIGHT // 16, WIDTH // 16

t_list = []
for i in (7,8,24,15,16):
	tile = pygame.image.load(f"tiles/{i}.png")
	tile = pygame.transform.rotate(tile, -90)
	t_list.append(tile)


running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			
	for c in range(COLS):
		for r in range(ROWS):
			if c in (0,1,2,3,4,5):
				win.blit(t_list[2], (c*t, r * t))
			if c == 6:
				win.blit(t_list[4], (c*t, r*t))
			if c in (7,8,9,10):
				win.blit(t_list[1], (c*t, r*t))
			if c == 11:
				win.blit(t_list[3], (c*t, r*t))
			if c in (12,13,14,15,16,17):
				win.blit(t_list[0], (c*t, r*t))
				
	pygame.image.save(win, "bg.png")
				
	clock.tick(FPS)
	pygame.display.update()
			
pygame.quit()