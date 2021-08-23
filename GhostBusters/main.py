import pygame

from world import World, load_level
from player import Player
from enemies import Ghost
from particles import Trail
from projectiles import Bullet, Grenade
from button import Button
from texts import Text, Message, BlinkingText, MessageBox

pygame.init()

WIDTH, HEIGHT = 640, 384
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
TILE_SIZE = 16

clock = pygame.time.Clock()
FPS = 30

# IMAGES **********************************************************************

BG1 = pygame.transform.scale(pygame.image.load('assets/BG1.png'), (WIDTH, HEIGHT))
BG2 = pygame.transform.scale(pygame.image.load('assets/BG2.png'), (WIDTH, HEIGHT))
BG3 = pygame.transform.scale(pygame.image.load('assets/BG3.png'), (WIDTH, HEIGHT))
MOON = pygame.transform.scale(pygame.image.load('assets/moon.png'), (300, 220))

# FONTS ***********************************************************************

title_font = "Fonts/Aladin-Regular.ttf"
instructions_font = 'Fonts/BubblegumSans-Regular.ttf'
# about_font = 'Fonts/DalelandsUncialBold-82zA.ttf'

ghostbusters = Message(WIDTH//2, HEIGHT//2 - 80, 90, "GhostBusters", title_font, (255, 255, 255), win)

t = Text(instructions_font, 18)
font_color = (12, 12, 12)
play = t.render('Play', font_color)
about = t.render('About', font_color)
controls = t.render('Controls', font_color)
exit = t.render('Exit', font_color)
main_menu = t.render('Main Menu', font_color)

about_font = pygame.font.SysFont('Verdana', 16)
with open('Data/about.txt') as f:
	info = f.read().replace('\n', ' ')

# BUTTONS *********************************************************************

ButtonBG = pygame.image.load('Assets/ButtonBG.png')
bwidth = ButtonBG.get_width()

play_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2, ButtonBG, 0.5, play)
about_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 30, ButtonBG, 0.5, about)
controls_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 60, ButtonBG, 0.5, controls)
exit_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 90, ButtonBG, 0.5, exit)
main_menu_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 120, ButtonBG, 0.5, main_menu)

# GROUPS **********************************************************************

trail_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
diamond_group = pygame.sprite.Group()
potion_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

objects_group = [water_group, diamond_group, potion_group, enemy_group, exit_group]

# LEVEL VARIABLES **************************************************************

ROWS = 24
COLS = 40
SCROLL_THRES = 200

level = 1
level_length = 0
screen_scroll = 0
bg_scroll = 0
dx = 0

# RESET ***********************************************************************

def reset_level():
	trail_group.empty()
	bullet_group.empty()
	grenade_group.empty()
	explosion_group.empty()
	enemy_group.empty()
	water_group.empty()
	diamond_group.empty()
	potion_group.empty()
	exit_group.empty()

	# LOAD LEVEL WORLD

	world_data, level_length = load_level(level)
	w = World(objects_group)
	w.generate_world(world_data, win)

	return world_data, level_length, w

def reset_player():
	p = Player(250, 50)
	moving_left = False
	moving_right = False

	return p, moving_left, moving_right

# MAIN GAME *******************************************************************

