import pygame
from pygame.locals import QUIT, KEYDOWN, K_SPACE

from objects import Dino, Cactus, Cloud

### SETUP *********************************************************************
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 700, 420

pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dino')

bg = pygame.image.load('assets/bg1.jpg').convert()
bgX = 0
bgX2 = bg.get_width()

### Objects & Events **********************************************************
ADDCACTUS = pygame.USEREVENT + 1
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCACTUS, 5000)
pygame.time.set_timer(ADDCLOUD, 8000)

cactus_sprites = pygame.sprite.Group()
cloud_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

dino = Dino()
dinos = pygame.sprite.Group(dino)

running = True
gameUpdating = True
while running:
	collision = 0

	win.blit(bg,(bgX,0))
	win.blit(bg,(bgX2,0))

	if gameUpdating:
		bgX -= 1.8
		bgX2 -= 1.8
		if bgX < bg.get_width() * -1:
			bgX = bg.get_width()
		if bgX2 < bg.get_width() * -1:
			bgX2 = bg.get_width()


	for event in pygame.event.get():
		if event.type == QUIT:
			running = False

		if event.type == ADDCACTUS:
			c = Cactus()
			cactus_sprites.add(c)
			all_sprites.add(c)
		if event.type == ADDCLOUD:
			c = Cloud()
			cloud_sprites.add(c)
			all_sprites.add(c)

	pressed_keys = pygame.key.get_pressed()
	dinos.update(pressed_keys)

	if gameUpdating:
		cactus_sprites.update()
		cloud_sprites.update()

	for entity in all_sprites:
		win.blit(entity.surf, entity.rect)
		pygame.draw.rect(win, (255,0,0), entity.rect, 2)
	dinos.draw(win)

	for entity in cactus_sprites:
		collision = dino.is_collided_with(entity)
		if collision:
			dino.is_dead()
			gameUpdating = False



	pygame.display.flip()
	clock.tick(30)

pygame.quit()