import random
import pygame
from objects import Block

pygame.init()
SCREEN = WIDTH, HEIGHT = 270, 480
win = pygame.display.set_mode(SCREEN)
pygame.display.set_caption('Piano Tiles')

clock = pygame.time.Clock()
FPS = 30

### Loading Images ************************************************************
bg = pygame.image.load('Assets/bg.png')
overlay = pygame.image.load('Assets/red overlay.png').convert_alpha()
# overlay.set_colorkey((125, 125, 125), pygame.RLEACCEL)

### EVENTS ********************************************************************
ADDBLOCK = pygame.USEREVENT + 1
pygame.time.set_timer(ADDBLOCK, 1000)

b = Block(win, (0,0))
block_group = pygame.sprite.Group()

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == ADDBLOCK:
			x_col = random.randint(0,3)
			block = Block(win, (67.5 * x_col, 20))
			block_group.add(block)

	win.blit(bg, (0,0))
	block_group.update()
	win.blit(overlay, (0,0))

	clock.tick(FPS)
	pygame.display.update()

pygame.quit()