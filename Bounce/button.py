import pygame 

class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()
		
		self.scale = scale
		self.image = img
		if self.scale:
			self.image = pygame.transform.scale(img, (self.scale[0], self.scale[1]))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

	def update_image(self, img):
		self.image = img
		if self.scale:
			self.image = pygame.transform.scale(img, (self.scale[0], self.scale[1]))

	def draw(self, win):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False

		win.blit(self.image, self.rect)
		return action

class LevelButton(Button):
	def __init__(self, img, scale, x, y, text=None, xoff=None, yoff=None):
		super(LevelButton, self).__init__(img, scale, x, y)
		self.text = text
		self.xoff = xoff
		self.yoff = yoff

		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.unlocked = False

		if self.text:
			if not self.xoff:
				self.xoff = self.text.get_width() // 2
			self.yoff = self.text.get_height() // 2

	def draw(self, win):
		action = False
		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		win.blit(self.image, (self.rect.x, self.rect.y))
		if self.text:
			self.image.blit(self.text, (self.width//2 - self.xoff, self.height//2 - self.yoff))

		return action