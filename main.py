import pygame
import pygame_gui

from window import Window


from assets import WINDOW_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    manager = pygame_gui.UIManager(WINDOW_SIZE)

    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, manager)

    clock = pygame.time.Clock()
    running = True
    while running:
        time_delta = clock.tick(60) / 1000

        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                manager.process_events(event)
                window.events_processing(event)

            window.render(screen, time_delta)
        except Exception:
            pass
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
