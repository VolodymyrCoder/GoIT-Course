import pygame as p
from pygame.constants import QUIT

p.init()

FPS = p.time.Clock()

HEIGHT = 800
WIDTH = 1200

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

main_display = p.display.set_mode((WIDTH, HEIGHT))

player_size = (20, 20)

player = p.Surface(player_size)
player.fill(COLOR_WHITE)
player_rect = player.get_rect()
player_speed = [-11, -13]

playing = True

while playing:
    FPS.tick(120)
    for event in p.event.get():
        if event.type == QUIT:
            playing = False

    main_display.fill(COLOR_BLACK)

    if player_rect.bottom >= HEIGHT or player_rect.top <= 0:
        player_speed[1] = -player_speed[1]

    if player_rect.right >= WIDTH or player_rect.left <= 0:
        player_speed[0] = -player_speed[0]

    main_display.blit(player, player_rect)

    player_rect = player_rect.move(player_speed)

    p.display.flip()