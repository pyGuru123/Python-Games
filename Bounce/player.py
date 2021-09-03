import pygame

SIZE = WIDTH, HEIGHT = 192, 192

class Ball(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Ball, self).__init__()
		self.x = x
		self.y = y

		self.original_img = pygame.image.load('Assets/ball.png')
		self.inflated_img = pygame.image.load('Assets/ball2.png')
		self.image = self.original_img
		self.rect = self.image.get_rect(center=(x, y))

		self.jump_height = 15
		self.speed = 3
		self.vel = self.jump_height
		self.mass = 1
		self.gravity = 1

		self.jump = False
		self.fluffy = False

	def inflate(self):
		x, y = self.rect.center
		self.fluffy = True
		self.image = self.inflated_img
		self.rect = self.image.get_rect(center=(x,y))
		self.gravity = 2

	def deflate(self):
		x, y = self.rect.center
		self.fluffy = False
		self.image = self.original_img
		self.rect = self.image.get_rect(center=(x,y))
		self.gravity = 1

	def check_collision(self, dx, dy, world, groups):
		self.size = self.image.get_width()


		for tile in world.water_list:
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				if self.fluffy:
					self.vel = 3
					dy = -self.vel
					self.gravity = 0
				else:
					self.gravity = 2
			else:
				if self.fluffy:
					self.vel = self.jump_height
					self.gravity = 2
					# dy = - (tile[1].top - self.rect.y)

		# Checking collision with walls
		for tile in world.wall_list:
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.size, self.size):
				# left / right collision
				dx = 0
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				# below ground
				if self.vel > 0 and self.vel != self.jump_height:
					dy = tile[1].bottom - self.rect.top
					self.jump = False
				# above ground
				elif self.vel <= 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom

		
		for tile in groups[0]:
			x = self.rect.x
			if tile.rect.x > x:
				delta = -5
			else:
				delta = 5
			if tile.rect.colliderect(x + dx + delta, self.rect.y, self.size, self.size):
				# left / right collision
				dx = 0
				self.inflate()
				self.jump = True
			if tile.rect.colliderect(x, self.rect.bottom + dy, self.size, self.size):
				# above ground
				if self.vel <= 0 or self.vel == self.jump_height:
					dy = tile.rect.top - self.rect.bottom
				self.inflate()
				self.jump = True

		return dx, dy


	def update(self, moving_left, moving_right, world, groups):
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

		if self.rect.top < 0:
			self.vel= -5

		self.dx, self.dy = self.check_collision(self.dx, self.dy, world, groups)

		self.rect.x += self.dx
		self.rect.y += self.dy

	def draw(self, win):
		win.blit(self.image, self.rect)