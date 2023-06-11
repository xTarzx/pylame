import pygame

from pylame.components import Button, Panel, Sizer, Alignment, LameUI, Text, Slider

window_width, window_height = 1024, 768

pygame.init()
screen = pygame.display.set_mode(
    (window_width, window_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
FPS = 60

lameui = LameUI((window_width, window_height),
                (0, 0), (33, 33, 33), name="lameui")


lameui.align(Alignment.CENTER)

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

        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         lameui.redraw()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            lameui.on_mouse_press(event.button)
        elif event.type == pygame.MOUSEBUTTONUP:
            lameui.on_mouse_release(event.button)

    lameui.process_mouse_pos()

    lameui.draw_to(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
