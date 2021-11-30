import random
import pygame
from objects import Block, Text, Counter, Button

pygame.init()
SCREEN = WIDTH, HEIGHT = 270, 480
win = pygame.display.set_mode(SCREEN)
pygame.display.set_caption('Piano Tiles')

clock = pygame.time.Clock()
FPS = 30

### Loading Images ************************************************************
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

### Loading Images ************************************************************
bg = pygame.image.load('Assets/bg.png')
overlay = pygame.image.load('Assets/red overlay.png').convert_alpha()
piano = pygame.image.load('Assets/piano.png').convert_alpha()
piano = pygame.transform.scale(piano, (212, 212))

### Fonts *********************************************************************
pygame.font.init()
score_font = pygame.font.Font('Fonts/Futura condensed.ttf', 30)
title_font = pygame.font.Font('Fonts/Alternity-8w7J.ttf', 30)
gameover_font = pygame.font.Font('Fonts/Alternity-8w7J.ttf', 40)

### Sounds ********************************************************************
pygame.mixer.music.load('Sounds/Bluestone Alley-Adapted.mp3')
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(loops=-1)

sound_list = []
sound_index = 0
for s in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
	sound = pygame.mixer.Sound(f'Sounds/{s}.mp3')
	sound_list.append(sound)
fail_page = pygame.mixer.Sound('Sounds/buzzer.mp3')

### Buttons *******************************************************************
start_img = pygame.image.load('Assets/start.png')
start_btn = Button(start_img, (120,40), 80, 380)

restart_img = pygame.image.load('Assets/restart.png')
menu_img = pygame.image.load('Assets/menu.png')

restart_btn = Button(restart_img, (40,40), 80, 320)
menu_btn = Button(menu_img, (40,40), 160, 320)

### EVENTS ********************************************************************
ADDBLOCK = pygame.USEREVENT + 1
ADDTIME = 650
pygame.time.set_timer(ADDBLOCK, ADDTIME)

### Sprite Groups *************************************************************
block_group = pygame.sprite.Group()
score_group = pygame.sprite.Group()

counter = Counter(win, gameover_font) 

# Game Variables **************************************************************
can_move = True
display_overlay = False
first_click = False
start_time = None
game_over = False
game_started = False

block_speed = 6
score = 0
high = 0
overlay_index = 0

running = True
while running:
	pos = None
	clicked_on_tile = False

	win.blit(bg, (0,0))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN and game_started:
			if event.button == 1 and not game_over:
				pos = pygame.mouse.get_pos()

				if not first_click:
					first_click = True
					start_time = pygame.time.get_ticks()

		if event.type == ADDBLOCK and not game_over and game_started and can_move:
			x_col = random.randint(0,3)
			block = Block(win, (67.5 * x_col, -120))
			block_group.add(block)

	if not game_started:
		win.blit(piano, (WIDTH//8, HEIGHT//8))
		img = title_font.render('Piano Tiles', True, WHITE)
		win.blit(img, (WIDTH // 2 - img.get_width() / 2 + 10, 300))
		if start_btn.draw(win):
			game_started = True
			display_overlay = False
			start_count = True
			can_move = False
	else:
		if start_count:
			if counter.count <= 0:
				can_move = True
				start_count = False
			counter.update()	
		else:
			block_group.update(can_move, block_speed)
			score_group.update(block_speed)
			if not game_over:
				for block in block_group:
					if block.game_over:
						game_over = True
						can_move = False
						fail_page.play()
				if pos:
					for block in block_group:
						if block.rect.collidepoint(pos):
							pos = list(block.get_pos())
							pos = (pos[0] + 25, pos[1])
							text = Text('+3', score_font, pos, win)
							score_group.add(text)

							if block.is_alive:
								score += 3
								if score >= high:
									high = score

								sound_list[sound_index].play()
								sound_index += 1
								if sound_index >= 6:
									sound_index = 0

							block.is_alive = False
							block.color = (0,0,0, 90)
							clicked_on_tile = True

					if not clicked_on_tile:
						game_over = True
						can_move = False
						fail_page.play()

				if start_time:
					current_time = pygame.time.get_ticks()
					delta = current_time - start_time
					if delta > 1200:
						block_speed += 1
						if block_speed % 10 == 0:
							if ADDTIME >= 450:
								ADDTIME -= 80
								pygame.time.set_timer(ADDBLOCK, ADDTIME)
						start_time = current_time
			else:
				can_move = False
				display_overlay = True

		if display_overlay:
			if overlay_index > 10 or overlay_index % 3 == 0:
				win.blit(overlay, (0,0))
			overlay_index += 1

			img1 = gameover_font.render('Game over', True, WHITE)
			img2 = score_font.render(f'Score : {score}', True, WHITE)
			win.blit(img1, (WIDTH // 2 - img1.get_width() / 2, 180))
			win.blit(img2, (WIDTH // 2 - img2.get_width() / 2,250))

			if restart_btn.draw(win):
				display_overlay = False
				block_group.empty()
				first_click = False
				block_speed = 6
				start_time = None
				game_over = False
				start_count = True

				score = 0
				overlay_index = 0
				counter.count = 3
				ADDTIME = 650
				pygame.time.set_timer(ADDBLOCK, ADDTIME)
			if menu_btn.draw(win):
				game_started = False
				can_move = False
				display_overlay = False
				block_group.empty()
				first_click = False
				block_speed = 6
				start_time = None
				game_over = False
				game_started = False
				start_count = True

				score = 0
				high = 0
				overlay_index = 0
				counter.count = 3
				ADDTIME = 650
				pygame.time.set_timer(ADDBLOCK, ADDTIME)
		else:
			if not start_count:
				img1 = score_font.render(f'Score : {score}', True, WHITE)
				win.blit(img1, (70 - img1.get_width() / 2, 10))

				img2 = score_font.render(f'High : {high}', True, WHITE)
				win.blit(img2, (200 - img2.get_width() / 2, 10))

	clock.tick(FPS)
	pygame.display.update()

pygame.quit()