import pygame
import os
from tools import *
from settings import *
from camera import *


class Background():

    def __init__(self, screen):
        self.ground_list = []
        self.trees_list = []
        self.background_anim = load_animation(11, "background", "background", 9, ".jpg")
        for i in range(len(self.background_anim)):
            self.background_anim[i] = pygame.transform.scale(self.background_anim[i], (self.background_anim[i].get_width() * 0.7, SCREEN_SIZE[1] - 150))
        self.background_image = self.background_anim[0]
        self.background_rect = self.background_image.get_rect()
        self.screen = screen
        self.add_ground(25)
        self.add_trees(10)
        self.background_rect.bottom = self.ground_list[0][1].top
        self.trees_box_rect = pygame.Rect(0, 0, self.trees_list[0][0].get_width() * 10, self.trees_list[0][0].get_height())
        self.trees_box_rect.bottom = self.trees_list[0][1].bottom
        self.ground_box_rect = pygame.Rect(0, 0, self.ground_list[0][0].get_width() * 25, self.ground_list[0][0].get_height())
        self.ground_box_rect.bottom = self.ground_list[0][1].bottom

        self.framerate = 150
        self.last_update = pygame.time.get_ticks()
        self.count = 0

        self.map_width = self.background_image.get_width() * 1.5
        self.map_height = self.background_image.get_height() + self.ground_list[0][0].get_height() - 30


        self.background_rect.left -= 200
        self.trees_box_rect.left -= 200

    def load_background_image(self, name):
        background_folder = load_img_folder("background", False)
        background_folder = os.path.join(background_folder, name)
        background = pygame.image.load(background_folder).convert_alpha()

        return background

    def add_ground(self, count):
        for i in range(count):
            ground_image = self.load_background_image("ground.jpg")
            ground_image = pygame.transform.scale(ground_image, (ground_image.get_width() * 3, ground_image.get_height() * 3))
            ground_rect = ground_image.get_rect()
            ground_rect.bottom = SCREEN_SIZE[1]
            ground_rect.left = i * ground_image.get_width()
            self.ground_list += [(ground_image, ground_rect)]

    def draw_ground(self, camera):
        for ground_image, ground_rect in self.ground_list:
            self.screen.blit(ground_image, camera.apply(ground_rect))

    def configure_ground(self):
        for i in range(len(self.ground_list)):
            self.ground_list[i][1].left = self.ground_box_rect.left + i * self.ground_list[i][0].get_width() - 10

    def add_trees(self, count):
        for i in range(count):
            trees_image = self.load_background_image("trees1.png")
            trees_image = pygame.transform.scale(trees_image, (trees_image.get_width() * 5, trees_image.get_height() * 6))
            trees_rect = trees_image.get_rect()
            trees_rect.bottom = self.ground_list[0][1].top + 10
            trees_rect.left = i * trees_image.get_width() - 10
            self.trees_list += [(trees_image, trees_rect)]

    def draw_trees(self, camera):
        for trees_image, trees_rect in self.trees_list:
            self.screen.blit(trees_image, camera.apply(trees_rect))

    def configure_trees(self):
        for i in range(len(self.trees_list)):
            self.trees_list[i][1].left = self.trees_box_rect.left + i * self.trees_list[i][0].get_width() - 10

    def draw_background(self, camera):
        self.screen.blit(self.background_image.convert_alpha(), camera.apply(self.background_rect))

    def draw(self, camera):
        self.draw_ground(camera)
        self.draw_background(camera)
        self.draw_trees(camera)

    def play_animation(self, num, frames, framerate=50):
        now = pygame.time.get_ticks()
        if now - self.last_update > framerate:
            self.last_update = now
            self.count += 1
            self.count = self.count % num

            self.background_image = frames[self.count]

    def parallax_effect(self, player):
        self.parallax_configure(player, 0.8, self.background_rect)
        self.parallax_configure(player, 0.5, self.trees_box_rect)
        self.parallax_configure(player, 0.2, self.ground_box_rect)


    def parallax_configure(self, player, coof, target):
        speedX = player.speedX * coof

        if player.hitbox.x > self.map_width - SCREEN_SIZE[0] / 2:
            speedX = 0
        if player.hitbox.x < SCREEN_SIZE[0] / 2:
            speedX = 0

        target.x += player.direction.x * speedX

        # if target.right < self.map_width:
        #     target.right = self.map_width
        # if target.left > 0:
        #     target.left = 0

    def update(self, player):
        self.play_animation(11, self.background_anim, self.framerate)
        self.parallax_effect(player)
        self.configure_trees()
