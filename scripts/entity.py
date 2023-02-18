import pygame
import os
from settings import *
from tools import *



class Entity(pygame.sprite.Sprite):
    def __init__(self, screen, entity_type, scale=3):
        pygame.sprite.Sprite.__init__(self)

        img_folder = load_img_folder(entity_type)
        self.image = pygame.image.load(img_folder)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale, self.image.get_height() * scale))
        self.screen = screen

        self.rect = self.image.get_rect()
        self.rect.x = 1000
        self.rect.bottom = SCREEN_SIZE[1] * 0.9
        self.hitbox = self.rect.inflate(20, 0)

        self.field_size = FIELD_SIZE
        self.on_ground = False
        self.gravity = GRAVITY

        self.direction = pygame.math.Vector2()
        self.speedX = 5
        self.speedY = 0
        self.side = "right"

        self.count = 0
        self.last_update = pygame.time.get_ticks()
        self.last_hit = pygame.time.get_ticks()

        self.invisibility_cooldown = 250
        self.can_be_attacked = True
        self.health = 100
        self.MAX_HEALTH = self.health
        self.damage = 20

        self.is_push = False
        self.impulse = 2
        self.MAX_SPEEDX = 5
        self.MAX_SPEEDY = 10
        self.last_dx = 0
        self.can_move = True
        self.is_invincible = False
        self.is_dead = False

        all_sprites.add(self)

        self.particles = []

    def stay(self):
        self.play_animation(6, self.stay_anim, 75)

    def move(self):
        if self.can_move:
            self.hitbox.x += self.direction.x * self.speedX
            self.hitbox.y += self.direction.y * self.speedY

    def get_hit(self, entity):
        self.health -= entity.damage

        self.speedY = 4
        self.direction.y = -1
        self.speedX = -20
        self.is_push = True

        self.can_be_attacked = False
        self.last_hit = self.current_time

    def check_gravity(self):
        if not self.on_ground:
            self.direction.y = -1
            self.speedY -= self.gravity
        else:
            self.direction.y = 0

    def check_push(self):
        if self.is_push:
            self.speedX += self.impulse

            if abs(self.speedX) <= self.MAX_SPEEDX and self.speedX > 0:
                self.speedX = self.MAX_SPEEDX
                self.is_push = False

            self.stay()
        else:
            self.speedX = self.MAX_SPEEDX

    def check_collide(self):
        self.current_hitbox = self.camera.apply(self.hitbox)

        if self.hitbox.right >= self.field_size[0]:
            self.hitbox.right = self.field_size[0]
        if self.hitbox.left <= 0:
            self.hitbox.left = 0
        if self.hitbox.bottom >= self.field_size[1] * 0.9:
            self.hitbox.bottom = self.field_size[1] * 0.9
            self.on_ground = True
        else:
            self.on_ground = False

        self.rect.center = self.hitbox.center


    def check_cooldowns(self):
        if self.can_move:
            self.current_time = pygame.time.get_ticks()

            if self.current_time - self.last_hit >= self.invisibility_cooldown:
                self.can_be_attacked = True
                self.is_invincible = False

    def check_particles(self):
        for particles in self.particles:
            particles.update()

    def play_animation(self, num, frames, framerate=50, is_loop=True):
        now = pygame.time.get_ticks()
        if now - self.last_update > framerate:
            self.last_update = now
            self.count += 1
            self.count = self.count % num

            self.image = frames[self.count]
            self.image = pygame.transform.flip(self.image, self.side == "left", 0)

        if not is_loop:
            if self.count == num - 1:
                return False
            else:
                return True

    def check_all(self, camera):
        self.camera = camera

        self.check_cooldowns()
        self.check_state()
        self.check_gravity()
        self.check_collide()
        self.check_health()
        self.check_push()
        self.check_particles()

    def check_health(self):
        if self.health <= 0 and self.on_ground:
            self.die()

    def die(self):
        self.kill()
