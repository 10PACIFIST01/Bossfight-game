import pygame
import os
from settings import *
from tools import *
from enemy import *


class Slime(Enemy):
    def __init__(self, screen, player, pos):
        super().__init__(screen, player, "slime", 3)

        self.speedX = 5
        self.speedY = 0
        self.hitbox.inflate_ip(-20, 0)
        self.hitbox.center = pos

        self.stay_anim = load_animation(6, "stay", "slime", scale = 4)
        self.jump_anim = load_animation(22, "jump", "slime", scale = 4)
        self.shmap_anim = load_animation(18, "shmap", "slime", scale = 4)

        self.health = 70
        self.MAX_HEALTH = self.health
        self.damage = 20

    def walk(self):
        if self.can_walk:
            self.can_walk = self.play_animation(22, self.jump_anim, 50, False)
        else:
            if not self.is_push:
                self.direction.x = 0

    def normalize_hitbox(self):
        self.rect.bottom -= 50
        self.rect.right -= 20
