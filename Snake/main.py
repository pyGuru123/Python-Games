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

def drawGrid():
	for row in range(ROWS):
		pygame.draw.line(win, WHITE, (0, row*CELLSIZE), (WIDTH, row*CELLSIZE), 1)
	for col in range(COLS):
		pygame.draw.line(win, WHITE, (col*CELLSIZE, 0), (col*CELLSIZE, HEIGHT))


class Snake:
	def __init__(self):
		self.length = 1
		self.direction = None
		self.x = COLS // 2
		self.y = ROWS // 2
		self.head = (COLS//2 * CELLSIZE, ROWS//2 * CELLSIZE)
		self.body = [self.head]

	def update(self):
		head = self.body[-1]
		if self.direction == 'up':
			head = (head[0], head[1] - CELLSIZE)
		elif self.direction == 'down':
			head = (head[0], head[1] + CELLSIZE)
		elif self.direction == 'left':
			head = (head[0] - CELLSIZE, head[1])
		elif self.direction == 'right':
			head = (head[0] + CELLSIZE, head[1])

		self.head = head
		self.body.append(self.head)
		if self.length < len(self.body):
			self.body.pop(0)

	def eatFood(self):
		self.length += 1

	def checkFood(self, food):
		if self.head[0] == food.x and self.head[1] == food.y:
			self.eatFood()
			food.respawn()

	def draw(self):
		for block in self.body:
			x, y = block
			pygame.draw.rect(win, GREEN, (x, y, CELLSIZE, CELLSIZE))

class Food:
	def __init__(self):
		self.image = pygame.image.load('apple.png')
		self.respawn()

	def respawn(self):
		self.x = random.randint(0,COLS-1) * CELLSIZE
		self.y = random.randint(0,ROWS-1) * CELLSIZE
		print(self.x, self.y)

	def draw(self):
		win.blit(self.image, (self.x, self.y))

snake = Snake()
food = Food()

running = True
while running:
	win.fill(BLACK)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False

			if event.key == pygame.K_RIGHT and snake.direction != 'left':
				snake.direction = 'right'

			if event.key == pygame.K_LEFT and snake.direction != 'right':
				snake.direction = 'left'

			if event.key == pygame.K_UP and snake.direction != 'down':
				snake.direction = 'up'

			if event.key == pygame.K_DOWN and snake.direction != 'up':
				snake.direction = 'down'

	drawGrid()
	snake.update()
	snake.checkFood(food)
	snake.draw()
	food.draw()

	clock.tick(FPS)
	pygame.display.update()
pygame.quit()