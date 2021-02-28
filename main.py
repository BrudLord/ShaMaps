import os
import sys
import requests
import pygame


class Button:
    def __init__(self, width, height, x, y, name):
        self.width = width
        self.height = height
        self.inactive_color = (41, 150, 150)
        self.active_color = (9, 190, 150)
        self.name = name
        self.x = x
        self.y = y

    def draw(self):
        x = self.x
        y = self.y
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        global map_vid
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
            if click[0] == 1:
                pygame.time.delay(150)
                # Смена окна
                if self.name == 'Схема':
                    map_vid = 'map'
                if self.name == 'Спутник':
                    map_vid = 'sat'
                if self.name == 'Гибрид':
                    map_vid = 'sat,skl'
        else:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
        if len(self.name) == 1:
            print_text(self.name, x, y, self.width, self.height)
        else:
            print_text(self.name, x, y, self.width, self.height)


def print_text(message, x, y, button_width, button_height, font_color=(0, 0, 0), font_type='Marta_Decor_Two.ttf',
               font_size=13):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x + button_width // 2 - text.get_width() // 2, y + button_height // 2 - text.get_height() // 2))


base_scale = 0.001
scale_modifier = 1 # scale = base_scale * scale_modifier
scale_change_modifier = 2 # How changes scale_modifier durning work of program
base_cord = [37.530887, 55.703118]
base_cord_change = 0.0005 # cord change = scale_modifier * base_cord_change
map_vid = 'map'


def do_map_request(cord, map_scale):
    map_scale = str(map_scale) + ',' + str(map_scale)
    cord = ','.join(list(map(lambda x: str(x), cord)))
    map_request = str("http://static-maps.yandex.ru/1.x/?ll=" + cord + "&spn=" + map_scale + "&l=" + map_vid)
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
buttons = [Button(35, 35, 10, 10, 'Схема'), Button(35, 35, 55, 10, 'Спутник'), Button(35, 35, 100, 10, 'Гибрид')]
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
    for i in buttons:
        i.draw()
    pygame.display.flip()
pygame.quit()