from os.path import join
from random import randint, uniform

import pygame
import settings


class Player(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
    self.rect = self.image.get_frect(center=(settings.WINDOW_WIDTH/2,
                                             settings.WINDOW_HEIGHT/2))
    self.direction = pygame.Vector2()
    self.speed = 300

    #cool down
    self.can_shoot = True
    self.laser_shoot_time = 0
    self.cooldown_duration = 400

  def update(self, dt):
    keys = pygame.key.get_pressed()
    self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    self.direction = self.direction.normalize() if self.direction \
      else self.direction
    self.rect.center += self.direction * self.speed * dt

    recent_keys = pygame.key.get_just_pressed()
    if recent_keys[pygame.K_SPACE] and self.can_shoot:
      Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
      self.can_shoot = False
      self.laser_shoot_time = pygame.time.get_ticks()

    self.laser_timer()

  def laser_timer(self):
    if not self.can_shoot:
      current_time = pygame.time.get_ticks()
      if current_time - self.laser_shoot_time >= self.cooldown_duration:
        self.can_shoot = True

class Star(pygame.sprite.Sprite):
  def __init__(self, groups, surf):
    super().__init__(groups)
    self.image = surf
    self.rect = self.image.get_frect(
      center=(randint(0, settings.WINDOW_WIDTH), randint(0,
                                                         settings.WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
  def __init__(self, surf, pos, groups):
    super().__init__(groups)
    self.image = surf
    self.rect = self.image.get_frect(midbottom = pos)

  def update(self, dt):
    self.rect.centery -= 400 * dt
    if self.rect.bottom < 0:
      self.kill()

class Meteor(pygame.sprite.Sprite):
  def __init__(self, surf, pos, groups):
    super().__init__(groups)
    self.image = surf
    self.rect = self.image.get_frect(center = pos)
    self.start_time = pygame.time.get_ticks()
    self.lifetime = 3000
    self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
    self.speed = randint(400, 500)

  def update(self, dt):
    self.rect.center += self.direction * self.speed * dt
    if self.rect.top > settings.WINDOW_HEIGHT:
      self.kill()

def collisions():
  global running

  all_sprites.update(dt)
  collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True)
  if collision_sprites:
    running = False
  for laser in laser_sprites:
    collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
    if collided_sprites:
      laser.kill()

def display_score():
  current_time = pygame.time.get_ticks() // 100
  text_surface = font.render(str(current_time), True, (240, 240, 240))
  text_rect = text_surface.get_frect(midbottom = (settings.WINDOW_WIDTH/2,
                                                  settings.WINDOW_HEIGHT - 50))
  screen.blit(text_surface, text_rect)
  pygame.draw.rect(screen, (240, 240, 240), text_rect.inflate(20, 16).move
        (0, -8),5, 5)
#setup
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((settings.WINDOW_WIDTH,settings.WINDOW_HEIGHT))
running = True
pygame.display.set_caption('Space Shooter')

#import
star_surface = pygame.image.load(join('images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)


#sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(20):
  Star(all_sprites, star_surface)

player = Player(all_sprites)
#custom events -> Meteor event
meteor_event = pygame.event.custom_type()

pygame.time.set_timer(meteor_event, 500)


test_rect = pygame.FRect(0, 0, 300, 600)


while running:
  dt = clock.tick() / 1000
  #event loop
  for event in pygame.event.get():
    if event.type  == pygame.QUIT:
      running = False
    if event.type == meteor_event:
      x, y = randint(0, settings.WINDOW_WIDTH,), randint(-200, -100)
      Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))

  #updating game
  collisions()

  #draw game
  screen.fill('#1a1f3d')
  display_score()

  all_sprites.draw(screen)

  pygame.display.update()
pygame.quit()