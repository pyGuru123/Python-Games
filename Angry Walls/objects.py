import pygame
import random

SCREEN = WIDTH, HEIGHT = 288, 512

pygame.font.init()


class Player:
	def __init__(self, win):
		self.win = win
		
		self.image = pygame.image.load(f"Assets/red.png")
		self.image = pygame.transform.scale(self.image, (44,44))
		self.reset()
		
	def update(self):
		self.win.blit(self.image, self.rect)
		
	def reset(self):
		self.x = 145
		self.y = 270
		self.rect = self.image.get_rect(center=(self.x,self.y))

class Bar(pygame.sprite.Sprite):
	def __init__(self, x, y, width, color, win):
		super(Bar, self).__init__()
		
		self.rect = pygame.Rect(x, y, width, 20, border_radius = 8)
		self.win = win
		self.color = color
		
	def update(self, speed):
		self.rect.y += speed
		if self.rect.y >= HEIGHT:
			self.kill()
		self.win.fill(self.color, self.rect)
		
class Ball(pygame.sprite.Sprite):
	def __init__(self, x, y, type, color, win):
		super(Ball, self).__init__()
		
		self.x = x
		self.y = y
		self.color = color
		self.win = win

		color_dict = {"red" : (255, 0, 0), "white" : (255, 255, 255), "gray" : (54, 69, 79)}
		self.c = color_dict[self.color]
		self.rect = pygame.draw.circle(win, self.c, (x,y), 5)
		
		self.gray = color_dict["gray"]
		
	def update(self, speed):
		self.y += speed
		if self.y >= HEIGHT:
			self.kill()
		
		pygame.draw.circle(self.win, self.gray, (self.x+2, self.y+2), 6)
		self.rect = pygame.draw.circle(self.win, self.c, (self.x,self.y), 6)
		

class Block(pygame.sprite.Sprite):
	def __init__(self, x, y, max, win):
		super(Block, self).__init__()
		
		self.win = win
		self.scale = 1
		self.counter = 0
		self.inc = 1
		self.x = x
		self.y = y
		self.max = max
		
		self.orig = pygame.image.load("Assets/block.jpeg")
		self.image = pygame.transform.scale(self.orig, (self.scale, self.scale))
		self.rect = self.image.get_rect(center=(x,y))
		
	def update(self):
		self.counter += 1
		if self.counter >= 2:
			self.scale += self.inc
			if self.scale <= 0 or self.scale >= self.max:
				self.inc *= -1
			self.image = pygame.transform.scale(self.orig, (self.scale, self.scale))
			self.rect = self.image.get_rect(center= (self.x, self.y))
			
			self.counter = 0
			
		self.win.blit(self.image, self.rect)
		
class ScoreCard:
	def __init__(self, x, y, win):
		self.win = win
		self.size = 50
		self.inc = 1
		self.animate = False
		
		self.style = "Fonts/BubblegumSans-Regular.ttf"
		self.font= pygame.font.Font(self.style, self.size)

		self.image = self.font.render("0", True, (255, 255, 255))
		self.rect = self.image.get_rect(center=(x,y))
		self.shadow_rect = self.image.get_rect(center=(x+3, y+3))
		
	def update(self, score):
		if self.animate:
			self.size += self.inc
			self.font = pygame.font.Font(self.style, self.size)
			if self.size <= 50 or self.size >= 65:
				self.inc *= -1
				
			if self.size == 50:
				self.animate = False
		self.image = self.font.render(f"{score}", False, (255, 255, 255))
		shadow = self.font.render(f"{score}", True,(54, 69, 79) )	
		
		self.win.blit(shadow, self.shadow_rect)
		self.win.blit(self.image, self.rect)
		

class Message:
	def __init__(self, x, y, size, text, font, color, win):
		self.win = win
		if not font:
			self.font = pygame.font.SysFont("Verdana", size)
			anti_alias = True
		else:
			self.font = pygame.font.Font(font, size)
			anti_alias = False
		self.image = self.font.render(text, anti_alias, color)
		self.rect = self.image.get_rect(center=(x,y))
		self.shadow = self.font.render(text, anti_alias, (54,69,79))
		self.shadow_rect = self.image.get_rect(center=(x+2,y+2))
		
	def update(self):
		self.win.blit(self.shadow, self.shadow_rect)
		self.win.blit(self.image, self.rect)
		
		
class Particle(pygame.sprite.Sprite):
	def __init__(self, x, y, size, color, win):
		super(Particle, self).__init__()
		self.x = x
		self.y = y
		self.color = color
		self.win = win
		self.size = random.randint(4,7)
		if size == 0:
			xr = (-1, 2)
			yr = (-2, 2)
			f = 1
			self.life = 60
		elif size == 1:
			xr = (-3,3)
			yr = (-6,6)
			f = 2
			self.life = 60
		elif size == 2:
			xr = (-3,3)
			yr = (-3,3)
			f = 2
			self.life = 40
		self.x_vel = random.randrange(xr[0], xr[1]) * f
		self.y_vel = random.randrange(yr[0], yr[1]) * f
		self.lifetime = 0
			
	def update (self):
		self.size -= 0.1
		self.lifetime += 1
		if self.lifetime <= self.life:
			self.x += self.x_vel
			self.y += self.y_vel
			s = int(self.size)
			pygame.draw.rect(self.win, self.color, (self.x, self.y,s,s))
		else:
			self.kill()
		
		
def generate_particles(p, particles, color, win):
	particle_pos = list(p.rect.center)
	particle_pos[1] += 25
		
	particles.append([particle_pos, [random.randint(0,20) / 10 - 1, -2], random.randint(4,8)])
	for particle in particles:
		particle[0][0] -= particle [1][0]
		particle[0][1] -= particle [1][1]
		particle [2] -= 0.1
		pygame.draw.circle(win, color, particle [0], int(particle [2]))
		#pygame.draw.rect(win, color, (particle[0][0], particle [0][1], int(particle[2]), int(particle[2])))
		if particle [2] <= 0:
			particles.remove(particle)
			
	return particles