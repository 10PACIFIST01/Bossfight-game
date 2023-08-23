import pygame
import os

pygame.init()
default_font_name = os.path.join("fonts", "pixel2.ttf")
default_font_name = os.path.join("..", default_font_name)


class Text:
    def __init__(self, text, pos, animate=False,  font=default_font_name):
        self.size = 40

        self.text = str(text)
        self.font_name = font
        self.font = pygame.font.Font(self.font_name, self.size)

        self.color = (255, 255, 255)
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.surf = pygame.display.get_surface()

        # for animation
        self.animate = animate
        self.is_animated = False
        self.last_update = pygame.time.get_ticks()
        self.count = 0
        self.new_text = ""

    def create_animation(self, frame_rate):
        now = pygame.time.get_ticks()
        if now - self.last_update > frame_rate and self.count < len(self.text):
            self.last_update = now
            self.new_text += self.text[self.count]

            pos = self.rect.center
            self.image = self.font.render(self.new_text, True, self.color)
            self.rect = self.image.get_rect()
            self.rect.center = pos

            self.count += 1

            if self.count == len(self.text):
                self.is_animated = True

    def update(self):
        self.font = pygame.font.Font(self.font_name, self.size)
        if self.animate:
            self.create_animation(100)

    def draw(self):
        self.update()
        self.surf.blit(self.image, self.rect)

