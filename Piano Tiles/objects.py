import pygame

SCREEN = WIDTH, HEIGHT = 270, 480

class Block(pygame.sprite.Sprite):
	def __init__(self, win, pos):
		super(Block, self).__init__()
		self.win = win
		self.x, self.y = pos
		self.color = (0,0,0)
		self.is_alive = True
		self.game_over = False

		self.rect = pygame.rect.Rect(self.x, self.y, 67.5, 120)

	def update(self, can_move, speed):
		if can_move:
			self.rect.y += speed

			if self.rect.bottom >= HEIGHT and self.is_alive:
				self.color = (255,0,0)
				self.game_over = True

			if self.rect.top >= HEIGHT + 120:
				self.kill()

		shape_surf = pygame.Surface(pygame.Rect(self.rect).size, pygame.SRCALPHA)
		pygame.draw.rect(shape_surf, self.color, shape_surf.get_rect())
		self.win.blit(shape_surf, self.rect)

	def get_pos(self):
		return (self.rect.x, self.rect.y)

class Text(pygame.sprite.Sprite):
	def __init__(self, text, font, pos, win):
		super(Text, self).__init__()
		self.win = win

		self.x,self.y = pos
		self.initial = self.y
		self.image = font.render(text, True, (255, 255, 255))

	def update(self, speed):
		self.y += speed
		if self.y - self.initial >= 100:
			self.kill()

		self.win.blit(self.image, (self.x, self.y))

class Counter(pygame.sprite.Sprite):
	def __init__(self, win, font):
		super(Counter, self).__init__()

		self.win = win
		self.font = font
		self.index = 1
		self.count = 3
		self.image = self.font.render(f'{self.count}', True, (255, 255, 255))

	def update(self):
		if self.index % 30 == 0:
			self.count -= 1

		self.index += 1

		if self.count > 0:
			self.image = self.font.render(f'{self.count}', True, (255, 255, 255))
			self.win.blit(self.image, (WIDTH // 2 - self.image.get_width() / 2,
											  HEIGHT // 2 - self.image.get_height() / 2))


class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()

		self.image = pygame.transform.scale(img, scale)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

	def draw(self, win, image=None):
		if image:
			self.image = image
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