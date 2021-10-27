import pygame

class Rect():
	def __init__(self, x, y, index):
		self.rect = pygame.Rect(x, y, 70, 70)
		self.index = index
		self.active = True

	def update(self, win, color=(255, 255, 255), width=2):
		if self.active:
			pygame.draw.rect(win, color, self.rect, width, border_radius=5)