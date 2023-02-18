import pygame
import os
from tools import *
from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, name, pos, side, player):
        super().__init__()

        scale = 3
        self.side = side

        folder = load_img_folder("bullets", False)
        img_folder = os.path.join(folder, name + '.png')
        self.image = pygame.image.load(img_folder)
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * scale, self.image.get_height() * scale))
        self.image = pygame.transform.flip(self.image, self.side == "right", 0)

        self.rect = self.image.get_rect()
        self.hitbox = self.rect
        self.hitbox.inflate_ip(-30, 0)
        self.hitbox.center = pos

        self.speedX = 15
        self.dx = -1 if self.side == "right" else 1
        self.spike_body = True

        self.damage = 40

        self.player = player
        all_sprites.add(self)
        bullet_sprites.add(self)

    def update(self):
        self.hitbox.x += self.speedX * self.dx

        if self.hitbox.colliderect(self.player.hitbox):
            self.player.get_hit(self)
            self.kill()

        if self.rect.x <= -100 or self.rect.x >= FIELD_SIZE[0] * 1.1:
            self.kill()


class Magic(pygame.sprite.Sprite):
    def __init__(self, side, name, pos):
        super().__init__()

        scale = 3
        self.side = side

        folder = load_img_folder("bullets", False)
        self.magic_anim = []
        for i in range(3):
            img_fold = os.path.join(folder, name + str(i) + ".png")
            img = pygame.image.load(img_fold)
            img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
            img = pygame.transform.flip(img, self.side == "left", 0)
            self.magic_anim += [img]
        self.count = 0
        self.last_update = 0

        self.image = self.magic_anim[0]
        self.rect = self.image.get_rect()
        self.hitbox = self.rect
        self.hitbox.center = pos

        self.speedX = 15
        self.dx = 1 if self.side == "right" else -1
        self.damage = 10
        self.can_hit = True
        self.last_update = 0
        self.hit_cooldown = 30

        self.enemies = enemy_sprites
        all_sprites.add(self)

    def update(self):
        self.hitbox.x += self.speedX * self.dx

        for enemy in self.enemies:
            if self.hitbox.colliderect(enemy.hitbox) and self.can_hit:
                enemy.get_hit(self)
                self.can_hit = False

        if self.rect.x <= -100 or self.rect.x >= SCREEN_SIZE[0] * 2:
            self.kill()

        self.play_animation(3, self.magic_anim)
        self.check_cooldown()

    def play_animation(self, num, frames, framerate=50):
        now = pygame.time.get_ticks()
        if now - self.last_update > framerate:
            self.last_update = now
            self.count += 1
            self.count = self.count % num

            self.image = frames[self.count]

    def check_cooldown(self):
        now = pygame.time.get_ticks()

        if not self.can_hit:
            if now - self.last_update > self.hit_cooldown:
                self.can_hit = True
                self.last_update = now
    
    def draw(self, camera):
        self.screen.blit(self.image, camera.apply(self.rect))