main_menu = True
about_page = False
controls_page = False
game_start = False
running = True
while running:
	win.fill((0,0,0))
	for x in range(5):
		win.blit(BG1, ((x*WIDTH) - bg_scroll * 0.6, 0))
		win.blit(BG2, ((x*WIDTH) - bg_scroll * 0.7, 0))
		win.blit(BG3, ((x*WIDTH) - bg_scroll * 0.8, 0))

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
			if event.key == pygame.K_SPACE:
				x, y = p.rect.center
				direction = p.direction
				bullet = Bullet(x, y, direction, (240, 240, 240), 1, win)
				bullet_group.add(bullet)

				p.attack = True
			if event.key == pygame.K_g:
				if p.grenades:
					p.grenades -= 1
					grenade = Grenade(p.rect.centerx, p.rect.centery, p.direction, win)
					grenade_group.add(grenade)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				moving_left = False
			if event.key == pygame.K_RIGHT:
				moving_right = False

	if main_menu:
		ghostbusters.update()

		if play_btn.draw(win):
			world_data, level_length, w = reset_level()
			p, moving_left, moving_right = reset_player()

			game_start = True
			main_menu = False

		if about_btn.draw(win):
			about_page = True
			main_menu = False

		if controls_btn.draw(win):
			controls_page = True
			main_menu = False

		if exit_btn.draw(win):
			running = False

	if about_page:
		MessageBox(win, about_font, 'GhostBusters', info)
		if main_menu_btn.draw(win):
			about_page = False
			game_start = False
			main_menu = True

			
	if game_start:
		win.blit(MOON, (-40, -10))
		w.draw_world(win, screen_scroll)

		# Updating Objects ********************************************************

		bullet_group.update(screen_scroll, w)
		grenade_group.update(screen_scroll, p, enemy_group, explosion_group, w)
		explosion_group.update(screen_scroll)
		trail_group.update()
		water_group.update(screen_scroll)
		water_group.draw(win)
		diamond_group.update(screen_scroll)
		diamond_group.draw(win)
		potion_group.update(screen_scroll)
		potion_group.draw(win)
		exit_group.update(screen_scroll)
		exit_group.draw(win)

		enemy_group.update(screen_scroll, bullet_group, p)
		enemy_group.draw(win)

		if p.jump:
			t = Trail(p, (220, 220, 220), win)
			trail_group.add(t)

		screen_scroll = 0
		p.update(moving_left, moving_right, w)
		p.draw(win)

		if (p.rect.right >= WIDTH - SCROLL_THRES and bg_scroll < (level_length*TILE_SIZE) - WIDTH) \
			or (p.rect.left <= SCROLL_THRES and bg_scroll > abs(dx)):
			dx = p.dx
			p.rect.x -= dx
			screen_scroll = -dx
			bg_scroll -= screen_scroll


		# Collision Detetction ****************************************************

		if p.rect.bottom > HEIGHT:
			p.health = 0

		if pygame.sprite.spritecollide(p, water_group, False):
			p.health = 0

		if pygame.sprite.spritecollide(p, diamond_group, True):
			pass

		if pygame.sprite.spritecollide(p, exit_group, False):
			level += 1

		potion = pygame.sprite.spritecollide(p, potion_group, False)
		if potion:
			if p.health < 100:
				potion[0].kill()
				p.health += 15
				if p.health > 100:
					p.health = 100


		for bullet in bullet_group:
			enemy =  pygame.sprite.spritecollide(bullet, enemy_group, False)
			if enemy and bullet.type == 1:
				if not enemy[0].hit:
					enemy[0].hit = True
					enemy[0].health -= 50
				bullet.kill()
			if bullet.rect.colliderect(p):
				if bullet.type == 2:
					if not p.hit:
						p.hit = True
						p.health -= 20
						print(p.health)
					bullet.kill()

		# drawing variables *******************************************************

		if p.alive:
			color = (0, 255, 0)
			if p.health <= 40:
				color = (255, 0, 0)
			pygame.draw.rect(win, color, (6, 8, p.health, 20), border_radius=10)
		pygame.draw.rect(win, (255, 255, 255), (6, 8, 100, 20), 2, border_radius=10)

		for i in range(p.grenades):
			pygame.draw.circle(win, (200, 200, 200), (20 + 15*i, 40), 5)
			pygame.draw.circle(win, (255, 50, 50), (20 + 15*i, 40), 4)
			pygame.draw.circle(win, (0, 0, 0), (20 + 15*i, 40), 1)
		
		if p.health <= 0:
			world_data, level_length, w = reset_level()
			p, moving_left, moving_right = reset_player() 

			screen_scroll = 0
			bg_scroll = 0

			main_menu = True
			about_page = False
			controls_page = False
			game_start = False

	pygame.draw.rect(win, (255, 255,255), (0, 0, WIDTH, HEIGHT), 4, border_radius=10)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()