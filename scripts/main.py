import pygame
import os
from hero import *
from slime import *
from zomby import *
from skeleton import *
from text import *
from settings import *
from tools import *
from background import *
from camera import *


class GameScreen:
    def __init__(self):
        self.FPS = FPS
        self.caption = CAPTION
        self.size = FIELD_SIZE

    def run(self):
        pygame.init()
        self.size = SCREEN_SIZE

        screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        pygame.display.set_caption(self.caption)

        clock = pygame.time.Clock()
        fps = Text("fps", (500, 50))
        fps.color = (255, 0, 0)

        background = Background(screen)
        FIELD_SIZE[0], FIELD_SIZE[1] = background.map_width, background.map_height
        width, height = FIELD_SIZE

        hero = Player(screen)
        zomby = Zomby(screen, hero, (width * 0.5, 1500))
        skeleton = Skeleton(screen, hero, (width * 0.8 , 3000))
        slime = Slime(screen, hero, (width * 0.1, 500))

        self.camera = Camera(FIELD_SIZE[0], FIELD_SIZE[1], self.size)

        while True:
            clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()
                    elif event.key == pygame.K_r:
                        for sprite in all_sprites:
                            sprite.kill()
                        self.run()

            screen.fill((200, 200, 255))

            self.camera.update(hero.rect)

            background.update(hero)
            background.draw(self.camera)

            for sprite in all_sprites:
                try:
                    screen.blit(sprite.image, self.camera.apply(sprite.rect))
                except:
                    pass

            for sprite in all_sprites:
                try:
                    sprite.update(self.camera)
                except:
                    sprite.update()

            #pygame.draw.rect(screen, (255, 0, 0), background.ground_box_rect, 3)

            display_fps = str(int(clock.get_fps()))
            fps.draw(display_fps)

            pygame.display.update()


def show_hitboxes(screen, group, camera):
    for sprite in group:
        pygame.draw.rect(screen, (255, 0, 0), camera.apply(sprite.hitbox), 3)
        pygame.draw.rect(screen, (0, 0, 255), camera.apply(sprite.rect), 3)

if __name__ == "__main__":
    game = GameScreen()
    game.run()
