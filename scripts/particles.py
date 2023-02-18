import pygame
import random
from settings import *


class Particle:
    def __init__(self, pos, color, speed, screen):
        self.x, self.y = (pos[0] + random.randint(-10, 10), pos[1] + random.randint(-10, 10))
        self.color = color
        self.speedX = random.randint(-2, 2)
        self.speedY = speed
        self.gravity = GRAVITY

        self.screen = screen

    def update(self):
        self.x += self.speedX
        self.y -= self.speedY
        self.speedY -= self.gravity

        if self.y > SCREEN_SIZE[1]:
            #self.kill()
            pass

        pygame.draw.rect(self.screen, self.color, (self.x, self.y, 5, 5))


class Particles:
    def __init__(self, pos, color, speed, screen, num=10):
        self.particles = []
        for _ in range(num):
            self.particles += [Particle(pos, color, speed, screen)]

    def update(self):
        for particle in self.particles:
            particle.update()
