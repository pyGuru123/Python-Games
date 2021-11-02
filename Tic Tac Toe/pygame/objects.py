import pygame

class Rect():
	def __init__(self, x, y, index):
		self.rect = pygame.Rect(x, y, 70, 70)
		self.index = index
		self.active = True

		self.bgcolor = (32, 33, 36)
		self.color = (255, 255, 255)
		self.text = ''
		self.font = pygame.font.Font('Fonts/PAPYRUS.ttf', 25)
		self.image = self.font.render(self.text, True, self.color)

	def update(self, win):
		if self.active:
			pygame.draw.rect(win, self.color, self.rect, 2, border_radius=5)
		else:
			pygame.draw.rect(win, self.bgcolor, self.rect, border_radius=5)
			pygame.draw.rect(win, self.color, self.rect, 2, border_radius=5)

		self.image = self.font.render(self.text, True, self.color)
		x = self.rect.centerx - self.image.get_width() // 2
		y = self.rect.centery - self.image.get_height() // 2
		win.blit(self.image, (x, y))


def create_board():
	return ['#'] + [' ' for i in range(9)]

def generate_boxes():
	box_list = []
	for i in range(9):
		r = i // 3
		c = i % 3
		x = 20 + 70 * c + 16
		y = 220 + 70 * r + 16
		box = Rect(x, y, i)
		box_list.append(box)

	return box_list