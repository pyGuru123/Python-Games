import random
import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_SPACE, K_LEFT, K_RIGHT

from objects import Rocket, Asteroid, Bullet, Explosion


### SETUP *********************************************************************
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500

pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Wars')

pygame.mixer.music.load('music/rpg_ambience_-_exploration.ogg')
pygame.mixer.music.play(loops=-1)

gunshot_sound = pygame.mixer.Sound("music/9_mm_gunshot-mike-koenig-123.wav")
explosion_sound = pygame.mixer.Sound("music/explosion.mp3")

font = pygame.font.Font('freesansbold.ttf', 32)
# text = font.render('', True, green, blue)


### Objects & Events **********************************************************
ADDAST1 = pygame.USEREVENT + 1
ADDAST2 = pygame.USEREVENT + 2
ADDAST3 = pygame.USEREVENT + 3
pygame.time.set_timer(ADDAST1, 2000)
pygame.time.set_timer(ADDAST2, 7000)
pygame.time.set_timer(ADDAST3, 18000)

rocket = Rocket(SIZE)

asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(rocket)

backgrounds = [f'assets/background/bg{i}s.png' for i in range(1,5)]
bg = pygame.image.load(random.choice(backgrounds))

### Game **********************************************************************
score = 0
running = True
while running:
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False
			if event.key == K_SPACE:
				pos = rocket.rect[:2]
				bullet = Bullet(pos, rocket.dir, SIZE)
				bullets.add(bullet)
				all_sprites.add(bullet)
				gunshot_sound.play()
			if event.key == K_LEFT:
				rocket.rotate_left()
			if event.key == K_RIGHT:
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
		elif event.type == QUIT:
			running = False


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
		running = False

	for bullet in bullets:
		collision = pygame.sprite.spritecollide(bullet, asteroids, True)
		if collision:
			pos = bullet.rect[:2]
			explosion = Explosion(pos)
			explosions.add(explosion)
			score += 1
			print(score)
			explosion_sound.play()

			bullet.kill()
			bullets.remove(bullet)

	pygame.display.flip()
	clock.tick(30)

pygame.quit()