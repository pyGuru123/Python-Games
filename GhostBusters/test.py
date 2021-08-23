import pygame, sys
#from pygame.locals import * # PEP8: `import *` is not preferred

# --- constants ---

WINDOW_SIZE = (1200, 800)

# --- classes --- # PEP8: all classes before main part

class Player(pygame.sprite.Sprite):
                        # PEP8: empty line before method
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self)  # Python 2 & 3
        super().__init__() # only Python 3
        
        self.image = pygame.Surface((8, 8))
        self.image.fill((255, 0, 255))

        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.bottom = 50
        
        self.is_jump = False   # PEP8: `lower_case_names` for variables
        self.jump_count = 5    # PEP8: `lower_case_names` for variables
        
        self.movement = pygame.math.Vector2(0, 0)
        self.speed = pygame.math.Vector2(0, 0)

        self.moving_right = False
        self.moving_left = False
        self.vertical_momentum = 0
        self.air_timer = 0

    def update(self):
        self.speed.x = 0
        #self.rect.x += self.speed.x

    def draw(self, screen, offset):
        screen.blit(self.image, self.rect.move(-offset))
        
class Mob(pygame.sprite.Sprite):
    
    def __init__(self,x,y):
        #pygame.sprite.Sprite.__init__(self)  # Python 2 & 3
        super().__init__() # only Python 3

        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = y
        self.rect.bottom = x
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10
        if keystate[pygame.K_SPACE]:
            self.speedy = -30
        self.rect.x += 0
        self.rect.y += 0
        
    def draw(self, screen, offset):
        screen.blit(self.image, self.rect.move(-offset))
        
#def load_map(path):
 #   f = open(path + '.txt', 'r')
  #  data = f.read()
   # f.close()
    #data = data.split('\n')
   # game_map = []
   # for row in data:
    #    game_map.append(list(row))
   # return game_map

class Map():
    
    def __init__(self, game_map):
        self.game_map = game_map
        
        #self.grass_img = pygame.image.load('data/pictures/Purple_grass.png')
        #self.dirt_img = pygame.image.load('data/pictures/purple_tile.png')

        self.grass_img = pygame.surface.Surface((8,8))
        self.grass_img.fill((0, 255, 0))
                            
        self.dirt_img = pygame.surface.Surface((8,8))
        self.dirt_img.fill((255, 64, 64))

        # - you can calculate it only once -

        self.tile_rects = []

        for y, layer in enumerate(self.game_map):
            for x, tile in enumerate(layer):
                if tile != '0':
                    self.tile_rects.append(pygame.Rect(x*8, y*8, 8, 8))

    def draw(self, screen, offset):
        
        for y, layer in enumerate(self.game_map):
            for x, tile in enumerate(layer):
                if tile == '1':
                    display.blit(self.dirt_img, (x*8 - offset.x, y*8 - offset.y))
                elif tile == '2':
                    display.blit(self.grass_img, (x*8 - offset.x, y*8 - offset.y))
        
# --- functions --- # PEP8: all functions before main part

def collision_test(rect, tiles):
    hit_list = []
    
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
            
    return hit_list

def move(player, map_game):
    
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False} # PEP8: spaces
    
    player.rect.x += player.movement.x
    
    hit_list = collision_test(player.rect, map_game.tile_rects)
    
    for tile in hit_list:
        if player.movement.x > 0:
            player.rect.right = tile.left
            collision_types['right'] = True
            break
        elif player.movement.x < 0:
            player.rect.left = tile.right
            collision_types['left'] = True
            break
            
    player.rect.y += player.movement.y
    
    hit_list = collision_test(player.rect, map_game.tile_rects)
    
    for tile in hit_list:
        if player.movement.y > 0:
            player.rect.bottom = tile.top
            collision_types['bottom'] = True
            break
        elif player.movement.y < 0:
            player.rect.top = tile.bottom
            collision_types['top'] = True
            break
            
    return collision_types

# --- main ---

#ame_map = load_map('data/pictures/map')
game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
            ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]


# - init -

pygame.init()
pygame.display.set_caption('Pygame Platformer')

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32) # initiate the window

display = pygame.Surface((150, 100)) # used as the surface for rendering, which is scaled

scroll = pygame.math.Vector2(0, 0)

map_data = Map(game_map)
player = Player()
mobs = [Mob(10, 10), Mob(50, 50)]

all_sprites = pygame.sprite.Group()
all_sprites.add(player, mobs)

# - main loop -

clock = pygame.time.Clock()

while True:

    # - all updates -
    #all_sprites.update()

    player.movement.update(0, 0)
    
    if player.moving_right == True:
        player.movement.x += 1
            
    if player.moving_left == True:
        player.movement.x -= 1
        
    player.movement.y += player.vertical_momentum
    
    player.vertical_momentum += 0.3
    if player.vertical_momentum > 3:
        player.vertical_momentum = 3

    collisions = move(player, map_data)

    if collisions['bottom'] == True:
        player.air_timer = 0
        player.jump_count = 0
        player.vertical_momentum = 0
    else:
        player.air_timer += 1

        
    for mob in mobs:
        if pygame.sprite.collide_rect(player, mob):
            #mob.image.fill((255,0,255))
            mobs.pop(mobs.index(mob))
            print("collide")
            all_sprites.remove(mob)
        else:
            mob.image.fill((255,255,0))

    # - all draws -

    # scroll
    scroll.update(player.rect.centerx - 75, player.rect.centery - 50)

    offset = pygame.math.Vector2(int(scroll.x), int(scroll.y))

    display.fill((146, 244, 255))  # PEP8: spaces after `,`

    map_data.draw(display, offset)
    
    for item in all_sprites:
        item.draw(display, offset)

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()

    clock.tick(60)
    
    # - all events -

    for event in pygame.event.get(): # event loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.moving_right = True
            if event.key == pygame.K_LEFT:
                player.moving_left = True
            if event.key == pygame.K_SPACE:
                if player.air_timer < 6:
                    player.vertical_momentum = -5
                    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.moving_right = False
            if event.key == pygame.K_LEFT:
                player.moving_left = False
                