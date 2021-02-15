import random
import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_SPACE, K_q, K_e

from objects import Rocket, Asteroid, Bullet, Explosion


### SETUP *********************************************************************
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500

pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Asteroids')

gunshot_sound = pygame.mixer.Sound("music/laser.wav")
explosion_sound = pygame.mixer.Sound("music/explosion.mp3")

font = pygame.font.Font('freesansbold.ttf', 32)
# text = font.render('', True, green, blue)


### Objects & Events **********************************************************
ADDAST1 = pygame.USEREVENT + 1
ADDAST2 = pygame.USEREVENT + 2
ADDAST3 = pygame.USEREVENT + 3
ADDAST4 = pygame.USEREVENT + 4
ADDAST5 = pygame.USEREVENT + 5
pygame.time.set_timer(ADDAST1, 2000)
pygame.time.set_timer(ADDAST2, 6000)
pygame.time.set_timer(ADDAST3, 10000)
pygame.time.set_timer(ADDAST4, 15000)
pygame.time.set_timer(ADDAST5, 20000)

rocket = Rocket(SIZE)

asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(rocket)

backgrounds = [f'assets/background/bg{i}s.png' for i in range(1,5)]
bg = pygame.image.load(random.choice(backgrounds))

startbg = pygame.image.load('assets/start.jpg')

### Game **********************************************************************
if __name__ == '__main__':
	score = 0
	running = True
	gameStarted = False
	musicStarted = False
	while running:
		if not gameStarted:
			if not musicStarted:
				pygame.mixer.music.load('music/Apoxode_-_Electric_1.mp3')
				pygame.mixer.music.play(loops=-1)
				musicStarted = True
			for event in pygame.event.get():
				if event.type == QUIT:
					running = False

				if event.type == KEYDOWN:
					if event.key == K_SPACE:
						gameStarted = True
						musicStarted = False

				win.blit(startbg, (0,0))		
		else:
			if not musicStarted:
				pygame.mixer.music.load('music/rpg_ambience_-_exploration.ogg')
				pygame.mixer.music.play(loops=-1)
				musicStarted = True
			for event in pygame.event.get():
				if event.type == QUIT:
					running = False

				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						running = False
					if event.key == K_SPACE:
						pos = rocket.rect[:2]
						bullet = Bullet(pos, rocket.dir, SIZE)
						bullets.add(bullet)
						all_sprites.add(bullet)
						gunshot_sound.play()
					if event.key == K_q:
						rocket.rotate_left()
					if event.key == K_e:
						rocket.rotate_right()

				elif event.type == ADDAST1:
					ast = Asteroid(1, SIZE)
					asteroids.add(ast)
					all_sprites.add(ast)
				elif event.type == ADDAST2:
					ast = Asteroid(2, SIZE)
					asteroids.add(ast)
					all_sprites.add(ast)
				elif event.type == ADDAST3:
					ast = Asteroid(3, SIZE)
					asteroids.add(ast)
					all_sprites.add(ast)
				elif event.type == ADDAST4:
					ast = Asteroid(4, SIZE)
					asteroids.add(ast)
					all_sprites.add(ast)
				elif event.type == ADDAST5:
					ast = Asteroid(5, SIZE)
					asteroids.add(ast)
					all_sprites.add(ast)


			pressed_keys = pygame.key.get_pressed()
			rocket.update(pressed_keys)

			asteroids.update()
			bullets.update()
			explosions.update()

			win.blit(bg, (0,0))
			explosions.draw(win)

			for sprite in all_sprites:
				win.blit(sprite.surf, sprite.rect)
			win.blit(rocket.surf, rocket.rect)

			if pygame.sprite.spritecollideany(rocket, asteroids):
				rocket.kill()
				score = 0
				for sprite in all_sprites:
					sprite.kill()
				all_sprites.empty()
				rocket = Rocket(SIZE)
				all_sprites.add(rocket)
				gameStarted = False
				musicStarted = False

			for bullet in bullets:
				collision = pygame.sprite.spritecollide(bullet, asteroids, True)
				if collision:
					pos = bullet.rect[:2]
					explosion = Explosion(pos)
					explosions.add(explosion)
					score += 1
					explosion_sound.play()

					bullet.kill()
					bullets.remove(bullet)

			text = font.render('Score : ' + str(score), 1, (200,255,0))
			win.blit(text, (340, 10))

		pygame.display.flip()
		clock.tick(30)

	pygame.quit()