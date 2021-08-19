import os
import pygame
import pickle
from pygame.locals import *

# SETUP *****************************************

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption('Connected')

clock = pygame.time.Clock()
FPS = 45

TILE_SIZE = 16
ROWS, COLS = HEIGHT // 16, WIDTH // 16

# Level Variables

NUM_TILES = 88              # Number of tiles you have in tiles folder
current_level = 1           # level which you want to create / edit.

# FONTS *****************************************

pygame.font.init()
font = pygame.font.SysFont('Bauhaus 93', 20)

# COLORS ***************************************

WHITE = (255,255,255)
BLUE = (30, 144, 255)

if not os.path.exists('levels/'):
	os.mkdir('levels/')
	
# Images ****************************************

bg = pygame.image.load("Assets/bg.png")

# Empty world data

world_data = []
for r in range(ROWS):
	c = [0] * COLS
	world_data.append(c)

# load tiles

tiles = []
for t in range(1,NUM_TILES+1):
	tile = pygame.image.load(f"tiles/{t}.png")
	tile = pygame.transform.rotate(tile, -90)
	tiles.append(tile)
	
# FUNCTIONS ************************************

# draw grid
def draw_grid(win):
	# ROWS
	for r in range(ROWS-1):
		pygame.draw.line(win, WHITE, (0,TILE_SIZE * r), (3 * TILE_SIZE, TILE_SIZE * r), 2)
	# 3, COLS
	for c in range(4):
		pygame.draw.line(win, WHITE, (TILE_SIZE * c,0), (TILE_SIZE * c, HEIGHT - 2 * TILE_SIZE), 2)
		
# draw text
def draw_text(text_, color, pos):
	text = font.render(text_, True, color)
	win.blit(text, pos)
		
# draw_box
def draw_box(r, c):
	t = TILE_SIZE
	pygame.draw.rect(win, BLUE, (c * t, r * t, t, t ), 2)
	
# draw text
def draw_text(text_, color, pos):
	text = font.render(text_, True, color)
	win.blit(text, pos)

	
# draw world
def draw_world():
	for row in range(ROWS):
		for col in range(COLS):
			index = world_data[row][col]
			if index > 0:
				img = tiles[index-1]
				win.blit(img, (col * TILE_SIZE, row * TILE_SIZE))
				
# BUTTONS
				
class Button:
	def __init__(self, pos, image, scale):
		self.image = image
		
		if scale:
			self.image = pygame.transform.scale(self.image, (30, 16))
			
		self.image = pygame.transform.rotate(self.image, -90)
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
	
load_img = pygame.image.load('assets/load_btn.png')
save_img = pygame.image.load('assets/save_btn.png')
clear_img = pygame.image.load('assets/clear.png')

load_button = Button((1, 30 * TILE_SIZE + 2), load_img, True)
save_button = Button((17, 30 * TILE_SIZE + 2), save_img, True)
clear_button = Button((33, 30 * TILE_SIZE + 2), clear_img, True)

# Tiles

class Tile():
	def __init__(self, pos, image, index):
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
	row = index //  3
	column = index %  3
	pos = (column * TILE_SIZE), (row * TILE_SIZE)
	t = Tile(pos, tile, index+1)
	tile_group.append(t)
				
# VARIABLES ************************************

clicked = False
pos = None
r, c = 0, 3
		
# Main
running = True
while running:
	#win.fill((0,0,0))
	win.blit(bg, (0,0))
	
	for tile in tile_group:
		index = tile.update()
		if index:
			world_data[r][c] = index
			
	draw_grid(win)
	draw_world()
	draw_box(r, c)
	
#	t = f"{pos}, {r}, {c}"
#	draw_text(t, BLUE, (10,500))
	
	pos = None
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = event.pos
			x, y = pos[1] // TILE_SIZE, pos[0] // TILE_SIZE
			if y >= 3:
				r = x
				c = y
			
	
	if save_button.draw():
		pickle_out = open(f'levels/level{current_level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
		
	if load_button.draw():
		if os.path.exists(f'levels/level{current_level}_data'):
			pickle_out = open(f'levels/level{current_level}_data_backup', 'wb')
			pickle.dump(world_data, pickle_out)
			
			pickle_in = open(f'levels/level{current_level}_data', 'rb')
			world_data = pickle.load(pickle_in)
			
	if clear_button.draw():
		world_data[r][c] = 0
	
			
	clock.tick(FPS)
	pygame.display.update()
			
pygame.quit()