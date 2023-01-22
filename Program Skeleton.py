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
coins_group = pygame.sprite.Group()

clock = pygame.time.Clock()
pictures = ['']

player_n_speed = 10
player_f_speed = 30
player_x = 100
player_y = 500  # эти две переменные должны быть изменены при загрузке уровня
coins_cords = [pygame.Rect(150, 550, 64, 64)]  # в эту переменную при загрузке уровня помещаются все координаты монеток

player_direction = "right"
player_state = "idle"  # "walking"
FPS = 60


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
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def show_winners_table():
    pass


def terminate():
    pygame.quit()
    sys.exit()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, **kwargs):
        super().__init__(player_group, all_sprites)
        self.frames = {**kwargs}
        self.frames["left"] = pygame.transform.flip(self.frames["right"], True, False)
        self.frames["walking_left"] = [pygame.transform.flip(i, True, False) for i in self.frames["walking_right"]]
        self.x = x
        self.y = y
        self.animation_timer = 0
        self.animation_speed = 10
        self.image_index = 0
        self.image = self.frames[player_direction]
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self):
        self.rect = self.image.get_rect().move(self.x, self.y)
        if player_state == "walking":
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.image_index = (self.image_index + 1) % len(self.frames["walking_right"])
            self.image = self.frames[f"walking_{player_direction}"][self.image_index]
        else:
            self.image = self.frames[player_direction]
            self.animation_timer = 0
            self.image_index = 0


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet, columns, rows, coin_size):
        super().__init__(coins_group, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows, coin_size)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.animation_timer = 0
        self.animation_speed = 10

    def cut_sheet(self, sheet, columns, rows, coin_size):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)), coin_size))

    def update(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


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


# start_screen()
player = Player(player_x, player_y, right=load_image("char/sprite_00.png"),
                walking_right=[load_image("char/sprite_01.png"),
                               load_image("char/sprite_02.png"),
                               load_image("char/sprite_03.png"),
                               load_image("char/sprite_04.png")])
coins = [Coin(c.x, c.y, load_image("coin.png"), 6, 1, c.size) for c in coins_cords]
camera = Camera()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
            break
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # влево (A или <-)
        if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
            player.x -= player_f_speed
            player_state = 'running'
        else:
            player.x -= player_n_speed
            player_state = 'walking'
        player_direction = "left"
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # вправо (D или ->)
        if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
            player.x += player_f_speed
            player_state = 'running'
        else:
            player.x += player_n_speed
            player_state = 'walking'
        player_direction = "right"
    if not (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
        player_state = "idle"
    screen.fill('white')
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)
