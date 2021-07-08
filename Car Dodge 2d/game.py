import pygame

from objects import Background, Player, Enemy, Roadblock, Coin, Counter, Draw

# Setup *****************************************

pygame.init()
SCREEN = WIDTH, HEIGHT = 540, 960
xoffset, yoffset = 60, 50
win = pygame.display.set_mode(SCREEN, pygame.SCALED | pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 45

# Colors ****************************************
BLACK = (0,0,0)
WHITE = (255, 255, 255)

# Fonts ****************************************
pygame.font.init()
score_font = pygame.font.Font('Fonts/PatrickHand-Regular.ttf', 50)
counter_font = pygame.font.Font('Fonts/Alternity-8w7J.ttf', 160)

# Images ***************************************

menu_img = pygame.image.load('Assets/menu.jpeg')
menu_img = pygame.transform.scale(menu_img, (WIDTH + 500, HEIGHT))

start_btn = pygame.image.load('Assets/start.png')

arrows_img = pygame.image.load('Assets/arrows.png')
arrows_img = pygame.transform.scale(arrows_img, (300,200))

coin_img = pygame.image.load('Assets/coin.png')
coin_img = pygame.transform.scale(coin_img, (64, 64))

horn_img = pygame.image.load('Assets/horn.png')
horn_img = pygame.transform.scale(horn_img, (80, 80))

speedometer = pygame.image.load('Assets/speedometer.png')
speedometer = pygame.transform.scale(speedometer, (80, 80))

car_dodged_img = pygame.image.load('Assets/car_dodge.png')
car_dodged_img = pygame.transform.scale(car_dodged_img, (120, 92))

replay_img = pygame.image.load('Assets/replay.png')
replay_img = pygame.transform.scale(replay_img, (300,150))

# Music ***************************************
pygame.mixer.music.load('Sounds/rise-and-shine.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

crash_fx = pygame.mixer.Sound('Sounds/car_crash.wav')
horn_fx = pygame.mixer.Sound('Sounds/car_horn.wav')
coin_fx = pygame.mixer.Sound('Sounds/coin_fx.wav')
speeding_fx = pygame.mixer.Sound('Sounds/speeding_fx.wav')

# Objects ***************************************
bg = Background(win)

p = Player(WIDTH//2 + 50, yoffset + HEIGHT // 2, win)

counter = Counter(win, counter_font) 

draw = Draw(win)

# Object positions *******************************

horn_rect = pygame.Rect(xoffset + WIDTH - 50, yoffset + HEIGHT + 20, 85, 80)

start_rect = start_btn.get_rect()
start_rect.x = xoffset + WIDTH // 5
start_rect.y = yoffset + HEIGHT + 50

replay_rect = replay_img.get_rect()
replay_rect.x = xoffset + WIDTH // 4 + 15
replay_rect.y = yoffset + 150

# Game Variables ********************************

speed = 18
p_speed = 15
coins_collected = 0
car_dodged = 0
main_menu = True
restart_menu = False
crashed = False
ec_crash = False
rb_crash = False

# Game *****************************************

running = True
while running:
	win.fill(BLACK)
	pos = None
	ec_crash = False
	rb_crash = False

	if any(pygame.mouse.get_pressed()):
		pos = pygame.mouse.get_pos()
		
	if main_menu:
		win.blit(menu_img, (xoffset, yoffset), (200,0, xoffset + WIDTH, HEIGHT))
		draw.border()
		
		win.blit(start_btn, start_rect)
		if pos and start_rect.collidepoint(pos):
			main_menu = False
			bg.move = False

	if restart_menu:
		bg.update()
		draw.bottom_black_bar()
		draw.top_black_bar()
		draw.border()
		
		draw.score_box(coin_img, car_dodged_img, speedometer,  coins_collected, car_dodged, speed, score_font)
		if p.rect.bottom <= yoffset + HEIGHT:
			pos = None
			p.rect.y += 10
			p.update(pos, p_speed)
			enemy_group.update(10)
			roadblock_group.update(10)
		else:
			p.update(pos, 0)
			enemy_group.update(0)
			roadblock_group.update(0)
			
			win.blit(replay_img, replay_rect)
			
			if pos and replay_rect.collidepoint(pos):
				counter.count = 3

				speed = 18
				p_speed = 15
				coins_collected = 0
				car_dodged = 0
				main_menu = False
				restart_menu = False
				crashed = False
				ec_crash = False
				rb_crash = False

				p.rect.y = yoffset + HEIGHT // 2
		
	if not restart_menu and not main_menu:
		bg.update()
		draw.top_black_bar()
		draw.replay_black_bar()
		draw.border()
		
		if counter.count >0:
			counter.update()
			if counter.count == 0:
				bg.move = True
				
				e = Enemy(win)
				enemy_group = pygame.sprite.Group()
				enemy_group.add(e)
				
				rb = Roadblock(win)
				roadblock_group = pygame.sprite.Group()
				roadblock_group.add(rb)
				
				coin = Coin(win)
				coin_group = pygame.sprite.Group()
				coin_group.add(coin)
		else:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						running = False
		
			if any(pygame.mouse.get_pressed()):
				pos = pygame.mouse.get_pos()
			p.update(pos, p_speed)
			
			if pos and horn_rect.collidepoint(pos):
				horn_fx.play()
				for enemy in enemy_group:
					elane = enemy.lane
					plane = ((p.rect.x - xoffset + 112) // 93) - 2
					if elane == plane:
						if enemy.rect.y <= p.rect.y:
							if enemy.rect.x >= xoffset + 100 and enemy.rect.x <= xoffset + WIDTH - 115:
								if elane in (0,1):
									move = 10
								elif elane in (2,3):
									move = -10
								enemy.rect.x += move
			
			enemy_group.update(speed)
			roadblock_group.update(speed)
			coin_group.update(speed)
			
			for enemy in enemy_group:
				if enemy.rect.y >= yoffset + HEIGHT + 100:
					enemy.kill()
					e = Enemy(win)
					enemy_group.add(e)
					
					car_dodged += 1
					speed += 2
					
				if p.rect.colliderect(enemy.rect):
					crashed = True
					ec_crash = True

				if enemy.rect.y - 10 <= p.rect.y <= enemy.rect.y + 10:
					speeding_fx.play()
					
			for block in roadblock_group:
				if block.rect.y >= yoffset + HEIGHT + 100:
					block.kill()
					rb = Roadblock(win)
					roadblock_group.add(rb)
					
				if p.rect.colliderect(block.rect):
					crashed = True
					rb_crash = True
		
			for coin in coin_group:
				dead = False
				if coin.rect.y >= yoffset + HEIGHT + 100:
					dead = True
				
				if p.rect.colliderect(coin.rect):
					dead = True
					coins_collected += 1
					coin_fx.play()
		
				if dead:
					coin.kill()
					coin = Coin(win)
					coin_group.add(coin)
					
			draw.top_black_bar()
			draw.bottom_black_bar()
			draw.border()
			draw.controller(arrows_img)
			draw.coin_hud(coin_img)
			draw.car_hud(car_dodged_img)
			draw.horn_hud(speedometer, horn_img)
			draw.update_score(coins_collected, car_dodged, speed, score_font)
						
			if crashed:
				crash_fx.play()
				
				bg.move = False
				coin_group.empty()
				if rb_crash:
					enemy_group.empty()
				if ec_crash:
					roadblock_group.empty()
				
				restart_menu = True
		
		#pygame.draw.rect(win, WHITE, (xoffset+112, yoffset +50, 45, 50))
	
	
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()