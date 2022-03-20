import pygame
import random
from objects import Road, Player, Nitro, Tree, Button, \
					Obstacle, Coins, Fuel

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 30

lane_pos = [50, 95, 142, 190]

# COLORS **********************************************************************

WHITE = (255, 255, 255)
BLUE = (30, 144,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 20)

# FONTS ***********************************************************************

font = pygame.font.SysFont('cursive', 32)

select_car = font.render('Select Car', True, WHITE)

# IMAGES **********************************************************************

bg = pygame.image.load('Assets/bg.png')

home_img = pygame.image.load('Assets/home.png')
play_img = pygame.image.load('Assets/buttons/play.png')
end_img = pygame.image.load('Assets/end.jpg')
end_img = pygame.transform.scale(end_img, (WIDTH, HEIGHT))
game_over_img = pygame.image.load('Assets/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (220, 220))
coin_img = pygame.image.load('Assets/coins/1.png')
dodge_img = pygame.image.load('Assets/car_dodge.png')
dodge_img = pygame.transform.scale(dodge_img, (90, 56))

left_arrow = pygame.image.load('Assets/buttons/arrow.png')
right_arrow = pygame.transform.flip(left_arrow, True, False)

cars = []
car_type = 0
for i in range(1, 9):
	img = pygame.image.load(f'Assets/cars/{i}.png')
	img = pygame.transform.scale(img, (59, 101))
	cars.append(img)

nitro_frames = []
nitro_counter = 0
for i in range(6):
	img = pygame.image.load(f'Assets/nitro/{i}.gif')
	img = pygame.transform.flip(img, False, True)
	img = pygame.transform.scale(img, (18, 36))
	nitro_frames.append(img)

# FUNCTIONS *******************************************************************
def center(image):
	return (WIDTH // 2) - image.get_width() // 2

# BUTTONS *********************************************************************
play_btn = Button(play_img, (100, 34), center(play_img)+10, HEIGHT-80)
la_btn = Button(left_arrow, (32, 42), 40, 180)
ra_btn = Button(right_arrow, (32, 42), WIDTH-60, 180)

# OBJECTS *********************************************************************
road = Road()
nitro = Nitro(WIDTH-80, HEIGHT-80)
p = Player(100, HEIGHT-120, car_type)

tree_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
fuel_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

# VARIABLES *******************************************************************
home_page = True
car_page = False
game_page = False
over_page = False

move_left = False
move_right = False
nitro_on = False

counter = 0
counter_inc = 1
speed = 3
dodged = 0
coins = 0
cfuel = 100

running = True
while running:
	win.fill(BLACK)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

			if event.key == pygame.K_LEFT:
				move_left = True

			if event.key == pygame.K_RIGHT:
				move_right = True

			if event.key == pygame.K_n:
				nitro_on = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				move_left = False

			if event.key == pygame.K_RIGHT:
				move_right = False

			if event.key == pygame.K_n:
				nitro_on = False
				speed = 3
				counter_inc = 1

		if event.type == pygame.MOUSEBUTTONDOWN:
			x, y = event.pos

			if nitro.rect.collidepoint((x, y)):
				nitro_on = True
			else:
				if x <= WIDTH // 2:
					move_left = True
				else:
					move_right = True

		if event.type == pygame.MOUSEBUTTONUP:
			move_left = False
			move_right = False
			nitro_on = False
			speed = 3
			counter_inc = 1

	if home_page:
		win.blit(home_img, (0,0))
		counter += 1
		if counter % 60 == 0:
			home_page = False
			car_page = True

	if car_page:
		win.blit(select_car, (center(select_car), 80))

		win.blit(cars[car_type], (WIDTH//2-30, 150))
		if la_btn.draw(win):
			car_type -= 1
			if car_type < 0:
				car_type = len(cars) - 1

		if ra_btn.draw(win):
			car_type += 1
			if car_type >= len(cars):
				car_type = 0

		if play_btn.draw(win):
			car_page = False
			game_page = True

			p = Player(100, HEIGHT-120, car_type)
			counter = 0

	if over_page:
		win.blit(end_img, (0, 0))
		win.blit(game_over_img, (center(game_over_img), 16))

		num_coin_img = font.render(f'{coins}', True, WHITE)
		num_dodge_img = font.render(f'{dodged}', True, WHITE)
		distance_img = font.render(f'Distance : {counter/1000:.2f} km', True, WHITE)

		win.blit(coin_img, (80, 240))
		win.blit(dodge_img, (50, 280))
		win.blit(num_coin_img, (180, 250))
		win.blit(num_dodge_img, (180, 300))
		win.blit(distance_img, (center(distance_img), (350)))

	if game_page:
		win.blit(bg, (0,0))
		road.update(speed)
		road.draw(win)

		counter += counter_inc
		if counter % 60 == 0:
			tree = Tree(random.choice([-5, WIDTH-35]), -20)
			tree_group.add(tree)

		if counter % 270 == 0:
			type = random.choices([1, 2], weights=[6, 4], k=1)[0]
			x = random.choice(lane_pos)+10
			if type == 1:
				count = random.randint(1, 3)
				for i in range(count):
					coin = Coins(x,-100 - (25 * i))
					coin_group.add(coin)
			elif type == 2:
				fuel = Fuel(x, -100)
				fuel_group.add(fuel)
		elif counter % 90 == 0:
			obs = random.choices([1, 2, 3], weights=[6,2,2], k=1)[0]
			obstacle = Obstacle(obs)
			obstacle_group.add(obstacle)

		if nitro_on and nitro.gas > 0:
			x, y = p.rect.centerx - 8, p.rect.bottom - 10
			win.blit(nitro_frames[nitro_counter], (x, y))
			nitro_counter = (nitro_counter + 1) % len(nitro_frames)

			speed = 10
			if counter_inc == 1:
				counter = 0
				counter_inc = 5

		if nitro.gas <= 0:
			speed = 3
			counter_inc = 1

		nitro.update(nitro_on)
		nitro.draw(win)
		obstacle_group.update(speed)
		obstacle_group.draw(win)
		tree_group.update(speed)
		tree_group.draw(win)
		coin_group.update(speed)
		coin_group.draw(win)
		fuel_group.update(speed)
		fuel_group.draw(win)

		p.update(move_left, move_right)
		p.draw(win)

		if cfuel > 0:
			pygame.draw.rect(win, GREEN, (20, 20, cfuel, 15), border_radius=5)
		pygame.draw.rect(win, WHITE, (20, 20, 100, 15), 2, border_radius=5)
		cfuel -= 0.05

		# COLLISION DETECTION & KILLS
		for obstacle in obstacle_group:
			if obstacle.rect.y >= HEIGHT:
				if obstacle.type == 1:
					dodged += 1
				obstacle.kill() 

			if pygame.sprite.collide_mask(p, obstacle):
				pygame.draw.rect(win, RED, p.rect, 1)
				speed = 0

				game_page = False
				over_page = True

		if pygame.sprite.spritecollide(p, coin_group, True):
			coins += 1

		if pygame.sprite.spritecollide(p, fuel_group, True):
			cfuel += 25
			if cfuel >= 100:
				cfuel = 100

	pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT), 3)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()