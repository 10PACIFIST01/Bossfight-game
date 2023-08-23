import pygame
import os
from settings import *
from tools import *
from entity import *
from soul import *
from particles import *


class Enemy(Entity):
    def __init__(self, screen, player, entity, scale = 3):
        super().__init__(screen, entity, scale)

        self.speedX = 1
        self.speedY = 0

        self.can_walk = True
        self.is_push = False
        self.spawned = True
        self.walk_cooldown = 400
        self.last_step = pygame.time.get_ticks()
        self.impulse = 2

        self.player = player
        self.vis_radius = 700

        self.health = 50
        self.MAX_HEALTH = self.health
        self.damage = 20
        self.spike_body = True
        self.die_alpha = 0
        self.spawn_alpha = 0

        enemy_sprites.add(self)

        self.get_player_distance = get_player_distance
        self.get_player_direction = get_player_direction

    def check_state(self):
        if self.direction.x > 0:
            self.last_dx = 1
            self.walk()
            self.side = "left"
        if self.direction.x < 0:
            self.last_dx = -1
            self.walk()
            self.side = "right"
        if self.direction.x == 0 and self.on_ground:
            self.stay()


    # make enemy's behavior
    def action(self):
        self.distance = self.get_player_distance(self, self.player)
        if self.distance <= self.vis_radius:
            self.direction.x = self.get_player_direction(self, self.player).x
            self.walk()
            if self.player.rect.x - self.rect.x < 0:
                self.side = "right"
            else:
                self.side = "left"
        else:
            self.stay()
            self.direction.x = 0

    def get_hit(self, entity):
        self.particles += [Particles((self.camera.apply(self.hitbox).center[0], self.camera.apply(self.hitbox).top), (255, 0, 0), 8, self.screen)]
        Entity.get_hit(self, entity)

    def check_collide(self):
        Entity.check_collide(self)

        if self.hitbox.colliderect(self.player.attack_box) and self.player.can_damage():
            if self.can_be_attacked:
                self.get_hit(self.player)
                self.player.heal_points += 5

        #self.hitbox = camera.apply(self.hitbox)

    def check_push(self):
        Entity.check_push(self)

        if self.is_push:
            set_color(self.image, pygame.Color(255, 0, 0))

    def check_cooldowns(self):
        Entity.check_cooldowns(self)

        current_time = self.current_time
        if not self.can_walk:
            if current_time - self.last_step >= self.walk_cooldown:
                self.last_step = current_time
                self.can_walk = True

    def die(self):
        self.invincible = True
        self.can_move = False
        self.image = self.stay_anim[-1]
        if self.is_dead:
            for i in range(10):
                soul = Soul(self.player, self.rect.center)
                particle_sprites.add(soul)
                all_sprites.add(soul)
            Entity.die(self)
        else:
            set_color(self.image, pygame.Color(255, 255, 255, self.die_alpha), self.die_alpha)
            self.die_alpha += 5
            if self.die_alpha >= 255:
                self.is_dead = True

    def show(self):
        pass


    def update(self, camera):
        self.camera = camera

        if not self.spawned:
            self.show()
        self.action()
        self.move()
        self.check_all()
        self.normalize_hitbox()
        # self.draw_health_bar(self.screen, (self.hitbox.centerx - 75, self.hitbox.top - 20), self.health)