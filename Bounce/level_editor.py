import os
import pygame
import pickle
import button

pygame.init()

# game window
SCREEN_WIDTH = 192
SCREEN_HEIGHT = 192
MARGIN_LEFT = 450
WIDTH = SCREEN_WIDTH + MARGIN_LEFT
HEIGHT = SCREEN_HEIGHT

ROWS = 12
MAX_COLS = 100
TILE_SIZE = 16
NUM_TILES = 28

clock = pygame.time.Clock()
FPS = 30

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Level Designer')

# game_variables
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 0.5
current_tile = 0
current_level = 1

# color variabes
BLACK = (25, 25, 25)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 25, 25)
BLUE = (30, 144, 255)

font = pygame.font.SysFont('Futura', 24)

# tile list
world_data = []
for row in range(ROWS):
	col = [-1] * MAX_COLS
	world_data.append(col)

# populating last row with ground
for i in range(MAX_COLS):
	world_data[ROWS-1][i] = 0

# load images
save_img = pygame.image.load('assets/save_btn.png')
load_img = pygame.image.load('assets/load_btn.png')
left_img = pygame.image.load('assets/left.png')
right_img = pygame.image.load('assets/right.png')

img_list = []
for i in range(1,NUM_TILES + 1):
	img = pygame.image.load(f'tiles/{i}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

def draw_grid():
	# horizontal lines
	for c in range(ROWS + 1):
		pygame.draw.line(win, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))
	# vertical lines
	for c in range(MAX_COLS + 1):
		pygame.draw.line(win, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))

def draw_world():
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:
				win.blit(img_list[tile], (x*TILE_SIZE - scroll, y*TILE_SIZE))

def draw_text(text_, font, color, pos):
	text = font.render(text_, True, color)
	win.blit(text, pos)

# draw_buttons
button_list = []
b_col = 0
b_row = 0
for i in range(len(img_list)):
	t_button = button.Button(img_list[i], False, SCREEN_WIDTH + (30 * b_col + 20), 30 * b_row + 20,)
	button_list.append(t_button)

	b_col += 1
	if b_col == 12:
		b_row += 1
		b_col = 0

#create load and save buttons
load_button = button.Button(load_img, (56, 30), SCREEN_WIDTH + 220, SCREEN_HEIGHT - 35)
save_button = button.Button(save_img, (56, 30), SCREEN_WIDTH + 310, SCREEN_HEIGHT - 35)
left_button = button.Button(left_img, False, SCREEN_WIDTH + 30, SCREEN_HEIGHT - 35)
right_button = button.Button(right_img, False, SCREEN_WIDTH + 140, SCREEN_HEIGHT - 35)


running = True
while running:
	win.fill((175, 207, 240))
	draw_grid()
	draw_world()

	# draw button panel
	pygame.draw.rect(win, BLACK, (SCREEN_WIDTH,0, MARGIN_LEFT, HEIGHT))
	pygame.draw.line(win, WHITE, (SCREEN_WIDTH, SCREEN_HEIGHT-45), (WIDTH, SCREEN_HEIGHT-45))

	b_count = 0
	for index, i in enumerate(button_list):
		if i.draw(win):
			current_tile = index
			
	# highlight current tile
	pygame.draw.rect(win, GREEN, button_list[current_tile].rect, 3)

	# map scroller
	if scroll_left and scroll > 0:
		scroll -= 5 * scroll_speed
	if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
		scroll += 5 * scroll_speed

	# add new tiles
	pos = pygame.mouse.get_pos()
	x = int((pos[0] + scroll) // TILE_SIZE)
	y = (pos[1] // TILE_SIZE)

	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		if pygame.mouse.get_pressed()[2] == 1:
				world_data[y][x] = -1


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				scroll_left = True
			if event.key == pygame.K_RIGHT:
				scroll_right = True
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 5

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scroll_left = False
			if event.key == pygame.K_RIGHT:
				scroll_right = False
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 1

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
			world_data = [[0 for j in range(MAX_COLS)] for i in range(ROWS)]
			for y in range(ROWS):
				for x in range(MAX_COLS):
					world_data[y][x] = data[y][x]

	if left_button.draw(win):
		current_level -= 1
		if current_level < 1:
			current_level = 1
	if right_button.draw(win):
		current_level += 1

	#text showing current level
	draw_text(f'Level: {current_level}', font, WHITE, (SCREEN_WIDTH + 70, SCREEN_HEIGHT - 25))

	clock.tick(FPS)
	pygame.display.update()

pygame.quit()