import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pickle
import pygame
from pygame.locals import *
from pprint import pprint

if not os.path.exists('levels/'):
	os.mkdir('levels/')


# EDIT HERE ( WINDOW SIZE & TILE SIZE )
SIZE = WIDTH , HEIGHT= 1000, 650
tile_size = 50

# Not to be edited
pygame.init()
clock = pygame.time.Clock()
fps = 30

cols = WIDTH // tile_size
rows = HEIGHT // tile_size
margin = 210

win_width = WIDTH + margin
win_height = HEIGHT

win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Level Editor')

# load backgrounds
sun_img = pygame.image.load('assets/sun.png')
bg_img = pygame.image.load('assets/BG1.png')
bg_img = pygame.transform.scale(bg_img, (win_width - margin, HEIGHT))

# load buttons
save_img = pygame.image.load('assets/save_btn.png')
load_img = pygame.image.load('assets/load_btn.png')
left_img = pygame.image.load('assets/left.png')
right_img = pygame.image.load('assets/right.png')

# load tiles
tiles = []
for t in sorted(os.listdir('tiles/'), key=lambda s: int(s[:-4])):
	tile = pygame.image.load('tiles/' + t)
	tiles.append(tile)


#define game variables
clicked = False
current_level = 1

#define colours
WHITE = (255, 255, 255)
GREEN = (144, 201, 120)
BLUE = (30, 144, 255)

font = pygame.font.SysFont('Futura', 24)

# Empty world data
world_data = []
for r in range(rows):
	c = [0] * cols
	world_data.append(c)

def draw_text(text_, font, color, pos):
	text = font.render(text_, True, color)
	win.blit(text, pos)

def draw_lines():
	for row in range(rows+1):
		pygame.draw.line(win, WHITE, (0, tile_size*row), (WIDTH, tile_size*row), 2)
	for col in range(cols):
		pygame.draw.line(win, WHITE, (tile_size*col, 0), (tile_size*col, HEIGHT), 2)

