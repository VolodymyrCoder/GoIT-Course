from random import randint
import os

import pygame as p
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP, QUIT

p.init()

FPS = p.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = p.font.SysFont('Verdana', 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)

main_display = p.display.set_mode((WIDTH, HEIGHT))

bg = p.transform.scale(p.image.load('background.png'), (WIDTH, HEIGHT))
bg_x1 = 0
bg_x2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player = p.image.load('player.png').convert_alpha()
player_rect = p.Rect(0, HEIGHT / 2 - 76, 182, 76)
player_move_down = [0, 8]
player_move_up = [0, -8]
player_move_left = [-8, 0]
player_move_right = [8, 0]


def create_enemy():
    enemy = p.image.load('enemy.png').convert_alpha()
    rect = p.Rect(WIDTH, randint(72, HEIGHT - 72), 205, 72)
    move = [randint(-8, -4), 0]
    return {
        'enemy': enemy,
        'rect': rect,
        'move': move
    }


CREATE_ENEMY = p.USEREVENT + 1
p.time.set_timer(CREATE_ENEMY, 4500)

enemies = []


def create_bonus():
    bonus = p.image.load('bonus.png').convert_alpha()
    rect = p.Rect(randint(179, WIDTH - 179), 0, 179, 298)
    move = [0, randint(4, 8)]
    return {
        'bonus': bonus,
        'rect': rect,
        'move': move
    }


CREATE_BONUS = p.USEREVENT + 2
p.time.set_timer(CREATE_BONUS, 6000)

bonuses = []

score = 0

CHANGE_IMAGE = p.USEREVENT + 3
p.time.set_timer(CHANGE_IMAGE, 200)

image_index = 0

playing = True

while playing:
    FPS.tick(120)
    for event in p.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = p.image.load(os.path.join(
                IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    bg_x1 -= bg_move
    bg_x2 -= bg_move

    if bg_x1 < -bg.get_width():
        bg_x1 = bg.get_width()

    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()

    main_display.blit(bg, (bg_x1, 0))
    main_display.blit(bg, (bg_x2, 0))

    keys = p.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    for enemy in enemies:
        enemy['rect'] = enemy['rect'].move(enemy['move'])
        main_display.blit(enemy['enemy'], enemy['rect'])
        if enemy['rect'].left < 0:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy['rect']):
            playing = False

    for bonus in bonuses:
        bonus['rect'] = bonus['rect'].move(bonus['move'])
        main_display.blit(bonus['bonus'], bonus['rect'])
        if bonus['rect'].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus['rect']):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True,
                      COLOR_BLACK), (WIDTH - 50, 20))
    main_display.blit(player, player_rect)

    p.display.flip()
