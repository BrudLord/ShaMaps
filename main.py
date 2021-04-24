import os
import sys
import requests
import pygame


class InputBox:
    def __init__(self):
        self.rect = pygame.Rect(10, 50, 90, 35)
        self.color = pygame.Color(9, 190, 150)
        self.text = ''
        self.active = True
        self.x = 10
        self.y = 50
        self.w = 100
        self.h = 35

    def handle_event(self, k):
        if self.active:
            if pygame.key.name(k) == 'return':
                self.text = ''
            elif pygame.key.name(k) == 'backspace':
                self.text = self.text[:-1]
            else:
                if pygame.key.name(k) == 'space':
                    self.text += ' '
                elif len(pygame.key.name(k)) == 1:
                    if pygame.key.name(k) in '''`qwerttyuiop[]asdfghjkl;'zxcvbnm,./''':
                        j = 'ёйцукенгшщзхъфывапролджэячсмитьбю.'[
                            '''`qwertyuiop[]asdfghjkl;'zxcvbnm,./'''.index(pygame.key.name(k))]
                        self.text += j
                    elif pygame.key.name(k).isdigit():
                        self.text += pygame.key.name(k)

    def draw(self):
        pygame.draw.rect(screen, pygame.Color(150, 150, 150), (self.x, self.y, self.w, self.h))
        print_text(self.text, self.x, self.y, self.w, self.h)
        # Blit the rect.
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), 2)


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
        global base_cord
        global map_point
        global is_map_point, is_pochta
        global is_find_oc
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
                elif self.name == 'Спутн':
                    map_vid = 'sat'
                elif self.name == 'Гибрид':
                    map_vid = 'sat,skl'
                elif self.name == 'Почта':
                    is_pochta = not is_pochta
                    buttons[-1].draw()
                    pygame.display.flip()
                elif self.name == 'Клик':
                    is_find_oc = not is_find_oc
                elif self.name == 'Сборс':
                    is_map_point = False
                    buttons[-1].txt = ''
                    screen.blit(pygame.image.load(do_map_request(base_cord, base_scale * scale_modifier)), (0, 0))
                    pygame.display.flip()
                elif self.name == 'F':
                    bc = base_cord[:]
                    try:
                        base_cord = [float(i) for i in find_coords(ib.text).split()]
                        is_map_point = True
                        map_point = base_cord.copy()
                        buttons[-1].txt = find_address(ib.text)
                        screen.blit(pygame.image.load(do_map_request(base_cord, base_scale * scale_modifier)), (0, 0))
                        pygame.display.flip()
                    except Exception:
                        base_cord = bc
        else:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
            pygame.time.delay(5)
        if len(self.name) == 1:
            print_text(self.name, x, y, self.width, self.height)
        else:
            print_text(self.name, x, y, self.width, self.height)


class Pole:
    def __init__(self, width, height, x, y, name):
        self.width = width
        self.height = height
        self.inactive_color = (200, 200, 200)
        self.active_color = self.inactive_color[:]
        self.name = name
        self.x = x
        self.y = y

    def draw(self):
        x = self.x
        y = self.y
        pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
        try:
            if is_pochta and str(find_pochta(ib.text)).isdigit():
                print_text(self.txt + str(find_pochta(ib.text)), x, y, self.width, self.height)
            else:
                print_text(self.txt, x, y, self.width, self.height)
        except Exception:
            pass


def print_text(message, x, y, button_width, button_height, font_color=(0, 0, 0), font_type='Marta_Decor_Two.ttf',
               font_size=18):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x + button_width // 2 - text.get_width() // 2, y + button_height // 2 - text.get_height() // 2))


base_scale = 0.001
scale_modifier = 1  # scale = base_scale * scale_modifier
scale_change_modifier = 2  # How changes scale_modifier durning work of program
base_cord = [37.530887, 55.703118]
base_cord_change = 0.0005  # cord change = scale_modifier * base_cord_change
map_vid = 'map'
ib = InputBox()
is_find_oc = False
text_from_click = ''

map_point = [37.530887, 55.703118]
is_map_point = False