def draw_world():
	for row in range(rows):
		for col in range(cols):
			index = world_data[row][col]
			if index > 0:
				if index in range(1,14) or index in (25,26):
					#dirt block
					img = pygame.transform.scale(tiles[index-1], (tile_size, tile_size))
					win.blit(img, (col * tile_size, row * tile_size))
				if index == 14:
					#bush blocks
					img = pygame.transform.scale(tiles[index-1], (tile_size, int(tile_size * 0.50)))
					win.blit(img, (col * tile_size, row * tile_size + tile_size // 2))
				if index == 15:
					#lava blocks
					img = pygame.transform.scale(tiles[index-1], (tile_size, int(tile_size * 0.50)))
					win.blit(img, (col * tile_size, row * tile_size + tile_size // 2))
				if index == 16:
					#Lava Still block
					img = pygame.transform.scale(tiles[index-1], (tile_size, tile_size))
					win.blit(img, (col * tile_size, row * tile_size))
				if index == 17:
					#Diamond blocks
					img = pygame.transform.scale(tiles[index-1], (tile_size, tile_size))
					win.blit(img, (col * tile_size, row * tile_size))
				if index == 18:
					#Crate block
					img = pygame.transform.scale(tiles[index-1], (tile_size, tile_size))
					win.blit(img, (col * tile_size, row * tile_size))
				if index == 19:
					#Water blocks
					img = pygame.transform.scale(tiles[index-1], (tile_size, int(tile_size * 0.50)))
					win.blit(img, (col * tile_size, row * tile_size + tile_size // 2))
				if index == 20:
					#Water blocks
					img = pygame.transform.scale(tiles[index-1], (tile_size, tile_size))
					win.blit(img, (col * tile_size, row * tile_size))
				if index == 21:
					#tree blocks
					img = pygame.transform.scale(tiles[index-1], (3*tile_size, 3 * tile_size))
					win.blit(img, ((col-1) * tile_size + 10, (row-2) * tile_size + 5))
				if index == 22:
					#mushroom blocks
					img = pygame.transform.scale(tiles[index-1], (int(tile_size * 0.80), int(tile_size * 0.80)))
					win.blit(img, (col * tile_size + tile_size//8, row * tile_size + tile_size // 5))
				if index == 23:
					#Bee blocks
					img = pygame.transform.scale(tiles[index-1], (50, 50))
					win.blit(img, (col * tile_size, row * tile_size))
				if index == 24:
					#Bee blocks
					img = tiles[index-1]
					win.blit(img, (col * tile_size - tile_size//4, row * tile_size - tile_size//4))
				if index == 27:
					#flower blocks
					img = pygame.transform.scale(tiles[index-1], (2*tile_size, tile_size))
					win.blit(img, ((col) * tile_size, row * tile_size))
				if index == 28:
					#treelimb blocks
					img = pygame.transform.scale(tiles[index-1], (5*tile_size + 20, tile_size))
					win.blit(img, ((col-2) * tile_size + 10, row * tile_size + tile_size // 4))
				if index == 29:
					#slime blocks
					img = pygame.transform.scale(tiles[index-1], (int(1.2*tile_size), tile_size))
					win.blit(img, (col * tile_size - 10, row * tile_size))


class Button:
	def __init__(self, pos, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = pos
		self.clicked = False

	def draw(self):
		action = False

		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		win.blit(self.image, self.rect)

		return action

class Tile():
	def __init__(self, pos, image, index):
		image = pygame.transform.scale(image, (40,40))
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = pos
		self.clicked = False
		self.index = index

	def update(self):
		action = False

		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = self.index
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		win.blit(self.image, self.rect)

		return action

tile_group = []
for index, tile in enumerate(tiles):
	row = index // (margin // (40 + 5) )
	column = index %  (margin // (40 + 5) )
	pos = (WIDTH + 5 +(column * tile_size) + 5, 5 + row * tile_size + 5)
	t = Tile(pos, tile, index+1)
	tile_group.append(t)

# #create load and save buttons
load_button = Button((WIDTH + 10, HEIGHT - 80), load_img)
save_button = Button((WIDTH + 110, HEIGHT - 80), save_img)
left_button = Button((WIDTH + 30, HEIGHT - 35), left_img)
right_button = Button((WIDTH + 140, HEIGHT - 35), right_img)

initial_r = pygame.Rect(1*tile_size,1*tile_size,tile_size, tile_size)
rect = [initial_r, [1,1]]

running = True
while running:
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False

		if event.type == MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			if pos[0] <= WIDTH:
				x = pos[0] // tile_size
				y = pos[1] // tile_size
				if pygame.mouse.get_pressed()[0]:
					r = rect[1]
					if r == [x,y]:
						world_data[y][x] += 1
						if world_data[y][x] >= len(tiles) + 1:
							world_data[y][x] = 0
					else:
						r1 = pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size)
						r2 = [x,y]
						rect = [r1, r2]
				elif pygame.mouse.get_pressed()[2]:
					r = rect[1]
					if r == [x,y]:
						world_data[y][x] -= 1
						if world_data[y][x] < 0:
							world_data[y][x] = len(tiles)
					else:
						r1 = pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size)
						r2 = [x,y]
						rect = [r1, r2]


		if event.type == KEYDOWN:
			pos = rect[1]
			if event.key == K_LEFT:
				if pos[0] > 0:
					pos[0] -= 1
			elif event.key == K_RIGHT:
				if pos[0] < cols-1:
					pos[0] += 1
			elif event.key == K_UP:
				if pos[1] > 0:
					pos[1] -= 1
			elif event.key == K_DOWN:
				if pos[1] < rows-1:
					pos[1] += 1

			rect[0] = pygame.Rect(pos[0]*tile_size, pos[1]*tile_size, tile_size, tile_size)
			rect[1] = pos

		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False

	win.fill(BLUE)
	win.blit(bg_img, (0,0))
	win.blit(sun_img, (80,60))
	draw_lines()
	draw_world()
	pygame.draw.rect(win, (255,0,0), rect[0], 3)

	for tile in tile_group:
		index = tile.update()
		if index:
			current_tile = index
			r = rect[1]
			world_data[r[1]][r[0]] = index

	if save_button.draw():
		#save level data
		pickle_out = open(f'levels/level{current_level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
	if load_button.draw():
		#load in level data
		if os.path.exists(f'levels/level{current_level}_data'):
			pickle_in = open(f'levels/level{current_level}_data', 'rb')
			world_data = pickle.load(pickle_in)

	if left_button.draw():
		current_level -= 1
		if current_level < 1:
			current_level = 1
	if right_button.draw():
		current_level += 1

	#text showing current level
	draw_text(f'Level: {current_level}', font, WHITE, (WIDTH + 70, win_height - 25))

	pygame.display.flip()

pygame.quit()