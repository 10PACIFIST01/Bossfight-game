import pygame
import os
from hero import *
from slime import *
from zomby import *
from skeleton import *
from boss import *
from text import *
from settings import *
from tools import *
from background import *
from platforms import *
from camera import *
from bullet import Spear


class GameScreen:
    def __init__(self):
        self.FPS = FPS
        self.caption = CAPTION
        self.size = FIELD_SIZE

    def run(self):
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count():
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        self.size = SCREEN_SIZE

        screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        pygame.display.set_caption(self.caption)

        self.clock = pygame.time.Clock()
        fps = Text("fps", (500, 50))
        fps.color = (255, 0, 0)

        background = Background(screen)
        FIELD_SIZE[0], FIELD_SIZE[1] = background.map_width, background.map_height
        width, height = FIELD_SIZE

        platforms = [Platform((1050, 650)), Platform((1350, 400)), Platform((750, 400)), Platform((FIELD_SIZE[0] - 1050, 650)), Platform((FIELD_SIZE[0] - 1350, 400)), Platform((FIELD_SIZE[0] - 750, 400))]
        hero = Player(screen)
        #zomby = Zomby(screen, hero, (width * 0.5, 1500))
        #skeleton = Skeleton(screen, hero, (width * 0.8 , 3000))
        #slime = Slime(screen, hero, (width * 0.1, 500))
        boss = Boss(screen, hero, (width * 0.5, 100))
        boss.hitbox.top = self.size[1]

        death_text1 = Text("Ты был их последней надеждой, но теперь надежда мертва.", (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2), True)
        death_text1.color = (255, 0, 0)
        death_text2 = Text("Дьявольский некромант обратил мир в обитель агонии.", (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 50), True)
        death_text2.color = (255, 0, 0)

        win_text1 = Text("Некромант снова был повержен могучей рукой великого воина", (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 3), True)
        win_text2 = Text("Ты спас королевство, и твоё имя навеки останется в сердцах людей", (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 3 + 100), True)
        win_text1.size = win_text2.size = 35

        self.start_text1 = Text("Ужасный некромант, почти уничтоживший весь мир, вернулся, восстав из мёртвых", (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 4), True)
        self.start_text2 = Text("Жаждующий мести, он решил поработить королевство, где некогда был повержен", (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2), True)
        self.start_text3 = Text("Ты единственный, кто может его остановить. На тебе лежит судьба этого мира", (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 4 * 3), True)
        self.gamepad_text = Text("Нажмите start", (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 4 * 3 + 100), False)
        self.start_text1.size = self.start_text2.size = self.start_text3.size = 30
        self.gamepad_text.size = 20

        black_screen = pygame.Surface(SCREEN_SIZE)
        black_screen = black_screen.convert_alpha()
        rect = black_screen.get_rect()
        black_screen.fill((0, 0, 0, 255))
        alpha = 0

        self.camera = Camera(FIELD_SIZE[0], FIELD_SIZE[1], self.size)

        is_started = False

        while True:
            if not is_started:
                self.show_go_screen(screen, black_screen, rect)
                is_started = True
                black_screen.fill((0, 0, 0, 0))

            self.clock.tick(self.FPS)
            now = pygame.time.get_ticks()

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

                if pygame.joystick.get_count():
                    if self.joystick.get_button(4):
                        for sprite in all_sprites:
                            sprite.kill()
                        self.run()

            screen.fill((200, 200, 255))

            self.camera.update(hero.rect)
            #boss.update(self.camera)

            if not hero.is_dead:
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


            screen.blit(black_screen, rect)

            if hero.is_dead and now - hero.death_time > 2000:
                death_text1.draw()
                if death_text1.is_animated:
                    death_text2.draw()

                alpha += 1
                alpha = min(alpha, 255)
                black_screen.fill((0, 0, 0, alpha))

            if boss.is_dead:
                win_text1.draw()
                if win_text1.is_animated:
                    win_text2.draw()

                alpha += 1
                alpha = min(alpha, 255)
                black_screen.fill((0, 0, 0, alpha))

            if not boss.is_showed:
                if hero.hitbox.right > FIELD_SIZE[0] // 2 - 400 and hero.on_ground and hero.hitbox.bottom == FIELD_SIZE[1] * 0.9:
                    hero.can_move = False
                    hero.direction.x = 0
                    hero.stay()
                    boss.show()
            elif hero.death_time == 0:
                hero.can_move = True

            #pygame.draw.rect(screen, (255, 0, 0), background.ground_box_rect, 3)

            #display_fps = str(int(clock.get_fps()))
            #fps.draw(display_fps)

            #show_hitboxes(screen, all_sprites, self.camera)

            pygame.display.update()

    def show_go_screen(self, screen, image, rect):

        waiting = True
        while waiting:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False
                if pygame.joystick.get_count():
                    if self.joystick.get_button(7):
                        waiting = False

            screen.blit(image, rect)
            self.start_text1.draw()
            if self.start_text1.is_animated:
                self.start_text2.draw()
            if self.start_text2.is_animated:
                self.start_text3.draw()
            if self.start_text3.is_animated and pygame.joystick.get_count():
                self.gamepad_text.draw()
            pygame.display.flip()


def show_hitboxes(screen, group, camera):
    for sprite in group:
        pygame.draw.rect(screen, (255, 0, 0), camera.apply(sprite.hitbox), 3)
        pygame.draw.rect(screen, (0, 0, 255), camera.apply(sprite.rect), 3)

if __name__ == "__main__":
    game = GameScreen()
    game.run()
