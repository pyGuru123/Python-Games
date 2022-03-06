import pygame
import random
from objects import Road, Player, Tree, Button

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

# COLORS **********************************************************************

WHITE = (255, 255, 255)
BLUE = (30, 144,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 20)

# FONTS ***********************************************************************

font1 = pygame.font.SysFont('cursive', 32)

select_car = font1.render('Select Car', True, WHITE)

# IMAGES **********************************************************************

bg = pygame.image.load('Assets/bg.png')

menu_img = pygame.image.load('Assets/home.png')
play_img = pygame.image.load('Assets/play.png')

left_arrow = pygame.image.load('Assets/arrow.png')
right_arrow = pygame.transform.flip(left_arrow, True, False)

cars = []
car_type = 0
for i in range(1, 9):
	img = pygame.image.load(f'Assets/cars/{i}.png')
	img = pygame.transform.scale(img, (59, 101))
	cars.append(img)

# FUNCTIONS *******************************************************************
def center(image):
	return (WIDTH // 2) - image.get_width() // 2

# BUTTONS *********************************************************************
play_btn = Button(play_img, (100, 34), center(play_img)+10, HEIGHT-80)
la_btn = Button(left_arrow, (32, 42), 40, 180)
ra_btn = Button(right_arrow, (32, 42), WIDTH-60, 180)

# OBJECTS *********************************************************************
road = Road()

tree_group = pygame.sprite.Group()

# VARIABLES *******************************************************************
home_page = False
car_page = False
game_page = True

counter = 0
speed = 2.5
p = Player(100, HEIGHT-120, car_type)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

	if home_page:
		win.blit(menu_img, (0,0))
		counter += 1
		if counter % 60 == 0:
			home_page = False
			car_page = True

	if car_page:
		win.fill(BLACK)
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

	if game_page:
		counter += 1
		if counter % 60 == 0:
			t = Tree(random.choice([-5, WIDTH-35]), -20)
			tree_group.add(t)

		win.blit(bg, (0,0))
		road.update(speed)
		road.draw(win)

		p.update(0, 0)
		p.draw(win)

		tree_group.update(speed)
		tree_group.draw(win)

	pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT), 3)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()