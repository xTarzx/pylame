import pygame
from pylame.components import LameUI, Text, Alignment, Slider

window_width, window_height = 1024, 768

pygame.init()
screen = pygame.display.set_mode(
    (window_width, window_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
FPS = 60


background_color = (22, 22, 22)

lameui = LameUI((window_width, window_height), (0, 0),
                bg_color=background_color, name="lameui")
lameui.align(Alignment.CENTER)

title_color = (240, 240, 240)

title = Text("LameUI", 64, pos=(0, 0))

slider_w, slider_h = 700, 40
slider_color = (123, 123, 123)

r_slider = Slider((slider_w, slider_h), (0, 30), knob_color=(
    255, 0, 0), slider_color=slider_color, min_value=0, max_value=255, start_value=title_color[0])
g_slider = Slider((slider_w, slider_h), (0, 15), knob_color=(
    0, 255, 0), slider_color=slider_color, min_value=0, max_value=255, start_value=title_color[1])
b_slider = Slider((slider_w, slider_h), (0, 15), knob_color=(
    0, 0, 255), slider_color=slider_color, min_value=0, max_value=255, start_value=title_color[2])


lameui.add(title)
lameui.add(r_slider)
lameui.add(g_slider)
lameui.add(b_slider)


run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        else:
            pygame.event.post(event)

    lameui.handle_events()

    title_color = (r_slider.get_value(),
                   g_slider.get_value(), b_slider.get_value())

    if title_color != title.font_color:
        title.set_font_color(title_color)

    lameui.process_mouse_pos()

    lameui.draw_to(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
