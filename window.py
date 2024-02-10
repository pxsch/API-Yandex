import pygame

from assets import WINDOW_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from request import get_response
from assets import load_image


class Window:
    def __init__(self, width, height):
        self.background_color = (255, 255, 255)
        self.coords = "30.316526,59.9400798"
        self.map_scale = "0.6,0.6"
        self.mode = "map"
        self.get_image()
        self.current_image = "map_image/map.png"

    def get_image(self):
        map_file = "map_image/map.png"
        is_succes, response = get_response(self.coords, self.map_scale, self.mode)
        if not is_succes:
            print("Http статус:", response.status_code, "(", response.reason, ")")
        else:
            with open(map_file, "wb") as file:
                file.write(response.content)

    def render(self, screen):
        screen.fill(self.background_color)
        screen.blit(pygame.image.load(self.current_image), (0, 0))

        # font = pygame.font.Font(None, 24)
        # text = font.render(f"текущий уровень:", 1, (0, 0, 0))
        # screen.blit(text, (20, 20))

    def events_processing(self, event):
        pass


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            window.events_processing(event)

        window.render(screen)
        pygame.display.flip()
    pygame.quit()