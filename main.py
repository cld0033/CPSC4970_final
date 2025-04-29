import pygame
from pygame.sprite import Group

from random import randint
import settings

from os.path import join

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


#importing an image
player_surface = pygame.image.load(join('images', 'player.png')).convert_alpha()
player_rect = player_surface.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
player_direction = pygame.math.Vector2()
player_speed = 300

star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
star_positions = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i
                  in range(20)]
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
    # if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
    #   print('left')
    # if event.type == pygame.MOUSEMOTION:
    #   player_rect.center = event.pos

  #input
  # print(pygame.mouse.get_rel())
  keys = pygame.key.get_pressed()
  player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
  player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
  player_rect.center += player_direction * player_speed * dt


  #draw game
  screen.fill('blue')
  for pos in star_positions:
    screen.blit(star_surf, pos)

  screen.blit(meteor_surf, meteor_rect)
  screen.blit(laser_surf, laser_rect)
  screen.blit(player_surface, player_rect)

  screen.blit(player_surface, player_rect)

  pygame.display.update()
pygame.quit()