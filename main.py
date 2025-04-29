import pygame
from pygame.sprite import Group

from random import randint
import settings

from os.path import join

class Player(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
    self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    self.direction = pygame.Vector2()
    self.speed = 300

  def update(self, dt):
    keys = pygame.key.get_pressed()
    self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    self.direction = self.direction.normalize() if self.direction \
      else self.direction
    self.rect.center += self.direction * self.speed * dt
    recent_keys = pygame.key.get_just_pressed()
    if recent_keys[pygame.K_SPACE]:
      print('fire laser')

class Star(pygame.sprite.Sprite):
  def __init__(self, groups, surf):
    super().__init__(groups)
    self.image = surf
    self.rect = self.image.get_frect(
      center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))


#setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
pygame.display.set_caption('Space Shooter')

surf = pygame.Surface((100,200))
surf.fill('yellow')
x = 100

all_sprites = pygame.sprite.Group()
star_surface = pygame.image.load(join('images', 'star.png')).convert_alpha()
for i in range(20):
  Star(all_sprites, star_surface)
player = Player(all_sprites)


meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft=(20, WINDOW_HEIGHT - 20))
while running:
  dt = clock.tick() / 1000
  #event loop
  for event in pygame.event.get():
    if event.type  == pygame.QUIT:
      running = False
  #updating game
  all_sprites.update(dt)

  #draw game
  screen.fill('blue')
  all_sprites.draw(screen)

  pygame.display.update()
pygame.quit()