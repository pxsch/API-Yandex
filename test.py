import os
import sys
import pygame
import requests
from math import log


def search(coords="Москва"):
    toponym_coodrinates = None

    search_address = coords
    geocoder_request = "https://geocode-maps.yandex.ru/1.x/" \
                       "?apikey=40d1649f-0493-4b70-98ba-98533de7710b" \
                       f"&geocode={search_address}&format=json"

    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        print(toponym_coodrinates)
        return toponym_coodrinates
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")


def img(coords, z):
    x, y = coords.split(" ")
    map_request = (f"http://static-maps.yandex.ru/1.x/?ll={x},{y}&"
                   f"z={z}&l=map")
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


while True:
    z = input()
    coodrinates = search()
    img(coodrinates, z)

    pygame.init()
    screen = pygame.display.set_mode((600, 450))

    clock = pygame.time.Clock()
    running = True
    while running:

        screen.blit(pygame.image.load("map.png"), (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                z = int(z)
                step_x = int(2 ** (z + 8) / 600)
                step_y = int(2 ** (z + 8) / 450)
                print(step_x, step_y)
                print((event.pos[0] - 300) / abs(event.pos[0] - 300) * abs(event.pos[0] - 300))
                print((600 - event.pos[1] - 300) / abs(600 - event.pos[1] - 300) * abs(450 - event.pos[1] - 225))
                y = float(coodrinates.split()[1]) + int((event.pos[0] - 225) / (event.pos[0] - 225)) * log(abs(event.pos[0] - 300) * step_x, 2) - 8
                x = float(coodrinates.split()[0]) + int((600 - event.pos[1] - 300) / (600 - event.pos[1] - 300)) * log(abs(450 - event.pos[1] - 225) * step_y, 2) - 8
                print(x,y)
                img(f"{x} {y}", z)
        pygame.display.flip()
    pygame.quit()
    os.remove("map.png")
