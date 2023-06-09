from random import randint
import pygame
from pylame.components import LameUI, Text, Button, Alignment

window_width, window_height = 1024, 768

pygame.init()
screen = pygame.display.set_mode(
    (window_width, window_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
FPS = 60


background_color = (22, 22, 22)

lameui = LameUI((window_width, window_height), (0, 0),
                bg_color=background_color, name="lameui")

title = Text("LameUI", 64, pos=(0, -100))

button_w, button_h = 200, 60
button_color = (100, 100, 100)

button1 = Button((button_w, button_h), (0, 100), button_color,
                 text="click me!", font_size=24, border_radius=8)
close_button = Button((button_w, button_h), (0, 20),
                      button_color, text="quit", font_size=24, border_radius=8)

lameui.align(Alignment.CENTER)

lameui.add(title)
lameui.add(button1)
lameui.add(close_button)

run = True


def rand_title_color(button):
    if button == pygame.BUTTON_LEFT:
        title.set_font_color((randint(0, 255),
                             randint(0, 255),
                             randint(0, 255)))


def handle_close_button(button):
    global run
    if button == pygame.BUTTON_LEFT:
        run = False


button1.on_press = rand_title_color
close_button.on_press = handle_close_button


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
    lameui.process_mouse_pos()
    lameui.draw_to(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
