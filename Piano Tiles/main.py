# Piano Tiles

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 30 November, 2021

import json
import random
import pygame
from threading import Thread

from objects import Tile

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
start_img = pygame.transform.scale(start_img, (212, 212))

# MUSIC **********************************************************************

buzzer_fx = pygame.mixer.Sound('Sounds/piano-buzzer.mp3')

pygame.mixer.music.load('Sounds/piano-bgmusic.mp3')
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(loops=-1)

# GROUPS & OBJECTS ***********************************************************

tile_group = pygame.sprite.Group()
x = random.randint(0, 3)
t = Tile(x * TILE_WIDTH, -TILE_HEIGHT, win)
tile_group.add(t)

# FUNCTIONS ******************************************************************

def get_speed(score):
	return 200 + 6 * score

def play_notes(notePath):
	pygame.mixer.Sound(notePath).play()

# NOTES **********************************************************************

with open('notes.json') as file:
	notes_dict = json.load(file)

notes_list = notes_dict['1']
note_count = 0
pygame.mixer.set_num_channels(len(notes_list))

# VARIABLES ******************************************************************

num_tiles = 1
score = 0
speed = 1

clicked = False
pos = None

home_page = False
game_page = True
score_page = False

running = True
while running:
	pos = None
	win.blit(bg_img, (0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = event.pos

	if home_page:
		win.blit(piano_img, (WIDTH//8, HEIGHT//8))

	if score_page:
		pass

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
				running = False

		if pos:
			buzzer_fx.play()
			running = False


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

	pygame.draw.rect(win, BLUE, (0,0, WIDTH, HEIGHT), 2)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()