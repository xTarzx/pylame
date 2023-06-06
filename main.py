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

text1 = Text("test1", 12)

button1 = Button((100, 30), (0, 0), (220, 120, 20),
                 name="button1", text="button1")

slider1 = Slider((400, 30), (0, 0), bg_color=None, name="slider",
                 knob_color=(220, 100, 120), slider_color=(88, 88, 88), min_value=50, max_value=100, start_value=None)
text2 = Text("", 20)

panel = Panel((600, 300), (0, 0), (55, 55, 55), name="panel", border_radius=16)
panel.align(Alignment.CENTER_HORIZONTAL)
panel.add(text1)
panel.add(button1)
panel.add(slider1)
panel.add(text2)

lameui.add(panel)

lameui.align(Alignment.CENTER)

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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

    text2.set_text(f"{slider1.get_value():.2f}")
    lameui.process_mouse_pos()

    screen.blit(lameui.get_surface(), lameui.pos)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
