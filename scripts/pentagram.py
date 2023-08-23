import pygame
import os
import random
from tools import *
from settings import *

import skeleton
import slime
import zomby

class Pentagram(pygame.sprite.Sprite):
	def __init__(self, screen, hero, pos):
		pygame.sprite.Sprite.__init__(self)
		self.folder = os.path.join(load_img_folder("pentagram", False), "spawn")
		self.folder = os.path.join(self.folder, "spawn0.png")
		self.image = pygame.image.load(self.folder)
		self.image = pygame.transform.scale(self.image, (150, 150))
		self.rect = self.image.get_rect()
		self.rect.center = pos

		self.framerate = 50
		self.last_update = pygame.time.get_ticks()
		self.count = 0

		self.frames = load_animation(9, "circulation", "pentagram")
		self.spawn = load_animation(5, "spawn", "pentagram")
		all_sprites.add(self)

		self.spawned = False

		self.lifetime = 3000
		self.birth_time = pygame.time.get_ticks()

		self.screen = screen
		self.hero = hero

	def update(self):
		if self.spawned:
			self.play_animation(9, self.frames, 50)
		else:
			self.spawned = not self.play_animation(5, self.spawn, 100, False)
			if self.spawned:
				self.monsters = [skeleton.Skeleton, zomby.Zomby, slime.Slime]
				monster = self.monsters[random.randint(0, len(self.monsters) - 1)](self.screen, self.hero, self.rect.center)

		current = pygame.time.get_ticks()
		if current - self.birth_time > self.lifetime:
			self.kill()

	def play_animation(self, num, frames, framerate=50, is_loop=True):
		now = pygame.time.get_ticks()
		if now - self.last_update > framerate:
			self.last_update = now
			self.count += 1
			self.count = self.count % num

			self.image = frames[self.count]

		if not is_loop:
			if self.count == num - 1:
				return False
			else:
				return True