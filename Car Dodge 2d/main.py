import pygame
from objects import Background, Player, Button

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

menu_img = pygame.image.load('Assets/home.png')
start_img = pygame.image.load('Assets/start.png')
start_img = pygame.transform.scale(start_img, (120, 40))

left_arrow = pygame.image.load('Assets/arrow1.png')
right_arrow = pygame.transform.flip(left_arrow, True, False)
la_btn = Button(left_arrow, (32, 42), 40, 180)
ra_btn = Button(right_arrow, (32, 42), WIDTH-60, 180)

road_img = pygame.image.load('Assets/road.png')
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

cars = []
car_type = 0
for i in range(1, 8):
	img = pygame.image.load(f'Assets/cars/{i}.png')
	cars.append(img)

bg = Background()

def center(image):
	return (WIDTH // 2) - image.get_width() // 2

home_page = True
car_page = False
game_page = False

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
		win.blit(start_img, (WIDTH- start_img.get_width()+10, HEIGHT-180))

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

	if game_page:
		bg.update(2.5)
		bg.draw(win)

		win.blit(cars[6], (100, HEIGHT-100))

	pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT), 2)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()