import pygame

pygame.init()
SCREEN = WIDTH, HEIGHT = 270, 480
win = pygame.display.set_mode(SCREEN)
pygame.display.set_caption('Piano Tiles')

class Block(pygame.sprite.Sprite):
	def __init__(self, win, pos):
		super(Block, self).__init__()
		self.win = win
		self.x, self.y = pos

		self.rect = pygame.rect.Rect(self.x, self.y, 67.5, 120)

	def update(self):
		self.rect.y += 5
		if self.rect.top >= HEIGHT + 120:
			self.kill()
			# print('dead')

		pygame.draw.rect(self.win, (0,0,0), self.rect)