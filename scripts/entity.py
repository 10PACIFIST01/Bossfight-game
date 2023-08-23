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
        self.current_time = pygame.time.get_ticks()

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
        self.is_pushable = True
        self.is_massive = True
        self.is_collision = False

        all_sprites.add(self)

        self.particles = []

    def stay(self):
        self.play_animation(6, self.stay_anim, 75)

    def move(self):
        if self.can_move:
            self.hitbox.x += self.direction.x * self.speedX
            self.check_collisions(self.direction.x, 0)

            self.hitbox.y += self.direction.y * self.speedY
            self.check_collisions(0, -self.speedY)

    def get_hit(self, entity):
        self.health -= entity.damage

        if self.is_pushable:
            self.speedY = 4
            self.direction.y = -1
            self.speedX = -20
            self.is_push = True

        self.can_be_attacked = False
        self.last_hit = self.current_time

    def check_gravity(self):
        # if not self.on_ground:
        #     self.direction.y = -1
        #     self.speedY -= self.gravity
        # else:
        #     self.direction.y = 0

        self.speedY -= self.gravity
        self.direction.y = -1

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
        if self.hitbox.bottom >= self.field_size[1] * 0.9 and self.is_massive:
            self.hitbox.bottom = self.field_size[1] * 0.9
            self.on_ground = True
            #self.speedY = 0

        self.rect.center = self.hitbox.center

    def check_collisions(self, x_vel, y_vel):
        for border in border_sprites:
            if self.hitbox.colliderect(border.rect):
                # if x_vel > 0:
                #     self.hitbox.right = border.rect.left

                # if x_vel < 0:
                #     self.hitbox.left = border.rect.right

                if y_vel > 0 and self.hitbox.bottom - 20 <= border.rect.top:
                    self.hitbox.bottom = border.rect.top
                    self.speedY = 0
                    self.on_ground = True

                # if y_vel < 0:
                #     self.hitbox.top = border.rect.bottom
                #     self.speedY = 0

                self.is_collision = True


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

    def check_all(self):

        self.check_cooldowns()
        self.check_state()
        self.check_gravity() if self.is_massive else 0
        self.check_collide()
        self.check_health()
        self.check_push()
        self.check_particles()

    def check_health(self):
        if self.health <= 0 and self.on_ground:
            self.die()

    def die(self):
        self.kill()
