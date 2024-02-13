import pygame
import requests

from assets import WINDOW_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from request import get_response, geocoder_request
import pygame_gui


class Window:
    def __init__(self, width, height, manager):
        self.background_color = (255, 255, 255)

        self.coords = "30.316526,59.9400798"
        self.map_scale = "0.6,0.6"
        self.mode = "map"
        self.point_coords = None
        self.get_image()
        self.current_image = "map_image/map.png"
        self.current_image = "map_image/map.png"
        self.request_message = None
        self.include_postal_code = False

        # pygame_gui settings
        self.manager = manager
        self.search_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 50), (100, 30)),
            text="Поиск",
            manager=self.manager,
        )
        self.request_line = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, 10), (400, 30)),
            manager=self.manager
        )
        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((250, 50), (100, 30)),
            text="Сброс",
            manager=self.manager,
        )
        self.output = pygame_gui.elements.UITextBox(
            html_text="",
            relative_rect=pygame.Rect((0, 130), (400, 80)),
            manager=self.manager,
        )
        self.postal_code = pygame_gui.elements.UIDropDownMenu(
            options_list=["ВКЛЮЧИТЬ отображение почтового индекса", "ВЫКЛЮЧИТЬ отображение почтового индекса"],
            starting_option="ВЫКЛЮЧИТЬ отображение почтового индекса",
            relative_rect=pygame.Rect((0, 220), (400, 30)),
            manager=self.manager
        )

    def get_image(self):
        map_file = "map_image/map.png"
        is_succes, response = get_response(self.coords, self.map_scale, self.mode, self.point_coords)
        if not is_succes:
            print("Http статус:", response.status_code, "(", response.reason, ")")
        else:
            with open(map_file, "wb") as file:
                file.write(response.content)

    def render(self, screen, time_delta):
        self.manager.update(time_delta)
        screen.fill(self.background_color)
        screen.blit(pygame.image.load(self.current_image), (400, 0))

        # font = pygame.font.Font(None, 24)
        # text = font.render(f"текущий уровень:", 1, (0, 0, 0))
        # screen.blit(text, (20, 20))
        self.manager.draw_ui(screen)

    def events_processing(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP and float(self.map_scale.split(",")[0]) > 0.002:
                self.map_scale = (f"{str(float(self.map_scale.split(',')[0]) * 0.5)},"
                                  f"{str(float(self.map_scale.split(',')[1]) * 0.5)}")
            if event.key == pygame.K_PAGEDOWN and float(self.map_scale.split(",")[0]) < 20:
                self.map_scale = (f"{str(float(self.map_scale.split(',')[0]) / 0.5)},"
                                  f"{str(float(self.map_scale.split(',')[1]) / 0.5)}")
            self.get_image()

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                self.request_message = event.text
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.search_button:
                    self.searching()
                    self.get_image()
                if event.ui_element == self.reset_button:
                    self.point_coords = False
                    self.addrress_output(kill=True)
                    self.get_image()
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if self.postal_code.selected_option.split()[0] == "ВКЛЮЧИТЬ":
                    self.include_postal_code = True
                else:
                    self.include_postal_code = False
                #self.addrress_output(self.include_postal_code)

    def searching(self):
        if self.request_message:
            is_succes, coords = geocoder_request(self.request_message)
            if not is_succes:
                print("GEOCODER ERROR")
            else:
                self.coords = f"{coords.split(' ')[0]},{coords.split(' ')[1]}"
                self.point_coords = self.coords
                self.addrress_output(self.include_postal_code)

    def addrress_output(self, include_postal_code=False, kill=False):
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b"\
                           f"&geocode={self.request_message}&format=json"

        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()

            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]

            self.output.append_html_text(toponym_address)

            if include_postal_code:
                self.output.clear()
                toponym_postal_code = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
                self.output.append_html_text(f'{toponym_address}, {toponym_postal_code}')

            if kill:
                self.output.clear()

        else:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")