#######################################################################
########################################################################
##############################################################################################################################################
########################################################################
##############################################################################################################################################
########################################################################
##############################################################################################################################################
########################################################################
##############################################################################################################################################
########################################################################
##############################################################################################################################################
########################################################################
##############################################################################################################################################
########################################################################
##############################################################################################################################################
########################################################################
##############################################################################################################################################
########################################################################
##############################################################################################################################################
########################################################################
##############################################################################################################################################
########################################################################
##############################################################################################################################################
########################################################################
##############################################################################################################################################
########################################################################
##############################################################################################################################################
########################################################################
#######################################################################
#######################################################################
########################################################################
#######################################################################
#######################################################################
########################################################################
#######################################################################
#######################################################################
########################################################################
#######################################################################
#######################################################################
########################################################################
#######################################################################
def find_on_click(pos):
    global base_cord
    global base_cord_change
    global is_map_point
    global map_point
    global scale_modifier
    global is_pochta
    global text_from_click
    is_map_point = True
    base_cord1 = base_cord.copy()
    if pos[0] != 300:
        base_cord1[0] += round((base_cord_change * scale_modifier * 3.2) * ((pos[0] - 300) / 300), 8)
    if pos[1] != 225:
        base_cord1[1] -= round((base_cord_change * scale_modifier * 1.36) * ((pos[1] - 225) / 225), 8)
    map_point = base_cord1
    out = find_address(','.join(map(lambda x: str(x), base_cord1)))
    if is_pochta:
        try:
            out = find_pochta(','.join(map(lambda x: str(x), base_cord1))) + ', ' + out
        except Exception:
            pass
    text_from_click = out
    print(text_from_click) # Если что, text_from_click - глобальная переменная, ее выводить и надо.


########################################################################
#######################################################################
########################################################################
#######################################################################
#######################################################################
########################################################################
#######################################################################
#######################################################################
########################################################################
#######################################################################
#######################################################################
########################################################################
#######################################################################
#######################################################################
########################################################################
#######################################################################
##############################################################################################################################################
########################################################################
##############################################################################################################################################
########################################################################
##############################################################################################################################################
########################################################################
##############################################################################################################################################
########################################################################
#######################################################################
########################################################################
#######################################################################


def do_map_request(cord, map_scale):
    global is_map_point
    global map_point
    global point
    map_scale = str(map_scale) + ',' + str(map_scale)
    cord = ','.join(list(map(lambda x: str(x), cord)))
    point_cord = ','.join(list(map(lambda x: str(x), map_point)))
    map_request = str("http://static-maps.yandex.ru/1.x/?ll=" + cord + "&spn=" + map_scale + "&l=" + map_vid)
    if is_map_point:
        map_request += "&pt=" + point_cord + ",pm2rdm"
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


def find_coords(txt):
    toponym_to_find = txt
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    return toponym["Point"]["pos"]


def find_address(txt):
    toponym_to_find = txt
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    adress = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]['metaDataProperty']['GeocoderMetaData']['text']
    return adress


def find_pochta(txt):
    toponym_to_find = txt
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
        "GeocoderMetaData"]["Address"]["postal_code"]
    return toponym


# Инициализируем pygame
buttons = [Button(35, 35, 10, 10, 'Схема'), Button(35, 35, 55, 10, 'Спутн'), Button(35, 35, 100, 10, 'Гибрид'),
           Button(15, 35, 120, 50, 'F'), Button(35, 35, 560, 410, 'Сборс'), Button(35, 35, 560, 365, 'Почта'),
           Button(35, 35, 560, 325, 'Клик'),
           Pole(450, 35, 145, 10, 'Address')]
pygame.init()
screen = pygame.display.set_mode((600, 450))
clock = pygame.time.Clock()
running = True
renew = True
is_pochta = False
screen.blit(pygame.image.load(do_map_request(base_cord, base_scale * scale_modifier)), (0, 0))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os.remove("map.png")
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            ib.handle_event(event.key)
            # scale events
            if event.key == pygame.K_PAGEUP and scale_modifier > 1:
                scale_modifier *= (1 / scale_change_modifier)
                renew = True
            elif event.key == pygame.K_PAGEDOWN and scale_modifier < 8192:
                scale_modifier *= scale_change_modifier
                renew = True
            # Moving events
            if event.key == pygame.K_UP and base_cord[1] < 80:
                base_cord[1] += scale_modifier * base_cord_change
                renew = True
            elif event.key == pygame.K_DOWN and base_cord[1] > -80:
                base_cord[1] -= scale_modifier * base_cord_change
                renew = True
            elif event.key == pygame.K_RIGHT and base_cord[0] < 150:
                base_cord[0] += scale_modifier * base_cord_change
                renew = True
            elif event.key == pygame.K_LEFT and base_cord[0] > -150:
                base_cord[0] -= scale_modifier * base_cord_change
                renew = True
            if renew:
                screen.blit(pygame.image.load(do_map_request(base_cord, base_scale * scale_modifier)), (0, 0))
                renew = False
            for i in buttons:
                i.draw()
            ib.draw()
            pygame.display.flip()
        for i in buttons:
            i.draw()
        ib.draw()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_find_oc:
                find_on_click(event.pos)
            screen.blit(pygame.image.load(do_map_request(base_cord, base_scale * scale_modifier)), (0, 0))
        pygame.display.flip()
pygame.quit()
