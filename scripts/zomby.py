import pygame
import os
from settings import *
from tools import *
from enemy import *


class Zomby(Enemy):
        def __init__(self, screen, player, pos):
            super().__init__(screen, player, "zomby", 3)

            self.speedX = 1
            self.speedY = 0
            self.hitbox.inflate_ip(-100, -20)
            self.hitbox.center = pos

            self.attack_box = self.rect.inflate(-60, 0)
            self.attack_radius = 200
            self.can_attack = True
            self.is_attack = False
            self.attack_cooldown = 200
            self.last_attack = pygame.time.get_ticks()

            self.stay_anim = load_animation(4, "stay", "zomby")
            self.run_anim = load_animation(7, "walk", "zomby")
            self.attack_anim = load_animation(6, "attack", "zomby")

            self.health = 150
            self.MAX_HEALTH = self.health
            self.damage = 50
            self.spike_body = False

        def walk(self):
            if self.can_walk:
                self.can_walk = self.play_animation(7, self.run_anim, 100, False)
            else:
                if not self.is_push:
                    self.direction.x = 0

        def stay(self):
            self.play_animation(4, self.stay_anim, 150)

        def attack(self):
            self.is_attack = self.play_animation(6, self.attack_anim, 100, is_loop=False)
            self.direction.x = 0

            if not self.is_attack:
                self.last_attack = pygame.time.get_ticks()

        def check_state(self):
            if self.is_attack:
                self.attack()

        def check_cooldowns(self):
            Enemy.check_cooldowns(self)

            current_time = self.current_time
            if not self.can_attack:
                if current_time - self.last_attack >= self.attack_cooldown:
                    self.can_attack = True

        def normalize_hitbox(self):
            if self.side == "left":
                self.attack_box.left = self.hitbox.right
            else:
                self.attack_box.right = self.hitbox.left
            self.attack_box.top = self.hitbox.top

        def can_damage(self):
            return self.is_attack and 6 - self.count <= 3

        def action(self):
            Enemy.action(self)

            if self.distance <= self.attack_radius:
                self.is_attack = True
