import pygame

SCREEN = WIDTH, HEIGHT = 288, 512
TILE_WIDTH = WIDTH // 4
TILE_HEIGHT = 130

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 144, 255)
BLUE2 = (2, 239, 239)
PURPLE = (191, 64, 191)

class Tile(pygame.sprite.Sprite):
	def __init__(self, x, y, win):
		super(Tile, self).__init__()

		self.win = win
		self.x, self.y = x, y
		self.color = BLACK

		self.surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
		self.rect = self.surface.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.center = TILE_WIDTH//2, TILE_HEIGHT//2 + 15
		self.line_start = self.center[0], self.center[1]-18
		self.line_end = self.center[0], 20

	def update(self, speed):
		self.rect.y += speed
		if self.rect.y >= HEIGHT:
			self.kill()

		pygame.draw.rect(self.surface, self.color, (0,0, TILE_WIDTH, TILE_HEIGHT))
		pygame.draw.rect(self.surface, WHITE, (0,0, TILE_WIDTH, TILE_HEIGHT), 4)
		pygame.draw.rect(self.surface, BLUE2, (0,0, TILE_WIDTH, TILE_HEIGHT), 2)
		pygame.draw.line(self.surface, BLUE, self.line_start, self.line_end, 3)
		pygame.draw.circle(self.surface, BLUE, self.center, 15, 3)
		self.win.blit(self.surface, self.rect)