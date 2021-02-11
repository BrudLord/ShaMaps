import os
import sys

import pygame
import requests

base_scale = 0.001
scale_modifier = 1


def do_map_request(map_scale):
    map_scale = str(map_scale) + ',' + str(map_scale)
    map_request = str("http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&spn=" + map_scale + "&l=map")
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
screen.blit(pygame.image.load(do_map_request(base_scale * scale_modifier)), (0, 0))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os.remove("map.png")
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == 1073741899 and scale_modifier > 1:
                scale_modifier *= 0.5
            elif event.key == 1073741902 and scale_modifier < 4096:
                scale_modifier += scale_modifier
            print(scale_modifier, end='->')
            screen.blit(pygame.image.load(do_map_request(base_scale * scale_modifier)), (0, 0))
        pygame.display.flip()
pygame.quit()