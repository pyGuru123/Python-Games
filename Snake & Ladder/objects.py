import pygame

pygame.mixer.init()


class Player:
	def __init__(self, num):
		self.num = num

		if self.num == 1:
			self.image = pygame.image.load('Assets/pieces/blue.png').convert_alpha()
		if self.num == 2:
			self.image = pygame.image.load('Assets/pieces/green.png').convert_alpha()
		if self.num == 3:
			self.image = pygame.image.load('Assets/pieces/red.png').convert_alpha()
		if self.num == 4:
			self.image = pygame.image.load('Assets/pieces/yellow.png').convert_alpha()

		self.pos = 1
		self.rect = self.image.get_rect()
		self.update_rect()
		self.first_move = True

		self.snake_dict = {27:5, 40:3, 43:18, 54:31, 66:45, 76:58, 89:53, 99:41}
		self.snakes_at = list(self.snake_dict.keys())

	def move(self, steps):
		if steps:
			if self.first_move:
				self.steps_to_move = steps
				self.first_move = False

			if self.pos + self.steps_to_move <= 100:
				self.pos += 1
				self.update_rect()
				steps -= 1

				return steps
			return 0
		return 0

	def on_snake_ladder(self):
		if self.pos in self.snakes_at:
			self.pos = self.snake_dict[self.pos]
			self.update_rect()

	def update_rect(self):
		row = 9 - ((self.pos - 1) // 10)
		col = (self.pos - 1) % 10
		if row % 2 == 0:
			col = 9 - col
		self.rect.x = col * 61.2 + 380
		self.rect.y = row * 61.2 + 25
