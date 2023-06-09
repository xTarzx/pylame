import pygame
from pylame.components import LameUI, Alignment, Button, Text


window_width, window_height = 1024, 768
pygame.init()
screen = pygame.display.set_mode(
    (window_width, window_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
FPS = 60


background_color = (22, 22, 22)
btn_color = (55, 55, 55)

timer = 0
counting = False


lameui = LameUI((window_width, window_height), (0, 0),
                bg_color=background_color, name="lameui")
lameui.align(Alignment.CENTER)

start_button = Button((200, 40), (0, 20), btn_color, text="start")
stop_button = Button((200, 40), (0, 10), btn_color, text="stop")
reset_button = Button((200, 40), (0, 10), btn_color, text="reset")

timer_text = Text("", 32)

lameui.add(timer_text)
lameui.add(start_button)
lameui.add(stop_button)
lameui.add(reset_button)


def on_press_start(button):
    global counting
    if button == pygame.BUTTON_LEFT:
        counting = True


def on_press_stop(button):
    global counting
    if button == pygame.BUTTON_LEFT:
        counting = False


def on_press_reset(button):
    global timer
    if button == pygame.BUTTON_LEFT:
        timer = 0


start_button.on_press = on_press_start
stop_button.on_press = on_press_stop
reset_button.on_press = on_press_reset


def ms_to_format_str(ms):
    ss = int((ms % 1000)/10)
    s = int((ms/1000) % 60)
    m = int((ms/(1000*60)) % 60)
    h = int((ms/(1000*60*60)) % 24)

    return f"{h:02d}:{m:02d}:{s:02d}.{ss:02d}"


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

    timer_text.set_text(ms_to_format_str(timer))

    if counting:
        timer += dt

    lameui.handle_events()
    lameui.process_mouse_pos()
    lameui.process(dt)

    lameui.draw_to(screen)

    pygame.display.update()
    dt = clock.tick(FPS)

pygame.quit()
