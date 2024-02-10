import pygame

from window import Window


from assets import WINDOW_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, FPS


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)

    clock = pygame.time.Clock()
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            window.events_processing(event)

        window.render(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
