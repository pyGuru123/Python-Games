import pygame
import pickle

from objects import World, load_level, Button, Player, Portal, game_data

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
win = pygame.display.set_mode(SCREEN, pygame.SCALED | pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 45

tile_size = 16

# Images

bg = pygame.image.load("Assets/bg.png")

cave_story = pygame.transform.rotate(pygame.image.load("Assets/cave_story.png"), -90)
cave_story = pygame.transform.scale(cave_story, (150,300))

game_won_img = pygame.transform.rotate(pygame.image.load("Assets/win.png"), -90)
game_won_img = pygame.transform.scale(game_won_img, (150,300))

# Sounds
pygame.mixer.music.load('Sounds/goodbyte_sad-rpg-town.mp3')
pygame.mixer.music.play(loops=-1)

replay_fx =  pygame.mixer.Sound('Sounds/replay.wav')

# Buttons

move_btn = pygame.image.load("Assets/movement.jpeg")
move_btn = pygame.transform.rotate(move_btn, -90)
move_btn = pygame.transform.scale(move_btn, (42, HEIGHT))

play_img = pygame.transform.rotate(pygame.image.load("Assets/play.png"), -90)
play_btn = Button(play_img, (60, 150), 30, 170)

quit_img = pygame.transform.rotate(pygame.image.load("Assets/quit.png"), -90)
quit_btn = Button(quit_img, (60, 150), 140, 170)

replay_img = pygame.transform.rotate(pygame.image.load("Assets/replay.png"), -90)
replay_btn = Button(replay_img, (40, 40), 100, 190)

sound_off_img = pygame.transform.rotate(pygame.image.load("Assets/sound_off.png"), -90)
sound_on_img = pygame.transform.rotate(pygame.image.load("Assets/sound_on.png"), -90)
sound_btn = Button(sound_on_img, (40, 40), 100, 260)

# Variables

current_level = 1
MAX_LEVEL = 3
show_keys = True
pressed_keys = [False, False, False, False]

dir_dict = {
	'Up' : pygame.Rect(5, 27, 35, 50),
	'Down' : pygame.Rect(5, 160, 35, 50),
	'Left' :  pygame.Rect(5, 320, 35, 50),
	'Right' : pygame.Rect(5, 450, 35, 50)
}

# groups 
diamond_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
plant_group = pygame.sprite.Group()
board_group = pygame.sprite.Group()
chain_group = pygame.sprite.Group()
groups = [diamond_group, spike_group, plant_group, board_group, chain_group]

data = load_level(current_level)
(player_x, player_y), (portal_x, portal_y) = game_data(current_level)

world = World(win, data, groups)
player = Player(win, (player_x,player_y), world, groups)
portal = Portal(portal_x, portal_y, win)

game_started = False
game_over = False
game_won = False
replay_menu = False
sound_on = True

bgx = 0
bgcounter = 0
bgdx = 1

running = True
while running:
	win.blit(bg, (bgx, 0))
	for group in groups:
		group.draw(win)
	world.draw()
		
	if not game_started:
		win.blit(cave_story, (100,100))
		if play_btn.draw(win):
			game_started = True
	elif game_won:
		win.blit(game_won_img, (100,100))
	else:
		if show_keys:
			win.blit(move_btn, (0,0))
			bgcounter += 1
			if bgcounter >= 15:
				bgcounter = 0
				bgx += bgdx
				if bgx < 0 or bgx >5 :
					bgdx *= -1
			
	#	for rect in dir_dict:
	#		pygame.draw.rect(win, (255, 0, 0), dir_dict[rect])
			
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = event.pos
				if show_keys:
					if dir_dict["Up"].collidepoint(pos):
						pressed_keys[0] = True
					if dir_dict["Down"].collidepoint(pos):
						pressed_keys[1] = True
					if dir_dict["Left"].collidepoint(pos):
						pressed_keys[2] = True
					if dir_dict["Right"].collidepoint(pos):
						pressed_keys[3] = True
					
			if event.type == pygame.MOUSEBUTTONUP:
				pressed_keys = [False, False, False, False]
				
		portal.update()
				
		if not game_over:
			game_over = player.update(pressed_keys, game_over)
			if game_over:
				show_keys = False
				replay_menu = True
			
		if player.rect.colliderect(portal) and player.rect.top > portal.rect.top and player.rect.bottom < portal.rect.bottom:
			if current_level < MAX_LEVEL:
				current_level += 1
				for group in groups:
					group.empty()
					
				data = load_level(current_level)
				(player_x, player_y), (portal_x, portal_y) = game_data(current_level)
				
				world = World(win, data, groups)
				player = Player(win, (player_x,player_y), world, groups)
				portal = Portal(portal_x, portal_y, win)
			else:
				show_keys = False
				game_won = True
			
		if replay_menu:
			if quit_btn.draw(win):
				running = False
				
			if sound_btn.draw(win):
				sound_on = not sound_on
				
				if sound_on:
					sound_btn.update_image(sound_on_img)
					pygame.mixer.music.play(loops=-1)
				else:
					sound_btn.update_image(sound_off_img)
					pygame.mixer.music.stop()
				
			if replay_btn.draw(win):
				show_keys = True
				replay_menu = False
				game_over = False
				replay_fx.play()
				
				for group in groups:
					group.empty()
					
				data = load_level(current_level)
				(player_x, player_y), (portal_x, portal_y) = game_data(current_level)
				
				world = World(win, data, groups)
				player = Player(win, (player_x,player_y), world, groups)
				portal = Portal(portal_x, portal_y, win)
				
	clock.tick(FPS)
	pygame.display.update()
			
pygame.quit()