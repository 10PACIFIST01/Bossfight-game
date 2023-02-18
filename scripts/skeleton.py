import pygame
import os
from settings import *
from tools import *
from enemy import *
from entity import *
from bullet import *


class Skeleton(Enemy):
    def __init__(self, screen, player, pos):
        super().__init__(screen, player, "skeleton", 3)

        self.speedX = 3
        self.speedY = 0
        self.hitbox.inflate_ip(-120, -20)
        self.hitbox.center = pos
        self.side = "left"

        self.stay_anim = load_animation(4, "stay", "skeleton")
        self.run_anim = load_animation(6, "walk", "skeleton")
        self.attack_anim = load_animation(12, "attack", "skeleton")
        self.sprites = all_sprites
        self.bullets = bullet_sprites

        self.health = 100
        self.MAX_HEALTH = self.health
        self.damage = 40

        self.attack_distance = 1000
        self.attack_cooldown = 3000
        self.last_attack = pygame.time.get_ticks()
        self.is_attack = False
        self.can_attack = True

    def walk(self):
        self.play_animation(6, self.run_anim, 100, False)

    def stay(self):
        self.play_animation(4, self.stay_anim, 150)

    def attack(self):
        self.is_attack = self.play_animation(12, self.attack_anim, 100, False)
        self.direction.x = 0

        if not self.is_attack:
            self.can_attack = False
            bullet = Bullet("arrow", (self.hitbox.centerx, self.hitbox.centery - 30), self.side, self.player)
            self.last_attack = pygame.time.get_ticks()

    def action(self):
        self.distance = self.get_player_distance(self, self.player)
        if self.distance <= self.vis_radius:
            if self.distance <= self.attack_distance and self.can_attack:
                self.attack()
            else:
                self.direction.x = self.get_player_direction(self, self.player).x
                self.walk()
                if self.player.rect.x - self.rect.x < 0:
                    self.side = "right"
                else:
                    self.side = "left"
        else:
            self.stay()
            self.direction.x = 0

    def play_animation(self, num, frames, framerate=50, is_loop=True):
        now = pygame.time.get_ticks()
        if now - self.last_update > framerate:
            self.last_update = now
            self.count += 1
            self.count = self.count % num

            self.image = frames[self.count]
            self.image = pygame.transform.flip(self.image, self.side == "right", 0)

        if not is_loop:
            if self.count == num - 1:
                return False
            else:
                return True

    def normalize_hitbox(self):
        pass

    def check_cooldowns(self):
        Entity.check_cooldowns(self)

        current = self.current_time
        if not self.can_attack:
            if current - self.last_attack >= self.attack_cooldown:
                self.last_attack = current
                self.can_attack = True
