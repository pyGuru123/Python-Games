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

FPS = 10
clock = pygame.time.Clock()

# COLORS *********************************************************************

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# LOADING FONTS **************************************************************

smallfont = pygame.font.SysFont('Corbel', 25)

# GAME MODES *****************************************************************

gameoptions = ['Classic', 'Boxed','Arcade', 'Exit']
cmode = 0

# LOADING IMAGES *************************************************************

bg = pygame.image.load('Assets/bg.png')
logo = pygame.image.load('Assets/logo.jpg')
logo2 = pygame.image.load('Assets/logo2.jpg')

gameover_img = pygame.image.load('Assets/gameover.png')
bar_img = pygame.image.load('Assets/bar.png')

# LOADING TILES **************************************************************

tile_list = []
for i in range(5):
	tile = pygame.image.load(f'Tiles/{i+1}.png')
	tile_list.append(tile)

tile_size = {
	1 : (16, 64),
	2 : (64, 16),
	3 : (32, 32),
	4 : (32, 32),
	5 : (32, 32)
}

# FUNCTIONS & CLASSES ********************************************************

def drawGrid():
	for row in range(ROWS):
		pygame.draw.line(win, WHITE, (0, row*CELLSIZE), (WIDTH, row*CELLSIZE), 1)
	for col in range(COLS):
		pygame.draw.line(win, WHITE, (col*CELLSIZE, 0), (col*CELLSIZE, HEIGHT))

def loadlevel(level):
	if level == 'boxed':
		file = f'Levels/boxed'
	else:
		file = f'Levels/level{level}_data'
	with open(file, 'rb') as f:
		data = pickle.load(f)
		for y in range(len(data)):
			for x in range(len(data[0])):
				if data[y][x] >= 0:
					data[y][x] += 1
	return data, len(data[0])

def tile_collide(leveld, head):
	for y in range(ROWS):
		for x in range(COLS):
			if leveld[y][x] > 0:
				tile = leveldata[y][x]
				pos = (x*CELLSIZE, y*CELLSIZE)

				rect = pygame.Rect(pos[0], pos[1], tile_size[tile][0],
								tile_size[tile][1])
				if rect.collidepoint(head):
					return True

	return False

class Snake:
	def __init__(self):
		self.length = 3
		self.direction = None
		self.x = COLS // 2
		self.y = ROWS // 2
		self.head = COLS//2 * CELLSIZE, ROWS//2 * CELLSIZE
		self.body = [[self.head[0]-2*CELLSIZE, self.head[1]],
					[self.head[0]-CELLSIZE, self.head[1]],
					self.head]
		print(self.body)

		self.headup = pygame.image.load('Assets/body/uhead.png')
		self.headdown = pygame.image.load('Assets/body/dhead.png')
		self.headleft = pygame.image.load('Assets/body/lhead.png')
		self.headright = pygame.image.load('Assets/body/rhead.png')

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

	def eatFood(self):
		self.length += 1

	def checkFood(self, food):
		if self.head[0] == food.x and self.head[1] == food.y:
			return True
		return False

	def tailCollision(self):
		head = self.body[-1]
		has_eaten_tail = False

		for i in range(len(self.body)-2):
			block = self.body[i]
			if head[0] == block[0] or head[1] == block[1]:
				has_eaten_tail = True

		return has_eaten_tail

	def draw(self):
		for index, block in enumerate(self.body):
			x, y = block
			rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
			if index == self.length - 1:
				head = self.body[index]
				neck = self.body[index-1]
				image = self.headright
				if head[0] == neck[0] and head[1] < neck[1]:
					image = self.headup
				elif head[0] == neck[0] and head[1] > neck[1]:
					image = self.headdown
				elif head[1] == neck[1] and head[0] < neck[0]:
					image = self.headleft
				elif head[1] == neck[1] and head[0] > neck[0]:
					image = self.headright
				win.blit(image, (x, y))
			
			# if block == self.head:
			# 	win.blit(self.headright, rect)
			# else:
			# 	pygame.draw.rect(win, GREEN, rect)

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

		if tile_collide(leveldata, (self.x, self.y)):
			self.respawn()

	def update(self):
		self.counter += 1
		if self.counter % 3 == 0:
			self.size += self.ds
			if self.size < 15 or self.size > 17:
				self.ds *= -1

			self.temp = pygame.transform.scale(self.image, (self.size, self.size))

	def draw(self):
		win.blit(self.temp, (self.x, self.y))

