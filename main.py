import os
import sys

import pygame
import requests

base_scale = 0.001
scale_modifier = 1 # scale = base_scale * scale_modifier
scale_change_modifier = 2 # How changes scale_modifier durning work of program

base_cord = [37.530887, 55.703118]
base_cord_change = 0.0005 # cord change = scale_modifier * base_cord_change


def do_map_request(cord, map_scale):
    map_scale = str(map_scale) + ',' + str(map_scale)
    cord = ','.join(list(map(lambda x: str(x), cord)))
    map_request = str("http://static-maps.yandex.ru/1.x/?ll=" + cord + "&spn=" + map_scale + "&l=map")
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
clock = pygame.time.Clock()
running = True
screen.blit(pygame.image.load(do_map_request(base_cord, base_scale * scale_modifier)), (0, 0))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os.remove("map.png")
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            # scale events

            if event.key == pygame.K_PAGEUP and scale_modifier > 1:
                scale_modifier *= (1 /scale_change_modifier)
            elif event.key == pygame.K_PAGEDOWN and scale_modifier < 8192:
                scale_modifier *= scale_change_modifier

            # Moving events
            if event.key == pygame.K_UP and base_cord[1] < 80:
                base_cord[1] += scale_modifier * base_cord_change
            elif event.key == pygame.K_DOWN and base_cord[1] > -80:
                base_cord[1] -= scale_modifier * base_cord_change
            elif event.key == pygame.K_RIGHT and base_cord[0] < 150:
                base_cord[0] += scale_modifier * base_cord_change
            elif event.key == pygame.K_LEFT and base_cord[0] > -150:
                base_cord[0] -= scale_modifier * base_cord_change

            screen.blit(pygame.image.load(do_map_request(base_cord, base_scale * scale_modifier)), (0, 0))
        pygame.display.flip()
pygame.quit()