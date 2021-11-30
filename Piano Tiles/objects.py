import pygame

SCREEN = WIDTH, HEIGHT = 288, 512
TILE_WIDTH = WIDTH // 4
TILE_HEIGHT = 130

class Tile(pygame.sprite.Sprite):
	def __init__(self, x, y, win):
		super(Tile, self).__init__()

		self.win = win
		self.color = (255,0,0)

		self.surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
		self.rect = self.surface.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, speed):
		self.rect.y += speed
		if self.rect.y >= HEIGHT:
			self.kill()

		pygame.draw.rect(self.surface, self.color, (0,0, TILE_WIDTH, TILE_HEIGHT))
		self.win.blit(self.surface, self.rect)