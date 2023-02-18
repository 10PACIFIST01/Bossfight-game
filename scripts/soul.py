import pygame
import random
import math
import os
from tools import *


class Soul(pygame.sprite.Sprite):
    def __init__(self, hero, pos):
        pygame.sprite.Sprite.__init__(self)
        self.folder = os.path.join(load_img_folder("particles", False), "soul.png")
        self.image = pygame.image.load(self.folder)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.hitbox = self.rect

        self.hero = hero
        self.rect.center = (pos[0] + random.randint(0, 70), pos[1] + random.randint(0, 70))

        self.angle = 0
        self.diameter = get_player_distance(self, self.hero)
        self.speed = random.randint(5, 7)
        self.amplitude = random.randint(4, 7)

    def update(self):
        self.rect.y -= math.sin(self.angle) * self.amplitude
        self.rect.y += self.speed * get_player_direction(self, self.hero).y * 0.4
        self.rect.x += self.speed * get_player_direction(self, self.hero).x
        self.hitbox = self.rect

        self.angle += 0.1

        self.check_collide(self.hero)

    def check_collide(self, player):
        if self.rect.colliderect(player.hitbox):
            player.mana += 2
            self.kill()
