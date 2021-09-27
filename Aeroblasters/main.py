# Aeroblasters

import pygame
from objects import Background, Player, Enemy

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 60

# COLORS **********************************************************************

WHITE = (255, 255, 255)
BLUE = (30, 144,255)

# Loading Images

bg = Background(win)
p = Player(144, HEIGHT - 100)
e = Enemy(144, 100, 6)

moving_left = False
moving_right = False

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				moving_left = True
			if event.key == pygame.K_RIGHT:
				moving_right = True

		if event.type == pygame.MOUSEBUTTONDOWN:
			x = event.pos[0]
			if x <= WIDTH // 2:
				moving_left = True
			if x >= WIDTH // 2:
				moving_right = True

		if event.type == pygame.KEYUP:
			moving_left = False
			moving_right = False

		if event.type == pygame.MOUSEBUTTONUP:
			moving_left = False
			moving_right = False

	bg.update(3)

	p.update(moving_left, moving_right)
	p.draw(win)
	e.update()
	e.draw(win)

	pygame.draw.rect(win, WHITE, (0,0, WIDTH, HEIGHT), 5, border_radius=4)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()