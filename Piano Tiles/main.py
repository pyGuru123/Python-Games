# Piano Tiles

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 30 November, 2021

import json
import random
import pygame
from threading import Thread

from objects import Tile, Square

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
TILE_WIDTH = WIDTH // 4
TILE_HEIGHT = 130

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 30

# COLORS *********************************************************************

WHITE = (255, 255, 255)
GRAY = (75, 75, 75)
BLUE = (30, 144, 255)

# IMAGES *********************************************************************

bg_img = pygame.image.load('Assets/bg.png')
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

piano_img = pygame.image.load('Assets/piano.png')
piano_img = pygame.transform.scale(piano_img, (212, 212))

start_img = pygame.image.load('Assets/start.png')
start_img = pygame.transform.scale(start_img, (120, 40))
start_rect = start_img.get_rect(center=(WIDTH//2, HEIGHT-80))

overlay = pygame.image.load('Assets/red overlay.png')
overlay = pygame.transform.scale(overlay, (WIDTH, HEIGHT))

# MUSIC **********************************************************************

buzzer_fx = pygame.mixer.Sound('Sounds/piano-buzzer.mp3')

pygame.mixer.music.load('Sounds/piano-bgmusic.mp3')
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(loops=-1)

# GROUPS & OBJECTS ***********************************************************

square_group = pygame.sprite.Group()
tile_group = pygame.sprite.Group()

# FUNCTIONS ******************************************************************

def get_speed(score):
	return 200 + 5 * score

def play_notes(notePath):
	pygame.mixer.Sound(notePath).play()

# NOTES **********************************************************************

with open('notes.json') as file:
	notes_dict = json.load(file)

notes_list = notes_dict['4']
note_count = 0
pygame.mixer.set_num_channels(len(notes_list))

# VARIABLES ******************************************************************

num_tiles = 0
score = 0
speed = 1

clicked = False
pos = None

home_page = True
game_page = False
game_over = False

count = 0
overlay_index = 0


running = True
while running:
	pos = None

	count += 1
	if count % 100 == 0:
			square = Square(win)
			square_group.add(square)
			counter = 0

	win.blit(bg_img, (0,0))
	square_group.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

		if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
			pos = event.pos

	if home_page:
		win.blit(piano_img, (WIDTH//8, HEIGHT//8))
		win.blit(start_img, start_rect)

		if pos and start_rect.collidepoint(pos):
			home_page = False
			game_page = True

			x = random.randint(0, 3)
			t = Tile(x * TILE_WIDTH, -TILE_HEIGHT, win)
			tile_group.add(t)

			num_tiles += 1
			pos = None

	if game_page:
		for tile in tile_group:
			tile.update(speed)

			if pos:
				if tile.rect.collidepoint(pos):
					tile.alive = False
					score += 1
					pos = None

					note = notes_list[note_count].strip()
					print(note)
					th = Thread(target=play_notes, args=(f'Sounds/{note}.ogg', ))
					th.start()
					th.join()
					note_count = (note_count + 1) % len(notes_list)

			if tile.rect.bottom >= HEIGHT and tile.alive:
				tile.color = (255, 0, 0)
				game_over = True

		if pos:
			buzzer_fx.play()
			game_over = True

		if len(tile_group) > 0:
			t = tile_group.sprites()[-1]
			if t.rect.top + speed >= 0:
				x = random.randint(0, 3)
				y = -TILE_HEIGHT - (0 - t.rect.top)
				t = Tile(x * TILE_WIDTH, y, win)
				tile_group.add(t)
				num_tiles += 1

		for i in range(4):
			pygame.draw.line(win, WHITE, (TILE_WIDTH * i, 0), (TILE_WIDTH*i, HEIGHT), 1)

		speed = int(get_speed(score) * (FPS / 1000))

		if game_over:
			speed = 0
			pos = None

			if overlay_index > 20 or overlay_index % 3 == 0:
				win.blit(overlay, (0,0))
			overlay_index += 1

	pygame.draw.rect(win, BLUE, (0,0, WIDTH, HEIGHT), 2)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()