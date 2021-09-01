import pygame

SIZE = WIDTH, HEIGHT = 192, 192

class Ball(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Ball, self).__init__()
		self.x = x
		self.y = y

		self.image = pygame.image.load('Assets/ball.png')
		self.rect = self.image.get_rect(center=(x, y))

		self.jump_height = 15
		self.speed = 3
		self.vel = self.jump_height
		self.mass = 1
		self.gravity = 1

		self.jump = False

	def update(self, moving_left, moving_right):
		self.dx = 0
		self.dy = 0

		if moving_left:
			self.dx = -self.speed
			self.direction = -1
		if moving_right:
			self.dx = self.speed
			self.direction = 1
		if (not moving_left and not moving_right) and not self.jump:
			self.direction = 0
			self.walk_index = 0

		if self.jump:
			F = (1/2) * self.mass * self.vel
			self.dy -= F
			self.vel -= self.gravity

			if self.vel < -15:
				self.vel = self.jump_height
				self.jump = False
		else:
			self.dy += self.vel

		if self.rect.left + self.dx < 0 or self.rect.right + self.dx > WIDTH:
			self.dx = 0

		if self.rect.bottom > 150:
			self.rect.bottom = 150

		self.rect.x += self.dx
		self.rect.y += self.dy

	def draw(self, win):
		win.blit(self.image, self.rect)