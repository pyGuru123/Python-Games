import math
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_UP, MOUSEBUTTONUP

from objects import Dino, Cactus, Cloud, Ptera, GameOptions

### SETUP *********************************************************************
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 700, 420

pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dino')
pygame.mixer.music.load('music/Super_Sigil_Quest_for_the_Celestial_Dinosaur.mp3')
pygame.mixer.music.play(loops=-1)

bg = pygame.image.load('assets/bg1.jpg').convert()
bgX = 0
bgX2 = bg.get_width()

font = pygame.font.Font('freesansbold.ttf', 32)
dodgerblue = (30, 144, 255)
checkpoint_sound = pygame.mixer.Sound("music/checkPoint.wav")

### Objects & Events **********************************************************
ADDCACTUS = pygame.USEREVENT + 1
ADDCLOUD = pygame.USEREVENT + 2
ADDPTERA = pygame.USEREVENT + 3
cactus_time = random.choice([5000,6000,7000])
cloud_time  = 8000
ptera_time = 23000
pygame.time.set_timer(ADDCACTUS, cactus_time)
pygame.time.set_timer(ADDCLOUD, cloud_time)
pygame.time.set_timer(ADDPTERA, ptera_time)

cactus_sprites = pygame.sprite.Group()
cloud_sprites = pygame.sprite.Group()
ptera_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
dinos = pygame.sprite.Group()

game_options = GameOptions()

### Main Game *****************************************************************
if __name__ == '__main__':
	gameUpdating = False
	gameStarted = False
	isDead = False
	gameOver = False

	high_score = 0
	new_score = 0

	running = True
	while running:
		collision = 0

		win.blit(bg,(bgX,0))
		win.blit(bg,(bgX2,0))

		if not gameUpdating:
			score = 0
			mask1, mask2 = None, None
			for event in pygame.event.get():
				if event.type == QUIT:
					running = False
			
				if event.type == MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					mask1 = 504 < pos[0] < 531 and 181 < pos[1] < 206

				if event.type == KEYDOWN:
					mask2 = event.key == K_SPACE or event.key == K_UP

				if mask1 or mask2:
						cactus_sprites.empty()
						cloud_sprites.empty()
						ptera_sprites.empty()
						all_sprites.empty()
						dinos.empty()

						dino = Dino()
						dinos.add(dino)
						gameUpdating = True
						gameStarted = True
						isDead = False
						gameOver = False

						new_score = 0
						score = 0
						speed = -5
						pygame.time.delay(500)

				if event.type == MOUSEBUTTONUP:
					print(pygame.mouse.get_pos())
		else:
			bgX -= 1.8
			bgX2 -= 1.8
			if bgX < bg.get_width() * -1:
				bgX = bg.get_width()
			if bgX2 < bg.get_width() * -1:
				bgX2 = bg.get_width()

		if gameStarted:
			for event in pygame.event.get():
				if event.type == QUIT:
					running = False

				if event.type == ADDCLOUD:
					c = Cloud()
					cloud_sprites.add(c)
					all_sprites.add(c)
				if event.type == ADDCACTUS:
					if len(ptera_sprites) < 1:
						c = Cactus()
						cactus_sprites.add(c)
						all_sprites.add(c)
				if event.type == ADDPTERA:
					t = Ptera()
					ptera_sprites.add(t)
					all_sprites.add(t)

			pressed_keys = pygame.key.get_pressed()
			dinos.update(pressed_keys)

			if gameUpdating:
				cactus_sprites.update(speed)
				cloud_sprites.update(speed)
				ptera_sprites.update(speed)

			for entity in all_sprites:
				win.blit(entity.surf, entity.rect)
			dinos.draw(win)

			if not isDead:
				for entity in cactus_sprites:
					collision = dino.is_collided_with(entity)
					if collision:
						dino.is_dead()
						isDead = True
						gameOver = True
						gameUpdating = False

				for entity in ptera_sprites:
					if pygame.sprite.spritecollideany(dino, ptera_sprites):
						if entity.rect.left < dino.rect.left < entity.rect.right - 20:
							dino.is_dead()
							isDead = True
							gameOver = True
							gameUpdating = False

				score += 0.25
				new_score = math.floor(score)
				if new_score > 0 and new_score % 100 == 0:
					checkpoint_sound.play()
					speed -= 0.5

				if new_score >= high_score:
					high_score = new_score

			text = font.render('Score : ' + str(new_score), 1, dodgerblue)
			win.blit(text, (40, 10))
			text = font.render('High Score : ' + str(high_score), 1, dodgerblue)
			win.blit(text, (420, 10))

			if gameOver:
				win.blit(game_options.game_over, game_options.game_over_rect)
				win.blit(game_options.replay, game_options.replay_rect)

		else:
			win.blit(game_options.dino_wall, game_options.dino_rect)
			win.blit(game_options.dino_run, game_options.dino_run_rect)
			win.blit(game_options.start, game_options.start_rect)

		pygame.display.flip()
		clock.tick(30)

	pygame.quit()