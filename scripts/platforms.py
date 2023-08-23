import pygame
import os
from tools import *
from settings import *

class Platform(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.folder = os.path.join(load_img_folder("platforms", False), "platform.png")
		self.image = pygame.image.load(self.folder)
		self.image = pygame.transform.scale(self.image, (self.image.get_width() * 3, self.image.get_height() * 3))
		self.rect = self.image.get_rect()
		self.rect.center = pos
		self.hitbox = self.rect

		all_sprites.add(self)
		border_sprites.add(self)

	def update(self):
		pass