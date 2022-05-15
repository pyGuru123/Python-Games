# Snake


import random
import pygame
import pickle

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
CELLSIZE = 16
ROWS = HEIGHT // CELLSIZE
COLS = WIDTH // CELLSIZE

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

FPS = 15
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# LOADING IMAGES *************************************************************

bg = pygame.image.load('Assets/bg.png')

tile_list = []
for i in range(4):
	tile = pygame.image.load(f'Tiles/{i+1}.png')
	tile_list.append(tile)

tile_size = {
	1 : (16, 64),
	2 : (64, 16),
	3 : (32, 32),
	4 : (32, 32)
}

def drawGrid():
	for row in range(ROWS):
		pygame.draw.line(win, WHITE, (0, row*CELLSIZE), (WIDTH, row*CELLSIZE), 1)
	for col in range(COLS):
		pygame.draw.line(win, WHITE, (col*CELLSIZE, 0), (col*CELLSIZE, HEIGHT))

def loadlevel(level):
	file = f'Levels/level{level}_data'
	with open(file, 'rb') as f:
		data = pickle.load(f)
		for y in range(len(data)):
			for x in range(len(data[0])):
				if data[y][x] >= 0:
					data[y][x] += 1
	return data, len(data[0])

class Snake:
	def __init__(self):
		self.length = 1
		self.direction = None
		self.x = COLS // 2
		self.y = ROWS // 2
		self.head = [COLS//2 * CELLSIZE, ROWS//2 * CELLSIZE]
		self.body = [self.head]

	def update(self):
		head = self.body[-1]
		if self.direction == 'up':
			head = [head[0], head[1] - CELLSIZE]
		elif self.direction == 'down':
			head = [head[0], head[1] + CELLSIZE]
		elif self.direction == 'left':
			head = [head[0] - CELLSIZE, head[1]]
		elif self.direction == 'right':
			head = [head[0] + CELLSIZE, head[1]]

		self.head = head
		self.body.append(self.head)
		if self.length < len(self.body):
			self.body.pop(0)

		snake.outOfBound()
		# if snake.tailCollision():
		# 	print(True)

	def eatFood(self):
		self.length += 1

	def outOfBound(self):
		for index, block in enumerate(self.body):
			if block[0] > WIDTH:
				self.body[index][0] = 0
			elif block[0] < 0:
				self.body[index][0] = WIDTH - CELLSIZE
			elif block[1] > HEIGHT:
				self.body[index][1] = 0
			elif block[1] < 0:
				self.body[index][1] = HEIGHT - CELLSIZE

	def checkFood(self, food):
		if self.head[0] == food.x and self.head[1] == food.y:
			self.eatFood()
			food.respawn()

	def tailCollision(self):
		head = self.body[-1]
		has_eaten_tail = False

		for i in range(len(self.body)-2):
			block = self.body[i]
			if head[0] == block[0] or head[1] == block[1]:
				has_eaten_tail = True

		return has_eaten_tail

	def draw(self):
		for block in self.body:
			x, y = block
			color = GREEN
			if block == self.head:
				color = BLUE
			pygame.draw.rect(win, color, (x, y, CELLSIZE, CELLSIZE))

class Food:
	def __init__(self):
		type_ = random.randint(1, 3)
		self.image = self.temp = pygame.image.load(f'Assets/{type_}.png')
		self.size = 16
		self.ds = 1
		self.counter = 0
		self.respawn()

	def respawn(self):
		self.x = random.randint(0,COLS-1) * CELLSIZE
		self.y = random.randint(0,ROWS-1) * CELLSIZE

	def update(self):
		self.counter += 1
		if self.counter % 3 == 0:
			self.size += self.ds
			if self.size < 15 or self.size > 17:
				self.ds *= -1

			self.temp = pygame.transform.scale(self.image, (self.size, self.size))

	def draw(self):
		win.blit(self.temp, (self.x, self.y))

snake = Snake()
food = Food()
leveldata, length = loadlevel(1)


running = True
while running:
	win.fill(BLACK)
	for i in range(5):
		win.blit(bg, (0, 104 * i))
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

	# drawGrid()
	# draw level
	for y in range(ROWS):
		for x in range(COLS):
			if leveldata[y][x] > 0:
				tile = leveldata[y][x]
				pos = (x*CELLSIZE, y*CELLSIZE)
				win.blit(tile_list[tile-1], pos)

				if (pos[0] <= snake.head[0] <= pos[0] + tile_size[tile][0] and 
					pos[1] <= snake.head[1] <= pos[1] + tile_size[tile][1]):
					pass
	
	snake.update()
	snake.checkFood(food)
	snake.draw()
	food.update()
	food.draw() 

	clock.tick(FPS)
	pygame.display.update()
pygame.quit()