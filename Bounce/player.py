import pygame

SIZE = WIDTH, HEIGHT = 192, 192
TILE_SIZE = 16

class Ball(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Ball, self).__init__()
		self.x = x
		self.y = y

		self.original_img = pygame.image.load('Assets/ball.png')
		self.inflated_img = pygame.image.load('Assets/ball2.png')
		self.image = self.original_img
		self.rect = self.image.get_rect(center=(x, y))
		self.rect.x = x
		self.rect.y = y

		self.jump_height = 15
		self.speed = 3
		self.vel = self.jump_height
		self.mass = 1
		self.gravity = 1

		self.jump = False
		self.fluffy = False
		self.in_water = False

	def inflate(self):
		if not self.fluffy:
			x, y = self.rect.center
			self.image = self.inflated_img
			self.rect = self.image.get_rect(center=(x,y))
			self.fluffy = True

	def deflate(self):
		if self.fluffy:
			x, y = self.rect.center
			self.image = self.original_img
			self.rect = self.image.get_rect(center=(x,y))
			self.vel = self.jump_height
			self.fluffy = False

	def check_collision(self, dx, dy, world, groups):
		self.size = self.image.get_width()
		x = self.rect.x

		# Checking collision with inflator group ***********************************
		for tile in groups[0]:
			if tile.rect.x > x:
				delta = -5
			else:
				delta = 3
			if tile.rect.colliderect(x + dx + delta, self.rect.y, self.size, self.size):
				# left / right collision
				dx = 0
				self.inflate()
			elif tile.rect.colliderect(x, self.rect.bottom + dy, self.size, self.size):
				# above ground
				if self.vel <= 0 or self.vel == self.jump_height:
					dy = tile.rect.top - self.rect.bottom
				self.inflate()

		# Checking collision with deflator group ***********************************
		for tile in groups[1]:
			if tile.rect.colliderect(x + dx, self.rect.y, self.size, self.size):
				# left / right collision
				dx = 0
				self.deflate()
			elif tile.rect.colliderect(x, self.rect.bottom + dy, self.size, self.size):
				if not self.fluffy:
					if self.vel > 0 and self.vel != self.jump_height:
						dy = 0
						self.jump = False
						self.vel = self.jump_height
					elif self.vel <= 0 or self.vel == self.jump_height:
						dy = tile.rect.top - self.rect.bottom
				else:
					dy = 0
					self.deflate()

		# Checking collision with water tiles **************************************

		for tile in world.water_list:
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.size, self.size):
				self.in_water = True
				t = tile
				break

			elif tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				self.in_water = True
				t = tile
				break
		else:
			self.in_water = False

		if self.in_water:
			if self.fluffy:
				dy = (t[1].top - self.rect.bottom) // 8
				self.gravity = 2
			else:
				self.gravity = 2
		else:
			if self.fluffy:
				self.gravity = 2
			else:
				self.gravity = 1


		# Checking collision with ramps ********************************************
		for ramp in world.ramp_list:
			if self.rect.colliderect(ramp.rect):
				rel_x = self.rect.x - ramp.rect.x
				if ramp.type == 1:
					height = TILE_SIZE - rel_x
				elif ramp.type == 2:
					height = rel_x + self.rect.width

				height = min(height, TILE_SIZE)
				height = max(height, 0)

				y = ramp.rect.bottom - height - 2
				self.rect.bottom = y

				dy = 0

		# Checking collision with walls ********************************************
		for tile in world.wall_list:
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.size, self.size):
				# left / right collision
				dx = 0
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				if not self.fluffy:
					# below ground
					if self.vel > 0 and self.vel != self.jump_height:
						dy = 0
						self.jump = False
						self.vel = self.jump_height
					# above ground
					elif self.vel <= 0 or self.vel == self.jump_height:
						dy = tile[1].top - self.rect.bottom
				else:
					dy = 0


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