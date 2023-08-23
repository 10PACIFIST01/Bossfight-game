import pygame

pygame.init()
info_object = pygame.display.Info()

GRAVITY = 0.8
FPS = 60
SCREEN_SIZE = (info_object.current_w, info_object.current_h)
FIELD_SIZE = [500, 600]
CAPTION = "Bossfight"
GROUND_RECT = (SCREEN_SIZE[0], SCREEN_SIZE[1] * 0.9 + 20)

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
particle_sprites = pygame.sprite.Group()
border_sprites = pygame.sprite.Group()