class Tree:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.counter = self.index = 0

		self.imglist = []
		for i in range(4):
			img = pygame.image.load(f'Assets/tree{i}.png')
			self.imglist.append(img)
		self.image = self.imglist[self.index]

	def update(self):
		self.counter += 1
		if self.counter % 3 == 0:
			self.index = (self.index + 1) % 3
			self.counter = 0
			self.image = self.imglist[self.index]

	def draw(self):
		win.blit(self.image, (self.x, self.y))

# GAME VARIABLES *************************************************************

level = 1
MAX_LEVEL = 4
score = 0

snake = Snake()
tree = Tree(WIDTH//2 - 8, HEIGHT//2 - 52)

homepage = True
gamepage = False
gameover = False

running = True
while running:
	selected = False
	win.fill(BLACK)
	win.blit(bg, (0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False

			if homepage:
				if event.key == pygame.K_UP:
					cmode -= 1
					if cmode < 0:
						cmode = 3

				if event.key == pygame.K_DOWN:
					cmode += 1
					if cmode > 3:
						cmode = 0

				if event.key == pygame.K_RETURN:
					selected = True
					if cmode == 3:
						running = False

			if event.key == pygame.K_RIGHT and snake.direction != 'left':
				snake.direction = 'right'

			if event.key == pygame.K_LEFT and snake.direction != 'right':
				snake.direction = 'left'

			if event.key == pygame.K_UP and snake.direction != 'down':
				snake.direction = 'up'

			if event.key == pygame.K_DOWN and snake.direction != 'up':
				snake.direction = 'down'

	if homepage:
		win.blit(logo, (0,0))
		win.blit(logo2, (0,225))

		for index, mode in enumerate(gameoptions):
			color = (32, 32, 32)
			if cmode == index:
				color = WHITE
			shadow = smallfont.render(mode, True, color)
			text = smallfont.render(mode, True, WHITE)
			win.blit(text, (WIDTH//2 - text.get_width()//2+1, HEIGHT//2 + 55*index+1))
			win.blit(shadow, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + 55*index))

		if selected:
			if cmode == 0:
				leveldata = [[0 for i in range(COLS)] for j in range(ROWS)]

			if cmode == 1:
				level = 'boxed'
				leveldata, length = loadlevel(level)

			if cmode == 2:
				level = 1
				leveldata, length = loadlevel(level)
				
			snake.__init__()
			food = Food()

			homepage = False
			gamepage = True
			score = 0			

		pygame.draw.rect(win, BLUE, (0,0,WIDTH,HEIGHT), 2)

	if gamepage:
		# drawGrid()

		if not gameover:	
			# draw level
			for y in range(ROWS):
				for x in range(COLS):
					if leveldata[y][x] > 0:
						tile = leveldata[y][x]
						pos = (x*CELLSIZE, y*CELLSIZE)
						rect = pygame.Rect(pos[0], pos[1], tile_size[tile][0],
								tile_size[tile][1])

						if tile != 3:
							pygame.draw.rect(win, (18, 18, 18), (rect.x+2, rect.y+2,
										 rect.width, rect.height))
						win.blit(tile_list[tile-1], pos)
						if rect.collidepoint(snake.head):
							gameover = True

			snake.update()
			snake.checkFood(food)
			snake.draw()
			food.update()
			food.draw()

			if snake.checkFood(food):
				snake.eatFood()
				food.respawn()
				score += 1

			if cmode == 0 or cmode == 1:
				tree.update()
				tree.draw()

				score_img = smallfont.render(f'{score}', True, WHITE)
				win.blit(score_img, (WIDTH-30 - score_img.get_width()//2, HEIGHT - 50))

			elif cmode == 2:
				bar = pygame.transform.scale(bar_img, (score*10, 10))
				win.blit(bar, (WIDTH//2-50, HEIGHT-50))
				pygame.draw.rect(win, WHITE, (WIDTH//2-50, HEIGHT-51, 100, 10),1 , border_radius=10)

				if score and score % 10 == 0:
					level += 1
					if level <= MAX_LEVEL:
						leveldata, length = loadlevel(level)
						score = 0
						snake.__init__()
					else:
						gameover = True
		else:
			win.blit(gameover_img, (WIDTH//2 - gameover_img.get_width()//2, 80))
			pygame.draw.rect(win, BLUE, (0,0,WIDTH,HEIGHT), 2)

	clock.tick(FPS)
	pygame.display.update()
pygame.quit()