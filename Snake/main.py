# Snake


import random
import pygame

pygame.init()
SCREEN = WIDTH, HEIGHT =  288, 512
CELLSIZE = 16
ROWS = HEIGHT // CELLSIZE
COLS = WIDTH // CELLSIZE
win = pygame.display.set_mode(SCREEN)

FPS = 15
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

apple = pygame.image.load('apple.png')

def drawGrid():
	for row in range(ROWS):
		pygame.draw.line(win, WHITE, (0, row*CELLSIZE), (WIDTH, row*CELLSIZE), 1)
	for col in range(COLS):
		pygame.draw.line(win, WHITE, (col*CELLSIZE, 0), (col*CELLSIZE, HEIGHT))

def randomApple():
	return random.randint(0,ROWS-1), random.randint(0,COLS-1)

dx = dy = 0

class Snake:
	def __init__(self):
		self.length = 0
		self.direction = UP
		self.body = 20
		self.x = WIDTH // 2
		self.y = HEIGHT // 2

	def update(self):
		self.x += dx
		self.y += dy

	def draw(self):
		pygame.draw.rect(win, GREEN, self.x, self.y, self.body, self.body)

ay, ax = randomApple()
snake = Snake()

running = True
while running:
	win.fill(BLACK)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False

			if event.key == pygame.K_RIGHT:
				dx = CELLSIZE
				dy = 0

			if event.key == pygame.K_LEFT:
				dx = -CELLSIZE
				dy = 0

			if event.key == pygame.K_UP:
				dx = 0
				dy = -CELLSIZE

			if event.key == pygame.K_DOWN:
				dx = 0
				dy = CELLSIZE

	# drawGrid()
	x += dx
	y += dy
	win.blit(apple, (ax*CELLSIZE, ay*CELLSIZE))
	snake.update()
	snake.draw()

	clock.tick(FPS)
	pygame.display.update()
pygame.quit()