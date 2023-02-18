import pygame


class Camera:
    def __init__(self, width, height, size):
        self.map = pygame.Rect(0, 0, width, height)
        self.size = size
    
    def configure(self, camera, target_pos, size):
        x, y = -target_pos[0] + size[0] / 2, -target_pos[1] + size[1] / 2
        w, h = camera.width, camera.height

        x = min(0, x)
        x = max(-(camera.width - size[0]), x)
        y = max(-(camera.height - size[1]), y)
        y = min(0, y)

        return pygame.Rect(x, y, w, h)
    
    def apply(self, sprite_rect):
        return sprite_rect.move(self.map.topleft)
    
    def update(self, target_rect):
        self.map = self.configure(self.map, target_rect.center, self.size)
