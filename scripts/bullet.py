import pygame
import os
import math
import random
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

        self.check_collide()

    def check_collide(self):
        if self.hitbox.colliderect(self.player.hitbox):
            if self.spike_body:
                #self.player.get_hit(self)
                self.kill()

        if self.rect.x <= -100 or self.rect.x >= FIELD_SIZE[0] * 1.1 or self.rect.y >= FIELD_SIZE[1]:
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

        self.speedX = 25
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

        if self.rect.x <= -100 or self.rect.x >= FIELD_SIZE[0] * 2:
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

class Spear(Bullet):
    def __init__(self, pos, player, weapon_type="bullet"):
        super().__init__("spear", pos, "", player)

        self.speed = 20
        self.dx = 0
        self.speed_change = -1
        self.damage = 200

        self.image_orig = self.image.copy()
        if weapon_type == "trap":
            new_image = pygame.transform.rotate(self.image_orig, 90)
            old_center = self.hitbox.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.hitbox = self.rect
            self.rect.center = old_center
            self.spike_body = False
        self.type = weapon_type

        self.chasing_cooldown = 700
        self.grow_cooldown = 1000
        self.lifetime = 3000
        self.last_update = pygame.time.get_ticks()
        self.angle = 0
        self.rotation_speed = 5

    def update(self):
        self.check_collide()

        now = pygame.time.get_ticks()
        if self.type == "bullet":
            if now - self.last_update < self.chasing_cooldown:
                self.rotate()
            else:
                self.chase()
        elif self.type == "trap":
            if now - self.last_update < self.grow_cooldown:
                self.grow()
            else:
                if now - self.last_update > self.lifetime:
                    self.die()
                else:
                    self.attack()

    def rotate(self):
        length = math.sqrt((self.player.hitbox.centerx - self.hitbox.centerx) ** 2 + (self.player.hitbox.centery - self.hitbox.centery) ** 2)
        cosin = (self.player.hitbox.centerx - self.hitbox.centerx) / length
        sin = (self.player.hitbox.centery - self.hitbox.centery) / length
        self.cosin, self.sin = cosin, sin

        det = 1 if sin <= 0 else -1

        self.angle = det * math.degrees(math.acos(cosin))

        new_image = pygame.transform.rotate(self.image_orig, self.angle)
        old_center = self.hitbox.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.hitbox = self.rect
        self.hitbox.inflate_ip(-30, -30)
        self.rect.center = old_center

    def chase(self):
        self.speed_change += 0.1
        self.speed_change = min(self.speed_change, 1)
        self.hitbox.x += self.speed * self.cosin * self.speed_change
        self.hitbox.y += self.speed * self.sin * self.speed_change
    
    def grow(self):
        self.spike_body = False

        self.hitbox.y -= self.speed * 0.1 if self.hitbox.top > FIELD_SIZE[1] * 0.95 else 0

    def attack(self):
        self.spike_body = True

        self.speed_change += 0.1
        self.speed_change = min(self.speed_change, 1)
        self.hitbox.y -= self.speed * self.speed_change if self.hitbox.top > FIELD_SIZE[1] * 0.83 else 0

    def die(self):
        self.spike_body = False

        self.speed_change -= 0.1
        self.speed_change = max(self.speed_change, -1)
        self.hitbox.y -= self.speed * self.speed_change * 0.5

        if self.hitbox.top > FIELD_SIZE[1]:
            self.kill()


class Fireball(Bullet):
    def __init__(self, pos, player):
        super().__init__("fireball", pos, "", player)

        self.speed = 10
        self.dx = get_player_direction(self, player).x
        self.damage = 200
        self.amplitude = 7
        self.angle = random.randint(0, 360)

    def update(self):
        self.check_collide()
        self.hitbox.x += self.speed * self.dx
        self.hitbox.y += math.sin(self.angle) * self.amplitude

        self.angle += 0.05