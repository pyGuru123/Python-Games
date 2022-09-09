import pygame
import random

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 60

# COLORS **********************************************************************

WHITE = (255, 255, 255)
BLUE = (30, 144,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (168, 169, 169)

# FONTS *************************************************************************

alpha = pygame.font.SysFont("cursive", 21)
hindi = pygame.font.Font("Fonts/Akshar Unicode.ttf", 18)

msg = alpha.render("Guess the word using the hint below", True, BLUE)

# IMAGES ***********************************************************************

img_list = []
for i in range(7):
	img = pygame.image.load(f"Assets/hangman{i}.png")
	img = pygame.transform.scale(img, (100, 103))
	img_list.append(img)
	
hangman_logo = pygame.image.load("hangman_top.png")
hangman_logo = pygame.transform.scale(hangman_logo, (WIDTH-69, 128))
	
# SOUNDS ***********************************************************************

win_fx = pygame.mixer.Sound("Sounds/win.wav")
lose_fx = pygame.mixer.Sound("Sounds/lose.wav")

# DATA **************************************************************************

word_dict = {}
word_list = []
with open("words.txt") as file:
	for line in file.readlines():
		w, m = line.strip().split(":")
		word_dict[w.strip()] = m.strip()

def getWord():
	word = random.choice(list(word_dict.keys()))
	if word in word_list:
		return getWord()
	else:
		meaning = word_dict[word]
		return word.upper(), meaning
		
word, meaning = getWord()
word_list.append(word)
guessed = ['' for i in range(len(word))]
	
# OBJECTS **********************************************************************

class FadeScreen:
	def __init__(self, w, h, color):
		self.surface = pygame.Surface((w, h))
		self.surface.fill(color)
		self.alpha = 255
		self.surface.set_alpha(self.alpha)
		
	def update(self):
		self.alpha -= 0.8
		self.surface.set_alpha(self.alpha)
		
	def draw(self, x, y):
		win.blit(self.surface, (x,y))

class Button(pygame.sprite.Sprite):
	def __init__(self, text, x, y):
		super(Button, self).__init__()
		
		self.text = text
		self.image = alpha.render(self.text, True, WHITE)
		self.rect = pygame.Rect(x, y, 30, 30)
		self.clicked = False
		
	def collision(self, pos):
		if pos and not self.clicked:
			if self.rect.collidepoint(pos):
				self.image = alpha.render(self.text, True, GREEN)
				self.clicked = True
				return True, self.text
		return False
		
	def update(self):
		pygame.draw.rect(win, WHITE, self.rect, 2)
		win.blit(self.image, (self.rect.centerx - self.image.get_width() // 2, self.rect.centery - self.image.get_height() // 2))
		
	def reset(self):
		self.clicked = False
		self.image = alpha.render(self.text, True, WHITE)
		
btns = []
for i in range(26):
	text = f"{chr(65+i)}"
	x = 20 + ( i % 7 ) * 36
	y = 330 + (i // 7) * 36
	btns.append(Button(text, x, y))
	
restart_img = alpha.render("RESTART", True, WHITE)
quit_img = alpha.render("QUIT", True, WHITE)

restart_rect = restart_img.get_rect()
restart_rect.x = WIDTH// 2 + restart_img.get_width() // 2 + 30
restart_rect.y = 180

quit_rect = quit_img.get_rect()
quit_rect.x = WIDTH// 2 + quit_img.get_width() // 2 + 60
quit_rect.y = 210

# GAME ************************************************************************

lives = 6
score = 0
gameover = False
homepage = True

fadeScreen = FadeScreen(WIDTH, HEIGHT, GRAY)

score_img = alpha.render(f"Score : {score}", True, WHITE)
lives_img = alpha.render(f"Lives : {lives}", True, WHITE)

running = True
while running:
	pos = None
	win.fill((0,0,0))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False
				
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			
	if homepage:
		if fadeScreen.alpha >= 0:
			fadeScreen.update()
			fadeScreen.draw(0,0)
			
			hangman_logo.set_alpha(fadeScreen.alpha)
			win.blit(hangman_logo, (WIDTH//2 - hangman_logo.get_width() // 2, HEIGHT//2 - hangman_logo.get_height() // 2))
			
		else:
			homepage = False
		
	else:
		win.fill(GRAY)
		
		# render hangman images
		pygame.draw.rect(win, (20,20,20), (0, 0, WIDTH, 90))
		pygame.draw.rect(win, BLUE, (0, 0, WIDTH, 90), 2)
		pygame.draw.rect(win, (20,20,20), (0, HEIGHT//2 + 30, WIDTH, HEIGHT))
		pygame.draw.rect(win, BLUE, (0, HEIGHT//2 + 30, WIDTH, HEIGHT), 2)
		
		image = img_list[6-lives]
		win.blit(image, (WIDTH // 2 - image.get_width() // 2 - 60, HEIGHT // 2 - image.get_height() // 2 - 100))
		
		win.blit(score_img, (WIDTH// 2 + score_img.get_width() // 2 + 30, 110))
		win.blit(lives_img, (WIDTH// 2 + lives_img.get_width() // 2 + 30, 130))
	
		# render buttons
		for btn in btns:
			btn.update()
			collision = btn.collision(pos) 
			if collision and not gameover:
				if collision[1] in word:
					for i in range(len(word)):
						if word[i] == collision[1]:
							guessed[i] = collision[1]
							
					if guessed.count('') == 0:
						word, meaning = getWord()
						guessed = ['' for i in range(len(word))]
						word_list.append(word)
						win_fx.play()
						score += 1
						
						score_img = alpha.render(f"Score : {score}", True, WHITE)
						
						for btn in btns:
							btn.reset()
						break
				else:
					lives -= 1
					lives_img = alpha.render(f"Lives : {lives}", True, WHITE)
					if lives == 0:
						gameover = True
						lose_fx.play()
					
		# Render Dash and Characters
		for i in range(len(word)):
			x = WIDTH // 2 - ((18 * len(word)) // 2)
			x1, y1 = (x + 20 * i,HEIGHT // 2)
			x2, y2 = (x + 20 * i + 15, HEIGHT // 2)
			pygame.draw.line(win, (0,0,0), (x1, y1), (x2, y2), 2)
			
			if not gameover:
				char = alpha.render(guessed[i], True, WHITE)
			else:
				char = alpha.render(word[i], True, BLUE)
			win.blit(char, (x1 + 3, y1 - 15))
					
		# Render Top message and Hints
		hint = hindi.render(meaning, True, WHITE)
		win.blit(hint, (WIDTH // 2 - hint.get_width() // 2,50))
		win.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 25))
		
		if gameover:
			win.blit(restart_img, restart_rect)
			win.blit(quit_img, quit_rect)
			
			pygame.draw.rect(win, RED, (restart_rect.x - 5, restart_rect.y - 5, 75, 23), 2)
			pygame.draw.rect(win, RED, (quit_rect.x - 5, quit_rect.y - 5, 45, 23), 2)
			
			if pos and restart_rect.collidepoint(*pos):
				score = 0
				lives = 6
				gameover = False
				
				word, meaning = getWord()
				guessed = ['' for i in range(len(word))]
				word_list = []
				word_list.append(word)
				
				for btn in btns:
					btn.reset()
					
				score_img = alpha.render(f"Score : {score}", True, WHITE)
				lives_img = alpha.render(f"Lives : {lives}", True, WHITE)
				
			if pos and quit_rect.collidepoint(*pos):
				running = False
				
	pygame.draw.rect(win, BLUE, (0,0,WIDTH,HEIGHT), 3)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()
