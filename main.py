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


lameui.add(Slider((300, 30), (0, 0), name="slider1"))
# panel1 = Panel((160, 400), (0, 0), (55, 55, 55),
#                name="panel1", border_radius=16)

# button1 = Button(size=(100, 30), pos=(0, 0),
#                  color=(50, 10, 220), name="button1", text="button1", border_radius=12)
# button2 = Button(size=(100, 30), pos=(0, 0),
#                  color=(10, 180, 50), name="button2", text="click")

# def set_caption(text):
#     pygame.display.set_caption(text)

# button1.on_press = lambda _: set_caption(f"clicked {button1.name}")
# button2.on_press = lambda _: set_caption(f"clicked {button2.name}")


# panel1.add(button1)
# panel1.add(button2)
# panel1.add(Text("wakanda", 32))
# panel1.set_space_between(10)


# lameui.add(panel1)

lameui.set_direction(Sizer.HORIZONTAL)
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

    lameui.process_mouse_pos()

    screen.blit(lameui.get_surface(), lameui.pos)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
