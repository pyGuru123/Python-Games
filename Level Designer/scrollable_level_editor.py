import os
import pygame
import pickle
import button

pygame.init()

# game window
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 480
MARGIN_LEFT = 300
WIDTH = SCREEN_WIDTH + MARGIN_LEFT
HEIGHT = SCREEN_HEIGHT

ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS

clock = pygame.time.Clock()
FPS = 30

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Level Designer')

# game_variables
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
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

# populating last row with ground
# for i in range(MAX_COLS):
# 	world_data[ROWS-1][i] = 0

# load images
sky_img = pygame.image.load('assets/BG1.png')
mountain_img = pygame.image.load('assets/mountain.png')
save_img = pygame.image.load('assets/save_btn.png')
load_img = pygame.image.load('assets/load_btn.png')
left_img = pygame.image.load('assets/left.png')
right_img = pygame.image.load('assets/right.png')

img_list = []
for i in range(1,30):
	img = pygame.image.load(f'tiles/{i}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)


def draw_bg():
	win.fill(GREEN)
	width = sky_img.get_width()
	for x in range(4):
		win.blit(sky_img, ((x*width)-scroll * 0.5,0))
		win.blit(mountain_img, ((x*width)-scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height()  + 35))

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
	t_button = button.Button(SCREEN_WIDTH + (50 * b_col + 30), 50 * b_row + 30, img_list[i], 1)
	button_list.append(t_button)

	b_col += 1
	if b_col == 5:
		b_row += 1
		b_col = 0

# #create load and save buttons
load_button = button.Button(SCREEN_WIDTH + 10, SCREEN_HEIGHT - 80, load_img, 1)
save_button = button.Button(SCREEN_WIDTH + 110, SCREEN_HEIGHT - 80, save_img, 1)
left_button = button.Button(SCREEN_WIDTH + 30, SCREEN_HEIGHT - 35, left_img, 1)
right_button = button.Button(SCREEN_WIDTH + 140, SCREEN_HEIGHT - 35, right_img, 1)


running = True
while running:
	draw_bg()
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


	# map scroller
	if scroll_left and scroll > 0:
		scroll -= 5 * scroll_speed
	if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
		scroll += 5 * scroll_speed

	# add new tiles
	pos = pygame.mouse.get_pos()
	x = ((pos[0] + scroll) // TILE_SIZE)
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
		pickle_out = open(f'scrollable_levels/level{current_level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
	if load_button.draw(win):
		#load in level data
		if os.path.exists(f'scrollable_levels/level{current_level}_data'):
			pickle_in = open(f'scrollable_levels/level{current_level}_data', 'rb')
			world_data = pickle.load(pickle_in)

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