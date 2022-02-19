# Hex Rush

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 12 Feb, 2022

import math
import random
import pygame

from objects import Line, Player, Ball, Particle, Message, Button

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
FPS = 90

# COLORS **********************************************************************

RED = (255,0,0)
GREEN = (0,177,64)
BLUE = (0, 0,255)
ORANGE = (252,76,2)
YELLOW = (254,221,0)
PURPLE = (155,38,182)
AQUA = (0,103,127)
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (239, 237, 238)
GRAY2 = (200, 200, 203)
GRAY3 = (180, 180, 180)

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE]
cindex = 0
ccolor = COLORS[cindex]

# Fonts
score_font = "Fonts/DroneflyRegular-K78LA.ttf"
msg_font = "Fonts/Biondi Sans.ttf"

game_msg = Message(90, HEIGHT//2+20, 30, "GAME", msg_font, BLACK, win)
over_msg = Message(WIDTH//2+60, HEIGHT//2+20, 30, "OVER!", msg_font, RED, win)

cscore_msg = Message(WIDTH//2, 50, 20, "SCORE", msg_font, GRAY3, win)
cscore_msg2 = Message(WIDTH//2, 75, 24, "0", msg_font, BLACK, win)
best_msg = Message(WIDTH//2, 140, 20, "BEST", msg_font, GRAY3, win)
bestscore_msg = Message(WIDTH//2, 170, 24, "0", msg_font, BLACK, win)

hex_msg = Message(WIDTH//2, HEIGHT//2-30, 40, "HEX", msg_font, GRAY3, win)
dash_msg = Message(WIDTH//2, HEIGHT//2+20, 40, "DASH", msg_font, GRAY3, win)

score_msg = Message(WIDTH//2, HEIGHT//2, 60, "0", score_font, GRAY2, win)

# Sounds
score_fx = pygame.mixer.Sound('Sounds/click.wav')
score_fx.set_volume(0.2)
score_page_fx = pygame.mixer.Sound('Sounds/score_page.mp3')
explode_fx = pygame.mixer.Sound('Sounds/explode.wav')

pygame.mixer.music.load('Sounds/music.wav')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.7)

# Buttons
close_img = pygame.image.load('Assets/closeBtn.png')
replay_img = pygame.image.load('Assets/replay.png')
sound_off_img = pygame.image.load("Assets/soundOffBtn.png")
sound_on_img = pygame.image.load("Assets/soundOnBtn.png")

close_btn = Button(close_img, (24, 24), WIDTH // 4 - 18, HEIGHT//2 + 120)
replay_btn = Button(replay_img, (36,36), WIDTH // 2  - 18, HEIGHT//2 + 115)
sound_btn = Button(sound_on_img, (24, 24), WIDTH - WIDTH // 4 - 18, HEIGHT//2 + 120)

# Positons 
left = 100
top = 150
right = WIDTH - left
bottom = HEIGHT- top
mid = HEIGHT // 2

# Groups & Objects
line_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()

topr = Line((left, top), (WIDTH-left, top))
l1 = Line((left-15, top+10), (30, mid-10))
l2 = Line((30, mid+10), (left-15, bottom-10))
r1 = Line((right+15, top+10), (WIDTH-30, mid-10))
r2 = Line((WIDTH-30, mid+10), (right+15, bottom-10))
bottom = Line((left, HEIGHT-top), (WIDTH-left, HEIGHT-top))

line_group.add(topr)
line_group.add(r1)
line_group.add(r2)
line_group.add(bottom)
line_group.add(l2)
line_group.add(l1)

player = Player(WIDTH//2, HEIGHT//2)

# Score Bar
bar_index = random.randint(0,5)
l= line_group.sprites()[bar_index]
bar = Line((l.x1, l.y1), (l.x2, l.y2))

clicked = False
score = 0
high = 0
counter = 0

sound_on = True
gameover = False
home_page = True
game_page = False
score_page = False

color = COLORS[random.randint(0,4)]

running = True
while running:
    if counter % 100 == 0:
    	ball = Ball(win)
    	ball_group.add(ball)
    	counter = 0
    counter += 1
		
    win.fill(GRAY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
        	running = False
        	
        if event.type == pygame.MOUSEBUTTONDOWN:
        	if not clicked and game_page:
        		clicked = True
        		player.di *= -1
        		player.update_index()
        		rect = line_group.sprites()[player.index]
        		
        	if home_page:
        		home_page = False
        		game_page = True
        		
        if event.type == pygame.MOUSEBUTTONUP:
        	clicked = False
        	
    if home_page:
        	line_group.update(win, color)
        	hex_msg.update()
        	dash_msg.update()
        	
    if score_page:
    	cscore_msg.update(shadow=False)
    	cscore_msg2.update(score, shadow=False)
    	best_msg.update(shadow=False)
    	bestscore_msg.update(high, shadow=False)
    	game_msg.update(shadow=False)
    	over_msg.update(shadow=False)
    	
    	if close_btn.draw(win):
    		running = False
    		
    	if replay_btn.draw(win):
    		ball_group.empty()
    		gameover = False
    		score = 0
    		
    		player = Player(WIDTH//2, HEIGHT//2)
    		score_msg = Message(WIDTH//2, HEIGHT//2, 60, "0", score_font, GRAY2, win)
    		
    		game_page = True
    		score_page = False
    		home_page = False
    	if sound_btn.draw(win):
    		sound_on = not sound_on
    		
    		if sound_on:
    			sound_btn.update_image(sound_on_img)
    			pygame.mixer.music.play(loops=-1)
    		else:
    			sound_btn.update_image(sound_off_img)
    			pygame.mixer.music.stop()
    
    # drawing Objects
    if game_page:
	    score_msg.update(score, shadow=True)
	    line_group.update(win)
	    particle_group.update()
	    bar.update(win, ccolor)
	    line = line_group.sprites()[player.index]
	    player.update(line, ccolor, win)
	    ball_group.update(win)
	    
	    # Collison Detection
	    if player.rect.collidepoint(bar.get_center()):
	    	bar_index = random.randint(0,5)
	    	l= line_group.sprites()[bar_index]
	    	bar = Line((l.x1, l.y1), (l.x2, l.y2))
	    	
	    	score_fx.play()
	    	score += 1
	    	if score & score > high:
	    		high = score
	    	if score % 3 == 0:
	    		cindex = (cindex + 1) % 5
	    		ccolor = COLORS[cindex]
	    		
	    for ball in ball_group:
	    	if player.alive and ball.rect.colliderect(player.rect):
	    		x, y = player.rect.centerx, player.rect.centery
	    		for i in range(20):
	    			particle = Particle(x, y, ccolor, win)
	    			particle_group.add(particle)
	    		player.alive = False
	    		ball.kill()
	    		if not gameover:
	    			explode_fx.play()
	    			gameover = True
	    			
	    if gameover and len(particle_group) == 0:
	    		game_page = False
	    		score_page = True
    
    pygame.draw.rect(win, BLUE, (0,0,WIDTH-2, HEIGHT-2), 2)
    
    clock.tick(FPS)
    pygame.display.update()
    
pygame.quit()