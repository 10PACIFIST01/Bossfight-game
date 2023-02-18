import pygame
import os
import math
from settings import *
from tools import *
from entity import *
from bullet import *
from heal import *


class Player(Entity):
    def __init__(self, screen):
        super().__init__(screen, "hero")

        self.rect.x = 200
        self.speedX = 10
        self.MAX_SPEEDX = self.speedX

        self.attack_box = self.rect.inflate(30, 0)
        self.damage = 30
        self.health = 500
        self.MAX_HEALTH = self.health
        self.impulse = 2
        self.invisibility_cooldown = 1000

        health_image_folder = os.path.join(load_img_folder("UI", False), "health_bar.png")
        self.health_bar_image = pygame.image.load(health_image_folder)
        self.health_bar_image = pygame.transform.scale(self.health_bar_image, (250, 50))
        self.health_rect = self.health_bar_image.get_rect()

        self.enemies = enemy_sprites
        self.bullets = bullet_sprites

        # animations
        self.stay_anim = load_animation(6, "stay", "hero")
        self.run_anim = load_animation(6, "run", "hero")
        self.jump_anim = load_animation(5, "jump", "hero")
        self.death_anim = load_animation(9, "death", "hero")

        fold = load_img_folder("hero", False)
        fold = os.path.join(fold, "spell")
        img_fold = os.path.join(fold, "spell.png")
        self.spell_image = pygame.image.load(img_fold).convert_alpha()
        self.spell_image = pygame.transform.scale(self.spell_image, (self.spell_image.get_width() * 3, self.spell_image.get_height() * 3))

        self.attack_anim = load_animation(9, "attack", "hero")
        self.slash_anim = load_animation(5, "slash", "hero")
        self.power_hit_anim = load_animation(6, "power_hit", "hero")
        self.attacks = [self.attack_anim, self.slash_anim, self.power_hit_anim]
        self.frames = [9, 5, 6]
        self.attack_index = 0
        self.attack_cooldown = 500
        self.combo_cooldown = 300
        self.magic_cooldown = 300
        self.last_spell = 0
        self.last_attack = 0

        self.is_attack = False
        self.can_attack = True
        self.is_magic = False
        self.can_magic = True

        self.mana = 50
        self.MAX_MANA = 100
        self.mana_cost = 20
        self.heal_points = 100
        self.MAX_HEAL_POINTS = 100

        heal_circ = os.path.join(load_img_folder("UI", False), "health")
        self.heal_frames = []
        for i in range(16):
            frame = os.path.join(heal_circ, f"health_circle{i}.png")
            frame = pygame.image.load(frame)
            frame = pygame.transform.scale(frame, (frame.get_width() * 3 + 10, frame.get_height() * 3))
            self.heal_frames += [frame]

        pygame.joystick.init()
        if pygame.joystick.get_count():
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        self.input = "keyboard"

    # some actions
    def jump(self):
        if self.on_ground:
            self.on_ground = False
            self.is_attack = False
            self.direction.y = -1
            self.speedY = 17
            self.MAX_SPEEDY = self.speedY

    def check_gravity(self):
        Entity.check_gravity(self)
        if not self.on_ground and not self.is_push:
            self.image = pygame.transform.flip(self.jump_anim[1], self.side == "left", 0)

    def run(self):
        if self.on_ground:
            self.play_animation(6, self.run_anim, 60)

    def attack(self):
        self.is_attack = self.play_animation(self.frames[self.attack_index], self.attacks[self.attack_index], 45, is_loop=False)
        if not self.is_attack:
            if self.attack_index != 2: self.can_attack = True
            self.last_attack = pygame.time.get_ticks()
            self.attack_index += 1
            self.attack_index %= 3

    def spell(self):
        self.last_spell = pygame.time.get_ticks()
        self.is_magic = True
        self.can_magic = False

        self.image = self.spell_image
        self.image = pygame.transform.flip(self.image, self.side == "left", 0)

        self.hitbox.x += self.speedX * 3 if self.side == "left" else -self.speedX * 3

        if self.mana > self.mana_cost:
            self.mana -= self.mana_cost
            magic = Magic(self.side, "magic_ball", self.hitbox.center)

    def heal(self):
        self.health = self.MAX_HEALTH
        self.heal_points = 0
        heal1 = Heal(self)
        heal2 = Heal(self, True)

    # input
    def check_state(self):
        if self.is_attack:
            self.attack()
        elif self.is_magic:
            self.image = self.spell_image
            self.image = pygame.transform.flip(self.image, self.side == "left", 0)

        if self.can_move:
            if pygame.joystick.get_count():
                self.input = "gamepad"
            else:
                self.input = "keyboard"

            if self.input == "keyboard":
                self.check_keyboard()
            elif self.input == "gamepad":
                self.check_controller()

    def check_keyboard(self):
        k_state = pygame.key.get_pressed()
        if k_state[pygame.K_d] and not k_state[pygame.K_a]:
            self.is_attack = False
            self.direction.x = 1
            self.last_dx = 1
            self.side = "right"
            self.run()
        elif k_state[pygame.K_a] and not k_state[pygame.K_d]:
            self.is_attack = False
            self.direction.x = -1
            self.last_dx = -1
            self.side = "left"
            self.run()
        elif k_state[pygame.K_j] and self.on_ground and self.can_attack and not self.is_attack:
            self.can_attack = False
            self.is_attack = True
            self.count = 0
        elif k_state[pygame.K_k] and not self.is_magic and self.can_magic:
            self.spell()
        else:
            if not self.is_push:
                self.direction.x = 0
            if not self.is_attack and self.on_ground and not self.is_magic:
                self.stay()

        if k_state[pygame.K_i] and self.heal_points == self.MAX_HEAL_POINTS:
            self.heal()

        if k_state[pygame.K_SPACE]:
            self.jump()

    def check_controller(self):
        if self.joystick.get_axis(0) > 0:
            self.is_attack = False
            self.direction.x = 1
            self.side = "right"
            self.run()
        elif self.joystick.get_axis(0) < 0:
            self.is_attack = False
            self.direction.x = -1
            self.side = "left"
            self.run()
        elif self.joystick.get_button(2) and self.on_ground and self.can_attack and not self.is_attack:
            self.can_attack = False
            self.is_attack = True
            self.count = 0
        elif self.joystick.get_button(1) and not self.is_magic and self.can_magic:
            self.spell()
        else:
            if not self.is_push:
                self.direction.x = 0
            if not self.is_attack and self.on_ground and not self.is_magic:
                self.stay()

        if self.joystick.get_button(0):
            self.jump()
        if self.joystick.get_button(6):
            pygame.quit()

    def check_cooldowns(self):
        Entity.check_cooldowns(self)

        current_time = self.current_time
        if not self.can_attack:
            if current_time - self.last_attack >= self.attack_cooldown:
                self.can_attack = True
        elif current_time - self.last_attack >= self.combo_cooldown and not self.is_attack:
            self.attack_index = 0

        if self.is_magic:
            if current_time - self.last_spell >= self.magic_cooldown:
                self.is_magic = False

        if not self.can_magic:
            if current_time - self.last_spell >= self.magic_cooldown * 3:
                self.can_magic = True

    def normalize_hitbox(self):
        self.rect.right -= 100
        self.rect.bottom -= 25

        if self.side == "right":
            self.attack_box.left = self.hitbox.right
        else:
            self.attack_box.right = self.hitbox.left
        self.attack_box.top = self.hitbox.top

    def check_collide(self):
        Entity.check_collide(self)

        for enemy in self.enemies:
            if enemy.spike_body:
                if enemy.hitbox.colliderect(self.hitbox):
                    if self.can_be_attacked:
                        self.get_hit(enemy)
            elif not enemy.spike_body:
                if enemy.attack_box.colliderect(self.hitbox):
                    if self.can_be_attacked and enemy.can_damage():
                        self.get_hit(enemy)

        for bullet in self.bullets:
            if bullet.hitbox.colliderect(self.hitbox):
                if self.can_be_attacked:
                    self.get_hit(bullet)



    def can_damage(self):
        return self.is_attack and self.frames[self.attack_index] - self.count <= 2

    def draw_health_bar(self, screen, pos, health, mana):
        if health < 0:
            health = 0

        BAR_LENGTH = 95
        BAR_HEIGHT = 20
        fill = (health / self.MAX_HEALTH) * BAR_LENGTH
        fill_rect = pygame.Rect(pos[0], pos[1], fill * 2, BAR_HEIGHT)

        col_1 = gradient(fill, 1, BAR_LENGTH, 200, 255)
        pygame.draw.rect(screen, (int(col_1) + 20, 0, 150), fill_rect)

        self.draw_health_bar_image(screen, pos)
        self.draw_mana_bar(screen, (pos[0], pos[1] + 27), mana)

    def draw_mana_bar(self, screen, pos, mana):
        if mana < 0:
            mana = 0
        elif mana >= self.MAX_MANA:
            self.mana = self.MAX_MANA
        if self.heal_points >= self.MAX_HEAL_POINTS:
            self.heal_points = self.MAX_HEAL_POINTS

        BAR_LENGTH = 90
        BAR_HEIGHT = 6
        fill = (mana / self.MAX_MANA) * BAR_LENGTH
        fill_rect = pygame.Rect(pos[0], pos[1], fill * 2, BAR_HEIGHT)

        color = (0, 0, 255)
        pygame.draw.rect(screen, color, fill_rect)

    def draw_health_bar_image(self, screen, pos):
        self.health_rect.left = pos[0] - 60
        self.health_rect.top = pos[1] - 15
        frame = self.heal_frames[15 - int(self.heal_points / 100 * 15)]
        frame_rect = frame.get_rect()
        frame_rect.center = (pos[0] - 30, pos[1] + 10)
        screen.blit(frame, frame_rect)
        screen.blit(self.health_bar_image, self.health_rect)

    def die(self):
        self.is_invincible = True
        self.can_move = False
        if self.is_dead:
            self.image = self.death_anim[-1]
            self.image = pygame.transform.flip(self.image, self.side == "left", 0)
        else:
            self.is_dead = not self.play_animation(9, self.death_anim, 100, is_loop=False)

    def get_hit(self, entity):
        if not self.is_invincible:
            self.is_invincible = True
            Entity.get_hit(self, entity)

    def update(self, camera):
        self.move()
        self.check_all(camera)
        self.normalize_hitbox()
        self.draw_health_bar(self.screen, (110, self.field_size[1] - 45), self.health, self.mana)
