import pygame

from request import get_response
from assets import load_image


class Window:
    def __init__(self, width, height):
        self.background_color = (255, 255, 255)
        self.coords = "30.316526,59.9400798"
        self.map_scale = "0.6,0.6"
        self.mode = "map"
        self.current_image = get_response(self.coords, self.map_scale, self.mode)

    def render(self, screen):
        screen.fill(self.background_color)

        font = pygame.font.Font(None, 24)
        text = font.render(f"текущий уровень:", 1, (0, 0, 0))
        screen.blit(text, (20, 20))

    def events_processing(self, event):
        pass
