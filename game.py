import random

import pygame as p
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

p.init()

FPS = p.time.Clock()

HEIGHT = 800
WIDTH = 1200

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)

main_display = p.display.set_mode((WIDTH, HEIGHT))

player_size = (20, 20)

player = p.Surface(player_size)
player.fill(COLOR_WHITE)
player_rect = player.get_rect()
player_move_down = [0, 1]
player_move_up = [0, -1]
player_move_left = [-1, 0]
player_move_right = [1, 0]


def create_enemy():
    enemy_size = (30, 30)
    enemy = p.Surface(enemy_size)
    enemy.fill(COLOR_BLUE)
    rect = p.Rect(WIDTH, random.randint(0, HEIGHT), *enemy_size)
    move = [random.randint(-6, -1), 0]
    return {
        'enemy': enemy,
        'rect': rect,
        'move': move
    }


CREATE_ENEMY = p.USEREVENT + 1
p.time.set_timer(CREATE_ENEMY, 1500)

enemies = []


def create_bonus():
    bonus_size = (30, 30)
    bonus = p.Surface(bonus_size)
    bonus.fill(COLOR_GREEN)
    rect = p.Rect(random.randint(0, WIDTH), 0, *bonus_size)
    move = [0, random.randint(1, 6)]
    return {
        'bonus': bonus,
        'rect': rect,
        'move': move
    }


CREATE_BONUS = p.USEREVENT + 2
p.time.set_timer(CREATE_BONUS, 1500)

bonuses = []

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

    main_display.fill(COLOR_BLACK)

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

    for bonus in bonuses:
        bonus['rect'] = bonus['rect'].move(bonus['move'])
        main_display.blit(bonus['bonus'], bonus['rect'])
        if bonus['rect'].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(player, player_rect)

    p.display.flip()
