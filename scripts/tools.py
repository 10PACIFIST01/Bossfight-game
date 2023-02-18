import pygame
import os


def load_img_folder(name, is_image=True):
    img_folder = os.path.join(os.path.split(os.path.dirname(__file__))[0], "sprites")
    enemy_folder = os.path.join(img_folder, name)
    if is_image:
        enemy_img_folder = os.path.join(enemy_folder, f"default_{name}.png")
        return enemy_img_folder
    else:
        return enemy_folder


def load_animation(num, name, type, scale=3, form=".png"):
    images = []
    for i in range(num):
        fold_path = os.path.join(load_img_folder(type, False), name)
        img_path = os.path.join(fold_path, name + str(i) + form)
        image = pygame.image.load(img_path).convert_alpha()
        image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        images += [image]
    return images


def gradient(num, x, y, k, l):
    coof1 = x / y
    coof2 = 1 / (l - k)
    result = coof1 / coof2 * num
    return result


def set_color(image, color, alpha=None):
    for x in range(0, image.get_width(), 2):
        for y in range(0, image.get_height(), 2):
            if image.get_at((x, y)).a > 0 and alpha:
                color.a = alpha
            else:
                color.a = image.get_at((x, y)).a
            image.set_at((x, y), color)


def get_player_direction(self, player):
    self_vec = pygame.math.Vector2(self.rect.center)
    player_vec = pygame.math.Vector2(player.hitbox.center)
    distance = get_player_distance(self, player)

    if distance > 0:
        direction = (player_vec - self_vec).normalize()
    else:
        direction = pygame.math.Vector2()

    return direction


def get_player_distance(self, player):
    self_vec = pygame.math.Vector2(self.rect.center)
    player_vec = pygame.math.Vector2(player.rect.center)
    distance = (player_vec - self_vec).magnitude()

    return distance
