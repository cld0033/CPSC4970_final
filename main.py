from os.path import join
from random import randint, uniform

import pygame
import settings


class Player(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.original_image =  pygame.image.load(join('images',
                                        'Ship_2_D_Small.png')).convert_alpha()
    self.image = self.original_image
    self.rect = self.image.get_frect(center=(settings.WINDOW_WIDTH/2,
                                             settings.WINDOW_HEIGHT/2))
    self.direction = pygame.Vector2()
    self.pos = pygame.Vector2(self.rect.center)
    self.speed = 500

    #rotaion
    self.angle = 0

    #cool down
    self.can_shoot = True
    self.laser_shoot_time = 0
    self.cooldown_duration = 400

    #mask
    self.mask = pygame.mask.from_surface(self.image)
    self.rotation = 0


  def update(self, dt):
    keys = pygame.key.get_pressed()
    self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    self.direction = self.direction.normalize() if self.direction \
      else self.direction
    # self.rect.center += self.direction * self.speed * dt
    # Move
    if self.direction.length() > 0:
      self.pos += self.direction * self.speed * dt
      self.angle = self.direction.angle_to(
        pygame.Vector2(0, -1))  # Up is 0 degrees

    # Rotate image
    rotated_image = pygame.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_frect(center=self.pos)
    self.image = rotated_image

    recent_keys = pygame.key.get_just_pressed()
    if recent_keys[pygame.K_SPACE] and self.can_shoot:
      Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
      self.can_shoot = False
      self.laser_shoot_time = pygame.time.get_ticks()
      laser_sound.play()

    self.laser_timer()

  def shoot_laser(self):
    radians = math.radians(-self.angle)
    laser_offset = pygame.Vector2(0, -50)
    laser_position = self.pos + laser_offset.rotate(self.angle)
    Laser(laser_surf, laser_position, laser_sprites)

  def laser_timer(self):
    if not self.can_shoot:
      current_time = pygame.time.get_ticks()
      if current_time - self.laser_shoot_time >= self.cooldown_duration:
        self.can_shoot = True

class EnemyShip(pygame.sprite.Sprite):
  def __init__(self, surf, pos, player, groups):
    super().__init__(groups)
    self.original_image = surf
    self.image = self.original_image
    self.rect = self.image.get_frect(center = pos)
    self.player = player # reference to player object

    self.speed = 50
    self.pos = pygame.Vector2(pos)
    self.direction = pygame.Vector2()

    self.calculate_direction()

  def calculate_direction(self):
        """Calculate normalized direction vector toward the player."""
        player_vector = pygame.Vector2(self.player.rect.center)
        self.direction = (player_vector - self.pos).normalize()

        # Calculate angle for rotation (in degrees)
        angle = -self.direction.angle_to(pygame.Vector2(0, -1))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_frect(center=self.pos)

  def update(self, dt):
    # Update direction toward current player position
    player_vector = pygame.Vector2(self.player.rect.center)
    self.direction = (player_vector - self.pos).normalize()

    # Move toward the player
    self.pos += self.direction * self.speed * dt
    self.rect.center = self.pos

    # Rotate to face the player
    angle = -self.direction.angle_to(pygame.Vector2(0, -1))  # Up is 0 degrees
    self.image = pygame.transform.rotate(self.original_image, angle)
    self.rect = self.image.get_frect(center=self.rect.center)

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
    self.original_surf = surf
    self.image = self.original_surf
    self.rect = self.image.get_frect(center = pos)
    self.start_time = pygame.time.get_ticks()
    self.lifetime = 3000
    self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
    self.speed = randint(400, 500)
    self.rotation_speed = randint(20, 80)
    self.rotation = 0

  def update(self, dt):
    self.rect.center += self.direction * self.speed * dt
    if self.rect.top > settings.WINDOW_HEIGHT:
      self.kill()
    self.rotation += self.rotation_speed * dt
    self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
    self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
  def __init__(self, frames, pos, groups):
    super().__init__(groups)
    self.frames = frames
    self.frame_index = 0
    self.image = self.frames[self.frame_index]
    self.rect = self.image.get_frect(center = pos)

  def update(self, dt):
    self.frame_index += 20 * dt
    if self.frame_index < len(self.frames):
      self.image = self.frames[int(self.frame_index)]
    else:
      self.kill()

def collisions():
  global running

  all_sprites.update(dt)
  collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites,
                                                  True, pygame.sprite.collide_mask)
  if collision_sprites:
    running = False
  for laser in laser_sprites:
    collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
    if collided_sprites:
      laser.kill()
      AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
      explosion_sound.play()

def display_score():
  current_time = pygame.time.get_ticks() // 100
  text_surface = font.render(str(current_time), True, (240, 240, 240))
  text_rect = text_surface.get_frect(midbottom = (settings.WINDOW_WIDTH/2,
                                                  settings.WINDOW_HEIGHT - 50))
  screen.blit(text_surface, text_rect)
  pygame.draw.rect(screen, (240, 240, 240), text_rect.inflate(20, 10).move
        (0, -8),5, 5)

#setup
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((settings.WINDOW_WIDTH,settings.WINDOW_HEIGHT))
running = True
pygame.display.set_caption('Space Shooter')

#import
star_surface = pygame.image.load(join('images', 'star.png')).convert_alpha()
enemy_ship_surf = pygame.image.load(join('images',
                                        'enemy_ship.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)
explosion_frames = [pygame.image.load(join('images','explosion',
                      f'{i}.png')).convert_alpha() for i in range(21)]

laser_sound = pygame.mixer.Sound(join('sounds', 'laser.wav'))
laser_sound.set_volume(0.1)
explosion_sound = pygame.mixer.Sound(join('sounds', 'explosion.wav'))
explosion_sound.set_volume(0.1)
damage_sound = pygame.mixer.Sound(join('sounds', 'damage.ogg'))
game_music = pygame.mixer.Sound(join('sounds', 'game_music.wav'))
game_music.set_volume(0.1)
game_music.play()

#sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
for i in range(20):
  Star(all_sprites, star_surface)

player = Player(all_sprites)
#custom events -> Meteor event
meteor_event = pygame.event.custom_type()
enemy_event = pygame.event.custom_type()
#pygame.time.set_timer(meteor_event, 500)
pygame.time.set_timer(enemy_event, 500)

while running:
  dt = clock.tick() / 1000
  #event loop
  for event in pygame.event.get():
    if event.type  == pygame.QUIT:
      running = False
    if event.type == meteor_event:
      x, y = randint(0, settings.WINDOW_WIDTH,), randint(-200, -100)
      Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))
    if event.type == enemy_event:
      if event.type == enemy_event:
        x = randint(0, settings.WINDOW_WIDTH)
        y = randint(-100, -50)  # spawn just above the screen
        EnemyShip(enemy_ship_surf, (x, y), player, (all_sprites, enemy_sprites))


  #updating game
  collisions()

  #draw game
  screen.fill('#1a1f3d')
  display_score()

  all_sprites.draw(screen)

  pygame.display.update()
pygame.quit()