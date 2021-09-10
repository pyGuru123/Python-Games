import os
import pygame

from player import Ball
from world import World, load_level
from texts import Text, Message
from button import Button, LevelButton

pygame.init()
WIDTH, HEIGHT = 192, 212
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption('Bounce')

clock = pygame.time.Clock()
FPS = 30

# GAME VARIABLES **************************************************************
ROWS = 12
MAX_COLS = 150
TILE_SIZE = 16
MAX_LEVEL = 8

# COLORS **********************************************************************

BLUE = (175, 207, 240)
BLUE2 = (0, 0, 255)
WHITE = (255, 255, 255)

# FONTS ***********************************************************************

health_font = "Fonts/ARCADECLASSIC.TTF"

level_text = Text(health_font, 24)
health_text = Message(40, WIDTH + 10, 19, "x3", health_font, WHITE, win)
select_level_text = Message(WIDTH//2, 20, 24, "Select  Level", health_font, BLUE2, win)
current_level_text = Message(WIDTH - 40, WIDTH + 10, 20, "Level 1", health_font, WHITE, win)
you_win = Message(WIDTH //2, HEIGHT//2, 40, "You  Win", health_font, BLUE2, win)

# SOUNDS **********************************************************************

click_fx = pygame.mixer.Sound('Sounds/click.mp3')
life_fx = pygame.mixer.Sound('Sounds/gate.mp3')
checkpoint_fx = pygame.mixer.Sound('Sounds/checkpoint.mp3')

pygame.mixer.music.load('Sounds/track1.wav')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.4)

# LOADING IMAGES **************************************************************

ball_image = pygame.image.load('Assets/ball.png')
splash_img = pygame.transform.scale(pygame.image.load('Assets/splash_logo.png'),
			 (2*WIDTH, HEIGHT))
bounce_img = pygame.image.load('Assets/menu_logo.png')
game_lost_img = pygame.image.load('Assets/lose.png')
game_lost_img = pygame.transform.scale(game_lost_img, (WIDTH//2, 80))
level_locked_img = pygame.image.load('Assets/level_locked.png')
level_locked_img = pygame.transform.scale(level_locked_img, (40, 40))
level_unlocked_img = pygame.image.load('Assets/level_unlocked.png')
level_unlocked_img = pygame.transform.scale(level_unlocked_img, (40, 40))


play_img = pygame.image.load('Assets/play.png')
restart_img = pygame.image.load('Assets/restart.png')
menu_img = pygame.image.load('Assets/menu.png')
sound_on_img = pygame.image.load('Assets/SoundOnBtn.png')
sound_off_img = pygame.image.load('Assets/SoundOffBtn.png')
game_won_img = pygame.image.load('Assets/game won.png')


# BUTTONS *********************************************************************

play_btn = Button(play_img, False, 45, 130)
sound_btn = Button(sound_on_img, False, 45, 170)
restart_btn = Button(restart_img, False, 45, 130)
menu_btn = Button(menu_img, False, 45, 170)

# LEVEL TEXT & BUTTONS ********************************************************

level_btns = []
for level in range(MAX_LEVEL):
	text = level_text.render(f'{level+1}', (255, 255, 255))
	r = level // 3
	c = level % 3
	btn = LevelButton(level_locked_img, (40, 40), 20 + c * 55, 50 + r * 55, text)
	level_btns.append(btn)

# GROUPS **********************************************************************

spikes_group = pygame.sprite.Group()
inflator_group = pygame.sprite.Group()
deflator_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
checkpoint_group = pygame.sprite.Group()
health_group = pygame.sprite.Group()

objects_groups = [spikes_group, inflator_group, deflator_group, enemy_group, exit_group, 
					checkpoint_group, health_group]
collision_groups = [inflator_group, deflator_group]

# RESET ***********************************************************************

def reset_level_data(level):
	for group in objects_groups:
		group.empty()

	# LOAD LEVEL WORLD

	world_data, level_length = load_level(level)
	w = World(objects_groups)
	w.generate_world(world_data, win)

	return world_data, level_length, w

def reset_player_data(level):
	if level == 1:
		x, y = 64, 50
	if level == 2:
		x, y = 65, 50
	if level == 3:
		x, y = 64, 50
	if level == 4:
		x, y = 63, 50
	if level == 5:
		x, y = 64, 50
	if level == 6:
		x, y = 48, 50
	if level == 7:
		x, y = 78, 80
	if level == 8:
		x, y = 112,100

	p = Ball(x, y)
	moving_left = False
	moving_right = False

	return p, moving_left, moving_right

# VARIABLES *******************************************************************

moving_left = False
moving_right = False

SCROLL_THRES = 80
screen_scroll = 0
level_scroll = 0
level = 1
next_level = False
reset_level = False

checkpoint = None
health = 3
splash_count = 0
sound_on = True

logo_page = True
home_page = False
level_page = False
game_page = False
restart_page = False
win_page = False

running = True
while running:
	win.fill(BLUE)
	pygame.draw.rect(win, (255, 255,255), (0, 0, WIDTH, HEIGHT), 1, border_radius=5)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				moving_left = True
			if event.key == pygame.K_RIGHT:
				moving_right = True
			if event.key == pygame.K_UP:
				if not p.jump:
					p.jump = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				moving_left = False
			if event.key == pygame.K_RIGHT:
				moving_right = False

	if logo_page:
		win.blit(splash_img, (-100,0))
		splash_count += 1
		if splash_count % 50 == 0:
			logo_page = False
			home_page = True

	if home_page:
		win.blit(bounce_img, (10,10))
		
		if play_btn.draw(win):
			click_fx.play()
			home_page = False
			level_page = True
			
		if sound_btn.draw(win):
			click_fx.play()
			sound_on = not sound_on
			
			if sound_on:
				sound_btn.update_image(sound_on_img)
				pygame.mixer.music.play(loops=-1)
			else:
				sound_btn.update_image(sound_off_img)
				pygame.mixer.music.stop()

	if level_page:
		select_level_text.update(shadow=False)
		for index, btn in enumerate(level_btns):
			if index < level:
				if not btn.unlocked:
					btn.unlocked = True
					btn.update_image(level_unlocked_img)
			if btn.draw(win):
				if index < level:
					click_fx.play()
					level_page = False
					game_page = True
					level = index + 1
					screen_scroll = 0
					level_scroll = 0
					health = 3
					world_data, level_length, w = reset_level_data(level)
					p, moving_left, moving_right = reset_player_data(level)

	if restart_page:
		win.blit(game_lost_img, (45,20))
		if restart_btn.draw(win):
			click_fx.play()
			world_data, level_length, w = reset_level_data(level)
			p, moving_left, moving_right = reset_player_data(level)
			level_scroll = 0
			screen_scroll = 0
			health = 3
			checkpoint = None
			restart_page = False
			game_page = True

		if menu_btn.draw(win):
			click_fx.play()
			home_page = True
			restart_page = False

	if win_page:
		win.blit(game_won_img, (45, 20))
		you_win.update()
		if menu_btn.draw(win):
			click_fx.play()
			home_page = True
			win_page = False
			restart_page = False


	if game_page:
		w.update(screen_scroll)
		w.draw(win)

		spikes_group.update(screen_scroll)
		spikes_group.draw(win)
		health_group.update(screen_scroll)
		health_group.draw(win)
		inflator_group.update(screen_scroll)
		inflator_group.draw(win)
		deflator_group.update(screen_scroll)
		deflator_group.draw(win)
		exit_group.update(screen_scroll)
		exit_group.draw(win)
		checkpoint_group.update(screen_scroll)
		checkpoint_group.draw(win)
		enemy_group.update(screen_scroll)
		enemy_group.draw(win)

		screen_scroll = 0
		p.update(moving_left, moving_right, w, collision_groups)
		p.draw(win)

		if ((p.rect.right >= WIDTH - SCROLL_THRES) and level_scroll < (level_length * 16) - WIDTH) \
				or ((p.rect.left <= SCROLL_THRES) and level_scroll > 0):
				dx = p.dx
				p.rect.x -= dx
				screen_scroll = -dx
				level_scroll += dx

		if len(exit_group) > 0:
			exit = exit_group.sprites()[0]
			if not exit.open:
				if abs(p.rect.x - exit.rect.x) <= 80 and len(health_group) == 0:
					exit.open = True

			if p.rect.colliderect(exit.rect) and exit.index == 11:
				checkpoint = None
				checkpoint_fx.play()
				level += 1
				if level < MAX_LEVEL:
					checkpoint = False
					reset_level = True
					next_level = True
				else:
					checkpoint = None
					win_page = True

		cp = pygame.sprite.spritecollide(p, checkpoint_group, False)
		if cp:
			checkpoint = cp[0]
			if not checkpoint.catched:
				checkpoint_fx.play()
				checkpoint.catched = True
				checkpoint_pos = p.rect.center
				checkpoint_screen_scroll = screen_scroll
				checkpoint_level_scroll = level_scroll

		if pygame.sprite.spritecollide(p, spikes_group, False):
			reset_level = True

		if pygame.sprite.spritecollide(p, health_group, True):
			health += 1
			life_fx.play()

		if pygame.sprite.spritecollide(p, enemy_group, False):
			reset_level = True

		if reset_level:
			if health > 0:
				if next_level:
					world_data, level_length, w = reset_level_data(level)
					p, moving_left, moving_right = reset_player_data(level)
					level_scroll = 0
					health = 3
					checkpoint = None
					next_level = False

				elif checkpoint:
					checkpoint_dx = level_scroll - checkpoint_level_scroll
					w.update(checkpoint_dx)
					for group in objects_groups:
						group.update(checkpoint_dx)
					p.rect.center = checkpoint_pos
					level_scroll = checkpoint_level_scroll

				else:
					w.update(level_scroll)
					for group in objects_groups:
						group.update(level_scroll)
					p, moving_left, moving_right = reset_player_data(level)
					level_scroll = 0

				screen_scroll = 0
				reset_level = False
				health -= 1
			else:
				restart_page = True
				game_page = False
				reset_level = False

		# Drawing info bar
		pygame.draw.rect(win, (25, 25, 25), (0, HEIGHT-20, WIDTH, 20))
		pygame.draw.rect(win, (255, 255,255), (0, 0, WIDTH, WIDTH), 2, border_radius=5)

		win.blit(ball_image, (5, WIDTH + 2))
		health_text.update(f'x{health}', shadow=False)
		current_level_text.update(f'Level {level}', shadow=False)

	clock.tick(FPS)
	pygame.display.update()

pygame.quit()