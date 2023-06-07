import pygame
from pylame.components import LameUI

window_width, window_height = 1024, 768

pygame.init()
screen = pygame.display.set_mode(
    (window_width, window_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
FPS = 60


background_color = (22, 22, 22)

lameui = LameUI((window_width, window_height), (0, 0),
                bg_color=background_color, name="lameui")


run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        elif event.type == pygame.VIDEORESIZE:
            lameui.resize(event.size)

    lameui.draw_to(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
