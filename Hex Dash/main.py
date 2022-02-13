# Hex Rush

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 12 Feb, 2022

import math
import random
import pygame

from objects import Line, Player, Ball, Particle, Message

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
GRAY = (218, 218, 218)

COLORS = [RED, GREEN, BLUE, PURPLE]
cindex = 0
ccolor = COLORS[cindex]

# Fonts
score_font = "Fonts/DroneflyRegular-K78LA.ttf"
score_msg = Message(WIDTH//2, HEIGHT//2, 60, "0", score_font, (60, 60, 60), win)

# Sounds
score_fx = pygame.mixer.Sound('Sounds/click.wav')
score_fx.set_volume(0.2)
score_page_fx = pygame.mixer.Sound('Sounds/score_page.mp3')
explode_fx = pygame.mixer.Sound('Sounds/explode.wav')

pygame.mixer.music.load('Sounds/music.wav')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.7)

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
counter = 0
gameover = False

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
        	if not clicked:
        		clicked = True
        		player.di *= -1
        		player.update_index()
        		rect = line_group.sprites()[player.index]
        		
        if event.type == pygame.MOUSEBUTTONUP:
        	clicked = False
    
    # drawing Objects
    score_msg.update(score)
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
    	if score % 3 == 0:
    		cindex = (cindex + 1) % 3
    		ccolor = COLORS[cindex]
    		
    for ball in ball_group:
    	if player.alive and ball.rect.colliderect(player.rect):
    		x, y = player.rect.centerx, player.rect.centery
    		for i in range(20):
    			particle = Particle(x, y, ccolor, win)
    			particle_group.add(particle)
    			gameover = True
    		player.alive = False
    		ball.kill()
    		explode_fx.play()
    			
    if gameover and len(particle_group) == 0:
    		running = False
    
    pygame.draw.rect(win, BLUE, (0,0,WIDTH-2, HEIGHT-2), 2)
    
    clock.tick(FPS)
    pygame.display.update()
    
pygame.quit()