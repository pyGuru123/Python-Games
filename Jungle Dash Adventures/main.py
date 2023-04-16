import os
import random
import pickle
import pygame
from pygame.locals import *
from pygame import mixer
from pygame.locals import *
import asyncio
import pygbag

class Adventurer:
	def __init__(self, screen, pos, world, groups):
		self.reset(screen, pos, world, groups)

	def update(self, pressed_keys, game_over, level_won, game_won):
		dx = 0
		dy = 0
		walk_cooldown = 3
		col_threshold = 20

		if not game_over and not game_won:
			if (pressed_keys[K_UP] or pressed_keys[K_SPACE]) and not self.jumped and not self.in_air:
				self.vel_y = -15
				jump_fx.play()
				self.jumped = True
			if (pressed_keys[K_UP] or pressed_keys[K_SPACE]) == False:
				self.jumped = False
			if pressed_keys[K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1
			if pressed_keys[K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1

			if pressed_keys[K_LEFT] == False and pressed_keys[K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				self.image = self.img_right[self.index]

				if self.direction == 1:
					self.image = self.img_right[self.index]
				elif self.direction == -1:
					self.image = self.img_left[self.index]

			if self.counter > walk_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.img_right):
					self.index = 0

				if self.direction == 1:
					self.image = self.img_right[self.index]
				elif self.direction == -1:
					self.image = self.img_left[self.index]

			# add gravity
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			# check for colision
			self.in_air = True
			for tile in self.world.tile_list:
				# check for collision in x direction
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0

				# check for collision in y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					# check if below the ground
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False

			if pygame.sprite.spritecollide(self, self.groups[0], False):
				game_over = True
			if pygame.sprite.spritecollide(self, self.groups[1], False):
				game_over = True
			if pygame.sprite.spritecollide(self, self.groups[4], False):
				game_over = True

			# temp = self
			# temp = temp.rect.x + 20
			# if pygame.sprite.spritecollide(temp, self.groups[5], False):
			# 	level_won = True
			for gate in self.groups[5]:
				if gate.rect.colliderect(self.rect.x - tile_size // 2, self.rect.y, self.width, self.height):
					level_won = True

			if game_over:
				dead_fx.play()

			# check for collision with moving platform
			for platform in self.groups[6]:
				# collision in x direction
				if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0

				# collision in y direction
				if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					# check if below platform
					if abs((self.rect.top + dy) - platform.rect.bottom) < col_threshold:
						self.vel_y = 0
						dy = (platform.rect.bottom - self.rect.top)

					# check if above platform
					elif abs((self.rect.bottom + dy) - platform.rect.top) < col_threshold:
						self.rect.bottom = platform.rect.top - 1
						self.in_air = False
						dy = 0
					# move sideways with the platform
					if platform.move_x:
						self.rect.x += platform.move_direction

			for bridge in self.groups[7]:
				# collision in x direction
				if (bridge.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) and
						(bridge.rect.bottom < self.rect.bottom + 5)):
					dx = 0

				# collision in y direction
				if bridge.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					if abs((self.rect.top + dy) - bridge.rect.bottom) < col_threshold:
						self.vel_y = 0
						dy = (bridge.rect.bottom - self.rect.top)

					# check if above platform
					elif abs((self.rect.bottom + dy) - bridge.rect.bottom) < 8:
						self.rect.bottom = bridge.rect.bottom - 12
						self.in_air = False
						dy = 0

			# updating player position
			self.rect.x += dx
			self.rect.y += dy
			# if self.rect.x == self.width:
			# 	self.rect.x = self.width
			if self.rect.x >= WIDTH - self.width:
				self.rect.x = WIDTH - self.width
			if self.rect.x <= 0:
				self.rect.x = 0


		elif game_over:
			self.image = dead_img
			if self.rect.top > 0:
				self.rect.y -= 5

			self.win.blit(game_over_img, game_over_rect)

		# displaying player on window
		self.win.blit(self.image, self.rect)
		# pygame.draw.rect(self.win, (255, 255, 255), self.rect, 1)

		return game_over, level_won

	def reset(self, win, pos, world, groups):
		x, y = pos
		self.win = win
		self.world = world
		self.groups = groups

		self.img_right = []
		self.img_left = []
		self.index = 0
		self.counter = 0

		for i in range(6):
			img = pygame.image.load(f'player/walk{i + 1}.png')
			img_right = pygame.transform.scale(img, (45, 70))
			img_left = pygame.transform.flip(img_right, True, False)
			self.img_right.append(img_right)
			self.img_left.append(img_left)

		self.image = self.img_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.direction = 1
		self.vel_y = 0
		self.jumping = False
		self.in_air = True


class World:
	def __init__(self, screen, data, groups):
		self.tile_list = []
		self.win = screen
		self.groups = groups

		tiles = []
		for t in sorted(os.listdir('tiles/'), key=lambda s: int(s[:-4])):
			tile = pygame.image.load('tiles/' + t)
			tiles.append(tile)

		row_count = 0
		for row in data:
			col_count = 0
			for col in row:
				if col > 0:
					if col in range(1, 14) or col == 18:
						# dirt blocks
						img = pygame.transform.scale(tiles[col - 1], (tile_size, tile_size))
						rect = img.get_rect()
						rect.x = col_count * tile_size
						rect.y = row_count * tile_size
						tile = (img, rect)
						self.tile_list.append(tile)

					if col == 14:
						# bush
						bush = Forest('bush', col_count * tile_size, row_count * tile_size + tile_size // 2)
						self.groups[2].add(bush)

					if col == 15:
						# lava
						lava = Fluid('lava_flow', col_count * tile_size, row_count * tile_size + tile_size // 2)
						self.groups[1].add(lava)
					if col == 16:
						lava = Fluid('lava_still', col_count * tile_size, row_count * tile_size)
						self.groups[1].add(lava)

					if col == 17:
						# diamond
						diamond = Diamond(col_count * tile_size, row_count * tile_size)
						self.groups[3].add(diamond)
					if col == 19:
						# water block
						water = Fluid('water_flow', col_count * tile_size, row_count * tile_size + tile_size // 2)
						self.groups[1].add(water)
					if col == 20:
						# water block
						water = Fluid('water_still', col_count * tile_size, row_count * tile_size)
						self.groups[1].add(water)
					if col == 21:
						# tree
						tree = Forest('tree', (col_count - 1) * tile_size + 10, (row_count - 2) * tile_size + 5)
						self.groups[2].add(tree)
					if col == 22:
						# mushroom
						mushroom = Forest('mushroom', col_count * tile_size, row_count * tile_size + tile_size // 4)
						self.groups[2].add(mushroom)
					if col == 23:
						# bee
						bee = Bee(col_count * tile_size, row_count * tile_size)
						self.groups[4].add(bee)
					if col == 24:
						# Gate blocks
						gate = ExitGate(col_count * tile_size - tile_size // 4, row_count * tile_size - tile_size // 4)
						self.groups[5].add(gate)
					if col == 25:
						# Side moving platform
						platform = MovingPlatform('side', col_count * tile_size, row_count * tile_size)
						self.groups[6].add(platform)
					if col == 26:
						# top moving platform
						platform = MovingPlatform('up', col_count * tile_size, row_count * tile_size)
						self.groups[6].add(platform)
					if col == 27:
						# flower
						flower = Forest('flower', (col_count) * tile_size, row_count * tile_size)
						self.groups[2].add(flower)
					if col == 28:
						# bridge
						bridge = Bridge((col_count - 2) * tile_size + 10, row_count * tile_size + tile_size // 4)
						self.groups[7].add(bridge)
					if col == 29:
						# Slime
						slime = Slime(col_count * tile_size - 10, row_count * tile_size + tile_size // 4)
						self.groups[4].add(slime)

				col_count += 1
			row_count += 1

			diamond = Diamond((WIDTH // tile_size - 3) * tile_size, tile_size // 2)
			self.groups[3].add(diamond)

	def draw(self):
		for tile in self.tile_list:
			self.win.blit(tile[0], tile[1])


class MovingPlatform(pygame.sprite.Sprite):
	def __init__(self, type_, x, y):
		super(MovingPlatform, self).__init__()

		img = pygame.image.load('assets/moving.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		direction = random.choice([-1, 1])
		self.move_direction = direction
		self.move_counter = 0
		self.move_x = 0
		self.move_y = 0

		if type_ == 'side':
			self.move_x = 1
		elif type_ == 'up':
			self.move_y = 1

	def update(self):
		self.rect.x += self.move_direction * self.move_x
		self.rect.y += self.move_direction * self.move_y
		self.move_counter += 1
		if abs(self.move_counter) >= 50:
			self.move_direction *= -1
			self.move_counter *= -1


class Bridge(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Bridge, self).__init__()

		img = pygame.image.load('tiles/28.png')
		self.image = pygame.transform.scale(img, (5 * tile_size + 20, tile_size))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Fluid(pygame.sprite.Sprite):
	def __init__(self, type_, x, y):
		super(Fluid, self).__init__()

		if type_ == 'water_flow':
			img = pygame.image.load('tiles/19.png')
			self.image = pygame.transform.scale(img, (tile_size, tile_size // 2 + tile_size // 4))
		if type_ == 'water_still':
			img = pygame.image.load('tiles/20.png')
			self.image = pygame.transform.scale(img, (tile_size, tile_size))
		elif type_ == 'lava_flow':
			img = pygame.image.load('tiles/15.png')
			self.image = pygame.transform.scale(img, (tile_size, tile_size // 2 + tile_size // 4))
		elif type_ == 'lava_still':
			img = pygame.image.load('tiles/16.png')
			self.image = pygame.transform.scale(img, (tile_size, tile_size))

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class ExitGate(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(ExitGate, self).__init__()

		img_list = [f'assets/gate{i + 1}.png' for i in range(4)]
		self.gate_open = pygame.image.load('assets/gate5.png')
		self.image = pygame.image.load(random.choice(img_list))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()

	def update(self, player):
		if player.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
			self.image = self.gate_open


class Forest(pygame.sprite.Sprite):
	def __init__(self, type_, x, y):
		super(Forest, self).__init__()

		if type_ == 'bush':
			img = pygame.image.load('tiles/14.png')
			self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 0.50)))

		if type_ == 'tree':
			img = pygame.image.load('tiles/21.png')
			self.image = pygame.transform.scale(img, (3 * tile_size, 3 * tile_size))

		if type_ == 'mushroom':
			img = pygame.image.load('tiles/22.png')
			self.image = pygame.transform.scale(img, (int(tile_size * 0.80), int(tile_size * 0.80)))

		if type_ == 'flower':
			img = pygame.image.load('tiles/27.png')
			self.image = pygame.transform.scale(img, (2 * tile_size, tile_size))

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Diamond(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Diamond, self).__init__()

		img_list = [f'assets/d{i + 1}.png' for i in range(4)]
		img = pygame.image.load(random.choice(img_list))
		self.image = pygame.transform.scale(img, (tile_size, tile_size))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Bee(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Bee, self).__init__()

		img = pygame.image.load('tiles/23.png')
		self.img_left = pygame.transform.scale(img, (48, 48))
		self.img_right = pygame.transform.flip(self.img_left, True, False)
		self.image = self.img_left
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.pos = self.rect.y
		self.dx = 3

	def update(self, player):
		if self.rect.x >= player.rect.x:
			self.image = self.img_left
		else:
			self.image = self.img_right

		if self.rect.y >= self.pos:
			self.dx *= -1
		if self.rect.y <= self.pos - tile_size * 3:
			self.dx *= -1

		self.rect.y += self.dx


class Slime(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Slime, self).__init__()

		img = pygame.image.load('tiles/29.png')
		self.img_left = pygame.transform.scale(img, (int(1.2 * tile_size), tile_size // 2 + tile_size // 4))
		self.img_right = pygame.transform.flip(self.img_left, True, False)
		self.imlist = [self.img_left, self.img_right]
		self.index = 0

		self.image = self.imlist[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.move_direction = -1
		self.move_counter = 0

	def update(self, player):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) >= 50:
			self.index = (self.index + 1) % 2
			self.image = self.imlist[self.index]
			self.move_direction *= -1
			self.move_counter *= -1


class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()

		self.image = pygame.transform.scale(img, scale)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

	def draw(self, win):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False

		win.blit(self.image, self.rect)
		return action


# -------------------------------------------------------------------------------------------------
#											 Custom Functions
def draw_lines(win):
	for row in range(HEIGHT // tile_size + 1):
		pygame.draw.line(win, WHITE, (0, tile_size * row), (WIDTH, tile_size * row), 2)
	for col in range(WIDTH // tile_size):
		pygame.draw.line(win, WHITE, (tile_size * col, 0), (tile_size * col, HEIGHT), 2)


def load_level(level):
	game_level = f'levels/level{level}_data'
	data = None
	if os.path.exists(game_level):
		f = open(game_level, 'rb')
		data = pickle.load(f)
		f.close()

	return data


def draw_text(win, text, pos):
	img = score_font.render(text, True, BLUE)
	win.blit(img, pos)

def reset_level(level):
	global cur_score
	cur_score = 0

	data = load_level(level)
	if data:
		for group in groups:
			group.empty()
		world = World(win, data, groups)
		player.reset(win, player_pos, world, groups)
# 10, 340
	return world

# Window setup
SIZE = WIDTH, HEIGHT = 1000, 650
tile_size = 50

pygame.init()
win = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Jungle Adventure')
clock = pygame.time.Clock()
FPS = 30

pygame.font.init()
score_font = pygame.font.SysFont('Bauhaus 93', 30)

WHITE = (255, 255, 255)
BLUE = (30, 144, 255)

# load sounds
mixer.init()

pygame.mixer.music.load('sounds/Ballad for Olivia.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)

diamond_fx = pygame.mixer.Sound('sounds/341695__projectsu012__coins-1.wav')
diamond_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('sounds/jump.wav')
jump_fx.set_volume(0.5)
dead_fx = pygame.mixer.Sound('sounds/406113__daleonfire__dead.wav')
dead_fx.set_volume(0.5)
sounds = [diamond_fx, ]

# loading images
dead_img = pygame.image.load('assets/ghost.png')
game_over_img = pygame.image.load('assets/gover.png')
game_over_img = pygame.transform.scale(game_over_img, (300, 250))
game_over_rect = game_over_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - HEIGHT // 6))

# background images
bg1 = pygame.image.load('assets/BG1.png')
bg2 = pygame.image.load('assets/BG2.png')
bg = bg1
sun = pygame.image.load('assets/sun.png')
logo = pygame.image.load('assets/logo.png')
you_won = pygame.image.load('assets/won.png')

# loading level 1
level = 1
max_level = len(os.listdir('levels/'))
data = load_level(level)

player_pos = (10, 340)

# creating world & objects
water_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
forest_group = pygame.sprite.Group()
diamond_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
bridge_group = pygame.sprite.Group()
groups = [water_group, lava_group, forest_group, diamond_group, enemies_group, exit_group, platform_group,
		  bridge_group]
world = World(win, data, groups)
player = Adventurer(win, player_pos, world, groups)

# creating buttons
play = pygame.image.load('assets/play.png')
replay = pygame.image.load('assets/replay.png')
home = pygame.image.load('assets/home.png')
exit = pygame.image.load('assets/exit.png')
setting = pygame.image.load('assets/setting.png')

play_btn = Button(play, (128, 64), WIDTH // 2 - WIDTH // 16, HEIGHT // 2)
replay_btn = Button(replay, (45, 42), WIDTH // 2 - 110, HEIGHT // 2 + 20)
home_btn = Button(home, (45, 42), WIDTH // 2 - 20, HEIGHT // 2 + 20)
exit_btn = Button(exit, (45, 42), WIDTH // 2 + 70, HEIGHT // 2 + 20)


score = 0
cur_score = 0
main_menu = True
game_over = False
level_won = False
game_won = False
running = True
async def run():

    # Use global variables inside the coroutine
    global score, cur_score, main_menu, game_over, level_won, game_won, running, bg, level, world

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        pressed_keys = pygame.key.get_pressed()

        # displaying background & sun image
        win.blit(bg, (0, 0))
        win.blit(sun, (40, 40))
        world.draw()
        for group in groups:
            group.draw(win)

        # drawing grid
        # draw_lines(win)

        if main_menu:
            win.blit(logo, (WIDTH // 2 - WIDTH // 8, HEIGHT // 4))

            play_game = play_btn.draw(win)
            if play_game:
                main_menu = False
                game_over = False
                game_won = False
                score = 0

        else:

            if not game_over and not game_won:

                enemies_group.update(player)
                platform_group.update()
                exit_group.update(player)
                if pygame.sprite.spritecollide(player, diamond_group, True):
                    sounds[0].play()
                    cur_score += 1
                    score += 1
                draw_text(win, f'{score}', ((WIDTH // tile_size - 2) * tile_size, tile_size // 2 + 10))

            game_over, level_won = player.update(pressed_keys, game_over, level_won, game_won)

            if game_over and not game_won:
                replay = replay_btn.draw(win)
                home = home_btn.draw(win)
                exit = exit_btn.draw(win)

                if replay:
                    score -= cur_score
                    world = reset_level(level)
                    game_over = False
                if home:
                    game_over = True
                    main_menu = True
                    bg = bg1
                    level = 1
                    world = reset_level(level)
                if exit:
                    running = False

            if level_won:
                if level <= max_level:
                    level += 1
                    game_level = f'levels/level{level}_data'
                    if os.path.exists(game_level):
                        data = []
                        world = reset_level(level)
                        level_won = False
                        score += cur_score

                    bg = random.choice([bg1, bg2])
                else:
                    game_won = True
                    bg = bg1
                    win.blit(you_won, (WIDTH // 4, HEIGHT // 4))
                    home = home_btn.draw(win)

                    if home:
                        game_over = True
                        main_menu = True
                        level_won = False
                        level = 1
                        world = reset_level(level)

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(run())

