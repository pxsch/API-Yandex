import os
import sys
import pygame
import requests
from math import log


def search(coords="город Мадурай"):
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
    x1, y1 = 18.279018, 0.3
    x2, y2 = 37.85515, 49.992119
    map_request = (f"http://static-maps.yandex.ru/1.x/?pt={x},{y},pm2lbm~{x1},{y1},pm2lbm~{x2},{y2},pm2lbm&ll={x},{y}&"
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
    z = int(input())
    coodrinates = search()
    img(coodrinates, z)
    kx = 172 / 0.2374 * 2 ** (z - 10)
    ky = abs(199 / (0.024029 - 0.3) * 2 ** (z - 10))
    print("K:", ky)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))

    clock = pygame.time.Clock()
    running = True
    x, y = map(float, coodrinates.split())
    c = 1
    while running:

        screen.blit(pygame.image.load("map.png"), (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x2p, y2p = event.pos
                x2 = (x2p - 300) / kx + x
                k = abs(ky - abs((0 - y) ** 1.9) * 2 ** (z - 10))     # 36 44
                print(k)
                y2 = (450 - y2p - 225) / k + y
                print(">>", y2)
                print("pos", event.pos)
                c += 1
                x = x2
                y = y2
                print("msc", 37.617698, 55.755864)
                print("cor", 37.617698, 49.992119)
                print("new", x, y)
                print("c:", c)
                print()
                img(f"{x} {y}", z)
        pygame.display.flip()
    pygame.quit()
    os.remove("map.png")
