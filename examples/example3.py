import pygame
from pylame.components import LameUI, Alignment, TextInput, Panel

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

panel1 = Panel((600, 400), (0, 0), (55, 55, 55), border_radius=12)

textinput = TextInput((500, 40), (0, 0),
                      bg_color=(88, 88, 88), text="wakanda")
panel1.add(textinput)
lameui.add(panel1)

dt = 0
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

        else:
            pygame.event.post(event)

    lameui.handle_events()
    lameui.process_mouse_pos()
    lameui.process(dt)

    lameui.draw_to(screen)

    pygame.display.update()
    dt = clock.tick(FPS)

pygame.quit()
