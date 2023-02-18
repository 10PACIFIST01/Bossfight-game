import pygame
import os
from tools import *
from settings import *


class Heal(pygame.sprite.Sprite):
    def __init__(self, hero, flip=False):
        pygame.sprite.Sprite.__init__(self)

        scale = 3
        self.hero = hero

        folder = load_img_folder("particles", False)
        folder = os.path.join(folder, "heal")
        name = "heal"
        self.anim = []
        for i in range(21):
            img_fold = os.path.join(folder, name + str(i) + ".png")
            img = pygame.image.load(img_fold)
            img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
            img = pygame.transform.flip(img, flip, 0)
            self.anim += [img]

        self.image = self.anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.hero.hitbox.center

        self.count = 0
        self.last_update = 0

        all_sprites.add(self)

    def update(self):
        self.rect.center = self.hero.hitbox.center

        self.play_animation(21, self.anim)

    def play_animation(self, num, frames, framerate=50):
        now = pygame.time.get_ticks()
        if now - self.last_update > framerate:
            self.last_update = now
            self.count += 1
            if self.count == num - 1:
                self.kill()

            self.image = frames[self.count]
