import os
import pygame
import pickle
import button

pygame.init()

# game window
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
MARGIN_LEFT = 150
WIDTH = SCREEN_WIDTH + MARGIN_LEFT
HEIGHT = SCREEN_HEIGHT

TILE_WIDTH = 16
TILE_HEIGHT = 16
NUM_TILES = 5

ROWS = SCREEN_HEIGHT // TILE_HEIGHT
COLS = MAX_COLS = SCREEN_WIDTH // TILE_WIDTH

clock = pygame.time.Clock()
FPS = 30

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Level Editor')

# game_variables **************************************************************
current_tile = 0
current_level = 1

# color variabes
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (255, 25, 25)

font = pygame.font.SysFont('Futura', 24)

# tile list
world_data = []
for row in range(ROWS):
	col = [-1] * MAX_COLS
	world_data.append(col)

# load images
bg = pygame.image.load('assets/bg.png')

save_img = pygame.image.load('assets/save_btn.png')
load_img = pygame.image.load('assets/load_btn.png')
left_img = pygame.image.load('assets/left.png')
right_img = pygame.image.load('assets/right.png')

# load tileset

img_list = []
for i in range(1,NUM_TILES+1):
	img = pygame.image.load(f'tiles/{i}.png')
	# img = pygame.transform.scale(img, (TILE_WIDTH, TILE_SIZE))
	img_list.append(img)

def draw_grid():
	# horizontal lines
	for c in range(ROWS + 1):
		pygame.draw.line(win, WHITE, (0, c * TILE_HEIGHT), (SCREEN_WIDTH, c * TILE_HEIGHT))
	# vertical lines
	for c in range(MAX_COLS + 1):
		pygame.draw.line(win, WHITE, (c * TILE_WIDTH, 0), (c * TILE_WIDTH , SCREEN_HEIGHT))

def draw_world():
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:
				win.blit(img_list[tile], (x*TILE_WIDTH, y*TILE_HEIGHT))

def draw_text(text_, font, color, pos):
	text = font.render(text_, True, color)
	win.blit(text, pos)

# draw_buttons
button_list = []
b_col = 0
b_row = 0
for i in range(len(img_list)):
	# if TILE_WIDTH > 16:
	image = pygame.transform.scale(img_list[i], (16,16))
	# else:
	# 	image = img_list[i]
	t_button = button.Button(SCREEN_WIDTH + (35 * b_col + 15), 30 * b_row + 10, image, 1)
	button_list.append(t_button)

	b_col += 1
	if b_col == 4:
		b_row += 1
		b_col = 0

# #create load and save buttons
load_button = button.Button(SCREEN_WIDTH + 10, SCREEN_HEIGHT - 95, load_img, 0.7)
save_button = button.Button(SCREEN_WIDTH + 85, SCREEN_HEIGHT - 95, save_img, 0.7)
left_button = button.Button(SCREEN_WIDTH + 10, SCREEN_HEIGHT - 35, left_img, 1)
right_button = button.Button(SCREEN_WIDTH + 120, SCREEN_HEIGHT - 35, right_img, 1)


running = True
while running:
	win.blit(bg, (0,0))
	draw_grid()
	draw_world()

	# draw button panel
	pygame.draw.rect(win, GREEN, (SCREEN_WIDTH,0, MARGIN_LEFT, HEIGHT))

	b_count = 0
	for index, i in enumerate(button_list):
		if i.draw(win):
			current_tile = index
			print(current_tile)

	# highlight current tile
	pygame.draw.rect(win, RED, button_list[current_tile].rect, 3)

	# add new tiles
	pos = pygame.mouse.get_pos()
	x = ((pos[0]) // TILE_WIDTH)
	y = (pos[1] // TILE_HEIGHT)

	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		if pygame.mouse.get_pressed()[2] == 1:
				world_data[y][x] = -1


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	if save_button.draw(win):
		#save level data
		pickle_out = open(f'levels/level{current_level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
	if load_button.draw(win):
		#load in level data
		if os.path.exists(f'levels/level{current_level}_data'):
			pickle_in = open(f'levels/level{current_level}_data', 'rb')
			data = pickle.load(pickle_in)
			for i in range(len(data)):
				for j in range(len(data[0])):
					world_data[i][j] = data[i][j]
			del data

	if left_button.draw(win):
		current_level -= 1
		if current_level < 1:
			current_level = 1
	if right_button.draw(win):
		current_level += 1

	#text showing current level
	draw_text(f'Level: {current_level}', font, WHITE, (SCREEN_WIDTH + 53, SCREEN_HEIGHT - 25))
	pygame.draw.line(win, WHITE, (SCREEN_WIDTH+10, HEIGHT-50), (WIDTH-10, HEIGHT-50), 2)

	clock.tick(FPS)
	pygame.display.update()

pygame.quit()