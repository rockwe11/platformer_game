import pygame
import os
import sys
import random
import math

pygame.init()
size = WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill('white')
font = pygame.font.Font(pygame.font.get_default_font(), 24)
colors = {"BROWN": pygame.color.Color("#d18a66")}

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()  # Новая группа для пола

clock = pygame.time.Clock()
pictures = ['']

player_n_speed = 8
player_f_speed = 13

player_direction = "right"
player_state = "idle"  # "walking"
FPS = 60
GRAVITY = 3


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


player_images = {"right": load_image("char/sprite_00.png"),
                "walking_right": [load_image("char/sprite_05.png"),
                                  load_image("char/sprite_01.png"),
                                  load_image("char/sprite_06.png")],
                "running_right": [load_image("char/sprite_01.png"),
                                  load_image("char/sprite_02.png"),
                                  load_image("char/sprite_03.png"),
                                  load_image("char/sprite_04.png")],
                "jumping_right": [load_image("char/sprite_07.png"),
                                  load_image("char/sprite_08.png"),
                                  load_image("char/sprite_09.png")]}


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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            terminate()  # <- быстрый выход для временной отладки приложения на кнопку Backspace
            break

        pygame.display.flip()
        clock.tick(FPS)


def show_winners_table():
    pass


def terminate():
    pygame.quit()
    sys.exit()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__(player_group, all_sprites)
        self.frames = images
        self.frames["left"] = pygame.transform.flip(self.frames["right"], True, False)
        self.frames["walking_left"] = [pygame.transform.flip(i, True, False) for i in self.frames["walking_right"]]
        self.frames["jumping_left"] = [pygame.transform.flip(i, True, False) for i in self.frames["jumping_right"]]
        self.frames["running_left"] = [pygame.transform.flip(i, True, False) for i in self.frames["running_right"]]
        self.x = x
        self.y = y
        self.animation_timer = 0
        self.walking_speed = 7
        self.running_speed = 10
        self.image_index = 0
        self.isJump = False
        self.jumpCount = 20
        self.image = self.frames[player_direction]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self):
        self.rect = self.image.get_rect().move(self.x, self.y)
        if player_state == "walking":
            self.animation_timer += 1
            if self.animation_timer >= self.walking_speed:
                self.animation_timer = 0
                self.image_index = (self.image_index + 1) % len(self.frames["walking_right"])
            self.image = self.frames[f"walking_{player_direction}"][self.image_index]
        elif player_state == "running":
            self.animation_timer += 1
            if self.animation_timer >= self.running_speed:
                self.animation_timer = 0
                self.image_index = (self.image_index + 1) % len(self.frames["running_right"])
            self.image = self.frames[f"running_{player_direction}"][self.image_index]
        elif player_state == "idle":
            self.image = self.frames[player_direction]
            self.animation_timer = 0
            self.image_index = 0

        if self.isJump:
            if self.jumpCount == 20:
                self.image = self.frames[f"jumping_{player_direction}"][0]
            elif self.jumpCount == 12:
                self.image = self.frames[f"jumping_{player_direction}"][1]
            elif self.jumpCount == -15:
                self.image = self.frames[f"jumping_{player_direction}"][2]
            if self.jumpCount >= -20:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= self.jumpCount ** 2 * 0.1 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 20
        self.mask = pygame.mask.from_surface(self.image)

    def jump(self):
        pass


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet, columns, rows, coin_size):
        super().__init__(coins_group, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows, coin_size)
        self.masks = [pygame.mask.from_surface(x) for x in self.frames]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = self.masks[self.cur_frame]
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
        self.mask = self.masks[self.cur_frame]


class Camera:
    pass


# попытка создать зеленый пол просто прямоугольником, но нужно именно картинкой
class Floor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))


class Walls(pygame.sprite.Sprite):
    pass


class Spikes(pygame.sprite.Sprite):
    pass


class Door(pygame.sprite.Sprite):
    pass


# start_screen()

floor = Floor()

# ======================================================================================
# Данные при загрузке уровня

player_x = 100
player_y = 500

coins_cords = [pygame.Rect(250, 550, 64, 64),
               pygame.Rect(350, 550, 64, 64),
               pygame.Rect(350, 500, 64, 64),
               pygame.Rect(450, 550, 64, 64),
               pygame.Rect(450, 500, 64, 64),
               pygame.Rect(550, 550, 64, 64),
               pygame.Rect(550, 500, 64, 64)
               ]

coins_collected = 0

player = Player(player_x, player_y, player_images)
coins = [Coin(c.x, c.y, load_image("coin.png"), 6, 1, c.size) for c in coins_cords]
one_coin_image = load_image("coin.png").subsurface(pygame.Rect((0, 0), (32, 32)))

# ======================================================================================
camera = Camera()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
            break
    keys = pygame.key.get_pressed()
    ####################################################################################
    if keys[pygame.K_BACKSPACE]:
        terminate()  # <- быстрый выход для временной отладки приложения на кнопку Backspace
        break
    #####################################################################################
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # влево (A или <-)
        if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
            player.x -= player_f_speed
            if not player.isJump:
                player_state = 'running'
        else:
            player.x -= player_n_speed
            if not player.isJump:
                if player_state == "running":
                    player.image_index = 0
                player_state = 'walking'
        player_direction = "left"
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # вправо (D или ->)
        if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
            player.x += player_f_speed
            if not player.isJump:
                player_state = 'running'
        else:
            player.x += player_n_speed
            if not player.isJump:
                player_state = 'walking'
        player_direction = "right"
    ###############################################
    if keys[pygame.K_SPACE]:
        player.isJump = True
        player_state = "jumping"
    ###############################################
    if not (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not (keys[pygame.K_d] or keys[pygame.K_RIGHT])\
            and not player.isJump:
        player_state = "idle"

    for c in coins:
        if pygame.sprite.collide_mask(player, c):
            c.kill()
            coins.remove(c)
            coins_collected += 1

    screen.fill('white')

    # интерфейс
    screen.blit(one_coin_image, (10, 10))
    score_text = font.render(str(coins_collected), True, colors["BROWN"])
    score_text_rect = score_text.get_rect()
    score_text_rect.topleft = (42, 15)
    screen.blit(score_text, score_text_rect)

    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)
