import pygame
import os
import math
import random

from settings import *
from tools import *
from entity import *
from enemy import *
from particles import *

import bullet
import pentagram

class Boss(Enemy):
	def __init__(self, screen, player, pos):
		super().__init__(screen, player, "boss")

		self.speedX = 30
		self.max_speedX = 30
		self.speedY = 20
		self.acceleration = 4
		self.hitbox.inflate_ip(-110, 0)
		self.hitbox.center = pos
		self.original_pos = pos
		self.axis = pos[1]
		self.side = "right"
		self.target = pos[0]

		self.stay_anim = load_animation(6, "stay", "boss")
		self.attack_anim = load_animation(6, "attack", "boss")
		self.prepare_anim = load_animation(6, "prepare", "boss")
		self.release_anim = load_animation(6, "release", "boss")

		health_image_folder = os.path.join(load_img_folder("UI", False), "boss_bar.png")
		self.health_bar_image = pygame.image.load(health_image_folder)
		self.health_bar_image = pygame.transform.scale(self.health_bar_image, (500, 100))
		self.health_rect = self.health_bar_image.get_rect()
		self.health_rect.center = (SCREEN_SIZE[0] / 2, 50)
 
		self.sprites = all_sprites
		self.bullets = bullet_sprites
		self.attack_list = [self.spear_chasing, self.floor_is_spears, self.summoning, self.wave_of_fireballs]

		self.health = 1000
		self.MAX_HEALTH = self.health
		self.damage = 20
		self.escape_radius = random.randint(200, 1000)

		self.attack_cooldown = 5000
		self.attack_duration = 10000
		self.spear_spawn_cooldown = 1200
		self.fireball_cast_cooldown = 700
		self.last_attack = pygame.time.get_ticks()
		self.last_spear = pygame.time.get_ticks()
		self.last_fireball = pygame.time.get_ticks()
		self.last_start = pygame.time.get_ticks()
		self.is_attack = False
		self.is_attack_work = True
		self.can_attack = True
		self.is_prepare = True
		self.is_release = False
		self.is_escaping = False

		self.is_pushable = False
		self.is_massive = False
		self.spawned = True
		self.is_showed = False

		self.time = 0
		self.current_attack_ind = random.randint(0, 3)

	# boss is always looking at the center of screen
	def check_state(self):
		pass

	def normalize_hitbox(self):
		self.rect.right -= 80
		self.rect.bottom -= 25

	def stay(self):
		self.attack_cooldown = 5000
		if not self.is_release:
			Enemy.stay(self)
			self.hitbox.y = self.axis + math.sin(self.time) * self.speedY
			self.time += 0.1
			self.chase_player()
			self.escape_radius = random.randint(200, 1000)
			self.target = self.rect.center[0] - self.get_player_direction(self, self.player).x * self.escape_radius
		else:
			self.is_release = self.play_animation(6, self.release_anim, 100, False)
			self.is_prepare = True

	def attack(self):
		if not self.is_prepare:
			self.play_animation(6, self.attack_anim, 75)
			self.hitbox.y = self.axis + math.sin(self.time) * self.speedY
			self.time += 0.1

			self.escape()
			self.attack_list[self.current_attack_ind]()
		else:
			self.is_prepare = self.play_animation(6, self.prepare_anim, 100, False)
			self.is_release = True
			self.is_attack_work = True
			self.current_attack_ind = random.randint(0, 3)
			#self.current_attack_ind = 3

	def chase_player(self):
		distance = get_player_distance(self, self.player)

		if distance >= 700:
			self.direction.x = self.get_player_direction(self, self.player).x
		else:
			self.direction.x = 0

	def escape(self):
		self.is_escaping = True
		self.direction.x = -self.get_player_direction(self, self.player).x
		self.speedX = 0.6 * self.max_speedX
		if abs(self.rect.center[0] - self.target) < 20:
			self.direction.x = 0
			self.speedX = self.max_speedX
			self.is_escaping = False

	def spear_chasing(self):
		now = pygame.time.get_ticks()
		self.attack_cooldown = 10000

		if now - self.last_spear >= self.spear_spawn_cooldown and not self.is_escaping:
			spear = bullet.Spear((self.hitbox.centerx - 80, self.hitbox.centery - 100), self.player)
			self.last_spear = now

	def floor_is_spears(self):
		self.attack_cooldown = 10000
		if self.is_attack_work and not self.is_escaping:
			for i in range(20):
				spike = bullet.Spear((self.field_size[0] / 20 * i, self.field_size[1]), self.player, "trap")
			self.is_attack_work = False

	def summoning(self):
		self.attack_cooldown = 10000
		if self.is_attack_work and not self.is_escaping:
			for i in range(random.randint(3, 7)):
				new_enemy = pentagram.Pentagram(self.screen, self.player, (random.randint(0, 5000), self.field_size[1] * 0.9 - 100))
			self.is_attack_work = False

	def wave_of_fireballs(self):
		self.attack_cooldown = 15000
		now = pygame.time.get_ticks()

		if now - self.last_fireball >= self.fireball_cast_cooldown and not self.is_escaping:
			fireball = bullet.Fireball(([-random.randint(0, 50), FIELD_SIZE[0] + random.randint(0, 50)][random.randint(0, 1)], random.randint(200, FIELD_SIZE[1] - 50)), self.player)
			self.last_fireball = now

	def action(self):
		if self.is_showed:
			if not self.is_attack:
				self.stay()
			else:
				self.attack()

	def check_health(self):
		if self.health <= 0:
			self.die()

	def check_cooldowns(self):
		Enemy.check_cooldowns(self)

		current = self.current_time
		if current - self.last_attack >= self.attack_cooldown:
			self.last_attack = current
			self.is_attack = not self.is_attack
			self.count = 0

	def draw_health_bar(self, pos, health):
		if health < 0:
			health = 0

		BAR_LENGTH = 200
		BAR_HEIGHT = 20
		fill = (health / self.MAX_HEALTH) * BAR_LENGTH
		fill_rect = pygame.Rect(pos[0], pos[1], fill * 2, BAR_HEIGHT)
		back_rect = pygame.Rect(pos[0], pos[1], BAR_LENGTH * 2, BAR_HEIGHT)

		#col_1 = gradient(fill, 1, BAR_LENGTH, 200, 255)
		pygame.draw.rect(self.screen, (0, 0, 0), back_rect)
		pygame.draw.rect(self.screen, (255, 255, 255), fill_rect)
		self.screen.blit(self.health_bar_image, self.health_rect)

	def update(self, camera):
		Enemy.update(self, camera)

		self.draw_health_bar((self.health_rect.x + 100, 50), self.health)

	def show(self):
		Enemy.stay(self)

		self.hitbox.y -= self.speedY * 0.2
		if self.hitbox.y < self.original_pos[1]:
			self.is_showed = True
