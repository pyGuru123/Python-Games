import pygame

WIDTH, HEIGHT = 640, 384

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Player, self).__init__()
		self.x = x
		self.y = y

		self.idle_list = []
		self.walk_left = []
		self.walk_right = []
		self.attack_list = []
		self.death_list = []
		self.hit_list = []

		self.size = 24

		for i in range(1,3):
			image = pygame.image.load(f'Assets/Player/PlayerIdle{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.idle_list.append(image)
		for i in range(1,6):
			image = pygame.image.load(f'Assets/Player/PlayerWalk{i}.png')
			right = pygame.transform.scale(image, (24, 24))
			left = pygame.transform.flip(right, True, False)
			self.walk_right.append(right)
			self.walk_left.append(left)
		for i in range(1, 5):
			image = pygame.image.load(f'Assets/Player/PlayerAttack{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.attack_list.append(image)
		for i in range(1,11):
			image = pygame.image.load(f'Assets/Player/PlayerDead{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.death_list.append(image)
		for i in range(1, 3):
			image = pygame.image.load(f'Assets/Player/PlayerHit{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.hit_list.append(image)

		self.idle_index = 0
		self.walk_index = 0
		self.attack_index = 0
		self.death_index = 0
		self.hit_index = 0
		self.fall_index = 0

		self.jump_height = 15
		self.speed = 3
		self.vel = self.jump_height
		self.mass = 1
		self.gravity = 1

		self.counter = 0
		self.direction = 0

		self.alive = True
		self.attack = False
		self.hit = False
		self.jump = False

		self.grenades = 5
		self.health = 100

		self.image = self.idle_list[self.idle_index]
		self.image = pygame.transform.scale(self.image, (24, 24))
		self.rect = self.image.get_rect(center=(x, y))

	def check_collision(self, world, dx, dy):
		# Checking collision with ground
		for tile in world.ground_list:
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				# above ground
				if self.rect.y + dy <= tile[1].y:
				# if self.vel < 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom
				# print(self.vel, dy)

		# Checking collision with rocks & stones
		for tile in world.rock_list:
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.size, self.size):
				# left / right collision
				dx = 0
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				# below ground
				if self.vel > 0 and self.vel != self.jump_height:
					dy = 0
					self.jump = False
					self.vel = self.jump_height
				# above ground
				elif self.vel <= 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom


		return dx, dy

	def update_animation(self):
		self.counter += 1
		if self.counter % 7 == 0:
			if self.health <= 0:
				self.death_index += 1
				if self.death_index >= len(self.death_list):
					self.alive = False
			else:
				if self.attack:
					self.attack_index += 1
					if self.attack_index >= len(self.attack_list):
						self.attack_index = 0
						self.attack = False
				if self.hit:
					self.hit_index += 1
					if self.hit_index >= len(self.hit_list):
						self.hit_index = 0
						self.hit = False
				if self.direction == 0:
					self.idle_index = (self.idle_index + 1) % len(self.idle_list)			
				if self.direction == -1 or self.direction == 1:
					self.walk_index = (self.walk_index + 1) % len(self.walk_left)
			self.counter = 0

		if self.alive:
			if self.health <= 0:
				self.image = self.death_list[self.death_index]
			elif self.attack:
				self.image = self.attack_list[self.attack_index]
				if self.direction == -1:
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.hit:
				self.image = self.hit_list[self.hit_index]
			elif self.direction == 0:
				self.image = self.idle_list[self.idle_index]
			elif self.direction == -1:
				self.image = self.walk_left[self.walk_index]
			elif self.direction == 1:
				self.image = self.walk_right[self.walk_index]


	def update(self, moving_left, moving_right, world):
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

		self.dx, self.dy = self.check_collision(world, self.dx, self.dy)

		if self.rect.left + self.dx < 0 or self.rect.right + self.dx > WIDTH:
			self.dx = 0

		self.rect.x += self.dx
		self.rect.y += self.dy

		self.update_animation()

		
	def draw(self, win):
		win.blit(self.image, self.rect)
