import pygame
import random

from objects import Egg, Basket, Splash, Button, ScoreText, getEggPos, display_score

# Display ***************************************

pygame.init()
SCREEN = WIDTH, HEIGHT = 600, 960
win = pygame.display.set_mode(SCREEN)
xoffset, yoffset = 70, 100
clock = pygame.time.Clock()
FPS = 45

# Colors ***************************************

WHITE = 255, 255, 255
BLACK = 0, 0, 0

# Fonts ****************************************
pygame.font.init()
score_font = pygame.font.Font('Fonts/PatrickHand-Regular.ttf', 50)
score_font2 = pygame.font.SysFont('Arial',40)
score_font3 = pygame.font.Font('Fonts/PatrickHand-Regular.ttf', 80)

# Music ***************************************
pygame.mixer.music.load('Sounds/music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

egg_drop_sound = pygame.mixer.Sound('Sounds/drop.wav')
splash_sound = pygame.mixer.Sound('Sounds/splash.wav')
game_over_sound = pygame.mixer.Sound('Sounds/game_over.wav')

# Objects **************************************

basket = Basket(xoffset + WIDTH // 2, yoffset + HEIGHT - 180, win)

x, y = getEggPos()
e = Egg(x, y, win)
egg_group = pygame.sprite.Group()
egg_group.add(e)

splash_group = pygame.sprite.Group()
score_group = pygame.sprite.Group()

# images **************************************
bg = pygame.image.load('Assets/bg.png')
bg = pygame.transform.scale(bg, (600, 1100))

home = pygame.image.load('Assets/home.jpg')
home = pygame.transform.scale(home, (WIDTH+300, HEIGHT))

hen = pygame.image.load('Assets/hen.png')
hen = pygame.transform.scale(hen, (WIDTH, hen. get_height()))

egg_bucket = pygame.image.load('Assets/egg_bucket.png')

health_egg = pygame.image.load('Assets/egg1.png')
health_egg = pygame.transform.scale(health_egg, (30,40))

leaves = pygame.image.load('Assets/leaves.png')
arrow = pygame.image.load('Assets/arrow.png')
larrow = pygame.transform.scale(arrow, (80,80))
rarrow = pygame.transform.flip(larrow, True, False)

close_img = pygame.image.load('Assets/close.png')
close_img = pygame.transform.scale(close_img, (80,80))
restart_img = pygame.image.load('Assets/restart.png')
restart_img = pygame.transform.scale(restart_img, (80,80))

# Buttons **************************************
left_button = Button(larrow, (1,1), xoffset + 160, yoffset + HEIGHT - 85)
right_button = Button(rarrow, (1,1), xoffset + 360, yoffset + HEIGHT - 85)

restart_button = Button(restart_img, (1,1), xoffset + WIDTH // 2 - close_img.get_width()//2, yoffset + HEIGHT //2)

close_button = Button(close_img, (1,1), xoffset + WIDTH // 2 - close_img.get_width()//2, yoffset + HEIGHT //2 + 90)

# Game Variables ******************************
health = 5
score = 0
speed = 12
gameStarted = False
gameOver = False

# Game ****************************************

running = True
while running:
	win.fill(BLACK)
	win.blit(bg, (xoffset, yoffset), (0, 0, WIDTH, HEIGHT))
	pygame.draw.rect(win, WHITE, (xoffset-10, yoffset-10, WIDTH + 20, HEIGHT + 20), 3)
	
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
	
	if gameOver:
		score_img = score_font3.render(f'Score : {score}', True, (34, 139, 34))
		score_rect = score_img.get_rect()
		win.blit(score_img, (xoffset + WIDTH // 2 - score_img.get_width() // 2, yoffset + HEIGHT // 2 - 140))
		
		win.blit(egg_bucket, (50, yoffset + HEIGHT - 300))
	
		if restart_button.draw(win):
			health = 5
			score = 0
			speed = 12
			gameStarted = True
			gameOver = False

			pygame.mixer.music.play(loops=-1)
			
			x, y = getEggPos()
			e = Egg(x, y, win)
			egg_group.add(e)

		if close_button.draw(win):
			running = False

	else:
		if not gameStarted:
			win.blit(home, (xoffset, yoffset), (250, 0, WIDTH, HEIGHT))
			
			pos = pygame.mouse.get_pos()
			play_rect = pygame.Rect(110, 880, 230, 120)
			if play_rect.collidepoint(pos):
				gameStarted = True
				gameOver = False
	
	if gameStarted:
		win.blit(hen, (xoffset, yoffset+50))
		
		img, rect = display_score(score, score_font2, (xoffset + WIDTH-200, yoffset+10) )
		win.blit(img, rect)
		
		for index in range(health):
			win.blit(health_egg, (xoffset + 10 + 40 * index, yoffset + 15))
			
		win.blit(leaves, (xoffset,265), (0,0,WIDTH, leaves.get_height()))
		
		basket.update()
		egg_group.update(speed)
		splash_group.update()
		score_group.update()
		
		for egg in egg_group:
			collision = False
	
			if egg.rect.y >= yoffset + HEIGHT - 160:
				collision = True
				health -= 1
				splash = Splash(egg.rect.x, egg.rect.y+10, win)
				splash_group.add(splash)
				splash_sound.play()
	
			if basket.check_collision(egg.rect):
				collision = True
				score += 3
				egg_drop_sound.play()
				pos = egg.rect.x, egg.rect.y
				s = ScoreText('+3',  score_font, pos, win)
				score_group.add(s)
			
			if collision:
				egg.kill()
				x, y = getEggPos()
				e = Egg(x, y, win)
				egg_group.add(e)
				
		if health <= 0:
			gameStarted = False
			gameOver = True

			pygame.mixer.music.stop()
			game_over_sound.play()

			egg_group.empty()
			score_group.empty()
			splash_group.empty()
	
		if left_button.draw(win):
				if basket.rect.x >= xoffset:
					basket.rect.x -= 20
		if right_button.draw(win):
				if basket.rect.right <= xoffset + WIDTH:
					basket.rect.x += 20
			
	clock.tick(FPS)
	pygame.display.update()
		
pygame.quit()