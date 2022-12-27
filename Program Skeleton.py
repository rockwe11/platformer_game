import pygame
import os
import sys
import random
import math

pygame.init()
size = WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode(size)
screen.fill('white')

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
clock = pygame.time.Clock()
pictures = ['']
player_n_speed = 50
player_f_speed = 80


def load_image(name, colorkey=None):
    fullname = os.path.join('Animations', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as error_message:
        print('Невозможно загрузить картинку:', name)
        raise SystemExit(error_message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is None:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def generate_level(level_name):
    new_player, pos_x, pos_y = None, None, None
    pass


def start_screen():
    pass


def show_winners_table():
    pass


def terminate():
    pygame.quit()
    sys.exit()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        pass

    def update(self):
        pass


class Camera:
    pass


class Floor(pygame.sprite.Sprite):
    pass


class Walls(pygame.sprite.Sprite):
    pass


class Spikes(pygame.sprite.Sprite):
    pass


class Door(pygame.sprite.Sprite):
    pass


camera = Camera()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
            break

    screen.fill('white')
