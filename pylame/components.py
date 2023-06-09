from __future__ import annotations
import pygame


class Alignment:

    CENTER_HORIZONTAL = 0
    CENTER_VERTICAL = 1
    CENTER = 2


class Component:
    def __init__(self, size, pos, bg_color=None, name="", parent=None):
        self.size = size
        self.pos = pos
        self.base_pos = pos
        self.bg_color = bg_color
        if self.bg_color is None:
            self.bg_color = (0, 0, 0, 0)
        elif len(self.bg_color) == 3:
            self.bg_color = self.bg_color + (255,)
        self.name = name
        self.parent: Component | None = parent
        self.surface = pygame.Surface(size, pygame.SRCALPHA)

        self.highlight_color = None
        scale = 80

        r, g, b, a = self.bg_color

        r = min(r+scale, 255)
        g = min(g+scale, 255)
        b = min(b+scale, 255)
        a = min(a+scale, 255)

        self.highlight_color = (r, g, b, a)

    def get_surface(self):
        return self.surface

    def redraw(self):
        assert False, "unimplemented"

    def __str__(self) -> str:
        if self.name:
            return self.name
        return self.__repr__()

    def on_hover(self):
        pass

    def handle_mouse_selected(self, *args, **kwargs):
        pass

    def process(self, dt):
        pass

    def get_root(self):
        if self.parent:
            return self.parent.get_root()
        return self

    def on_press(self, *args, **kwargs):
        root = self.get_root()
        if isinstance(root, LameUI):
            root.set_selected(self)

    def on_select(self):
        pass

    def on_unselect(self):
        pass

    def on_release(self, *args, **kwargs):
        pass

    def get_abs_pos(self):
        pos_x, pos_y = self.pos

        if self.parent is not None:
            px, py = self.parent.get_abs_pos()
            pos_x += px
            pos_y += py
        return pos_x, pos_y


class Text(Component):
    def __init__(self, text, font_size=None, font_color=None, pos=None):
        size = (0, 0)
        if pos is None:
            pos = (0, 0)
        super().__init__(size, pos)
        self.font_size = 10
        if font_size:
            self.font_size = font_size

        self.font_color = (240, 240, 240)
        if font_color:
            self.font_color = font_color

        self.text = text

        self.__render_text()

        # width, height = self.parent.size
        # rect = rendered_text.get_rect()
        # rect.center = (width/2, height/2)

    def __render_text(self):
        font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        self.render = font.render(self.text, True, self.font_color)
        self.size = self.render.get_size()

    def set_text(self, text):
        self.text = str(text)
        self.__render_text()

    def set_font_color(self, color):
        self.font_color = color
        self.__render_text()

    def redraw(self):
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface.blit(self.render, (0, 0))


class TextInput(Component):
    def __init__(self, size, pos, name="", bg_color=None, parent=None, text="", font_color=None):
        super().__init__(size=size, pos=pos,  bg_color=bg_color, name=name, parent=parent)

        self.components = []
        self.sizer = Sizer(self)
        self.sizer.set_alignment(Alignment.CENTER_VERTICAL)

        self.text = text
        self.text_s = Text(text, size[1]-2, font_color)
        self.editing = False
        self.display_bar = True
        self.counter = 1300

        self.__initial_delete_interval = 450

        self.delete_interval = 0
        self.reset_delete_interval()
        self.deleting = False

        self.components.append(self.text_s)

    def redraw(self):
        self.text_s.set_text(self.text)
        width, height = self.size
        text_w, text_h = self.text_s.size

        pad = self.text_s.font_size/2

        cursor_w = self.text_s.font_size/7
        cursor_h = self.text_s.font_size

        cursor_x = text_w
        cursor_y = 2/2
        d = text_w+pad

        self.text_s.base_pos = (0, 0)
        if d > width:
            diff = d - width
            self.text_s.base_pos = (-diff, 0)
            cursor_x = text_w - diff

        char_cursor_padding = 6

        cursor_x += char_cursor_padding

        self.sizer.calc_pos()
        rect = self.surface.get_rect()
        pygame.draw.rect(self.surface, self.bg_color, rect)

        if self.editing and self.display_bar:
            rect = pygame.Rect(
                cursor_x, cursor_y, cursor_w, cursor_h)
            pygame.draw.rect(self.surface, self.text_s.font_color, rect)

        self.surface.blit(self.text_s.get_surface(), self.text_s.pos)

    def process(self, dt):
        if not self.editing:
            return
        self.counter -= dt
        if self.counter < 0:
            self.counter = 2000
            self.display_bar = not self.display_bar

        if self.deleting:
            self.delete_interval -= dt
            if self.delete_interval < 0:
                self.reset_delete_interval()
                self.__delete_char()

    def reset_delete_interval(self):
        self.delete_interval = 75

    def __delete_char(self):
        self.text = self.text[:-1]

    def on_select(self):
        self.editing = True
        self.display_bar = True

    def on_unselect(self):
        self.editing = False
        self.deleting = False

    def on_press(self, button):
        if button == pygame.BUTTON_LEFT:
            root = self.get_root()
            if isinstance(root, LameUI):
                root.set_selected(self)

    def handle_event(self, event):
        # TODO: what to do when event wasnt handled
        if event.type == pygame.TEXTINPUT:
            self.text += event.text
            return

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.__delete_char()
                self.delete_interval = self.__initial_delete_interval
                self.deleting = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                self.deleting = False


class Button(Component):
    def __init__(self, size, pos, color=None, name="", parent=None, text="", font_size=None, font_color=None, border_radius=0):
        super().__init__(size=size, pos=pos, bg_color=color, name=name, parent=parent)
        self.hovered = False
        self.border_radius = border_radius

        self.components = []
        self.sizer = Sizer(self)
        self.sizer.set_alignment(Alignment.CENTER)

        if font_size is None:
            font_size = self.size[1]//2

        self.text = Text(text, font_size, font_color)
        self.components.append(self.text)

    def redraw(self):
        self.sizer.calc_pos()

        rect = self.surface.get_rect()

        pygame.draw.rect(self.surface, self.bg_color,
                         rect, border_radius=self.border_radius)

        if self.hovered:
            pygame.draw.rect(self.surface, self.highlight_color,
                             rect, border_radius=self.border_radius)

        self.surface.blit(self.text.get_surface(), self.text.pos)

    def on_hover(self):
        self.hovered = True


class Sizer:
    VERTICAL = 0
    HORIZONTAL = 1

    def __init__(self, parent: Panel, direction: int = 0, space_between=0):
        self.parent = parent
        self.direction = direction
        self.center_h = False
        self.center_v = False

        self.space_between = space_between

    def set_direction(self, direction: int):
        self.direction = direction

    def set_alignment(self, alignment: Alignment):
        if alignment == Alignment.CENTER_HORIZONTAL:
            self.center_h = True
            self.center_v = False
        elif alignment == Alignment.CENTER_VERTICAL:
            self.center_h = False
            self.center_v = True
        elif alignment == Alignment.CENTER:
            self.center_h = True
            self.center_v = True

    def calc_pos(self):
        offset = 0

        total_component_width = 0
        total_component_height = 0
        for comp in self.parent.components:
            comp_width, comp_height = comp.size

            if total_component_width == 0:
                total_component_width = comp_width
                total_component_height = comp_height
                continue
            total_component_width += comp_width
            total_component_height += comp_height
            if self.direction == Sizer.HORIZONTAL:
                total_component_width += self.space_between
            elif self.direction == Sizer.VERTICAL:
                total_component_height += self.space_between

        for comp in self.parent.components:
            if isinstance(comp, Panel):
                comp.sizer.calc_pos()
            comp.redraw()

            width, height = self.parent.size
            center_x = width/2
            center_y = height/2

            base_x, base_y = comp.base_pos
            x, y = base_x, base_y
            comp_width, comp_height = comp.size

            if self.direction == Sizer.VERTICAL:
                y += offset
                offset += comp_height + self.space_between + base_y

                if self.center_h:
                    x += center_x - comp_width/2

                if self.center_v:
                    y += center_y - total_component_height/2

            elif self.direction == Sizer.HORIZONTAL:
                x += offset
                offset += comp_width + self.space_between + base_x

                if self.center_h:
                    x += center_x - total_component_width/2

                if self.center_v:
                    y += center_y - comp_height/2

            comp.pos = (x, y)


class Slider(Component):
    def __init__(self, size, pos, bg_color=None, name="", parent=None, knob_color=None, slider_color=None, min_value=0, max_value=1, start_value=None):
        super().__init__(size, pos, bg_color=bg_color, name=name, parent=parent)

        self.knob_color = (0, 0, 255)
        self.slider_color = (255, 0, 0)

        if knob_color:
            self.knob_color = knob_color
        if slider_color:
            self.slider_color = slider_color

        assert min_value < max_value
        assert max_value > 0
        self.min_value = min_value
        self.max_value = max_value

        self.value = 0.5

        if start_value is not None:
            value = (start_value-self.min_value) / \
                (self.max_value-self.min_value)
            value = max(0, min(1, value))
            self.value = value

    def get_value(self):
        return ((self.max_value-self.min_value)*self.value)+self.min_value

    def on_press(self, button):
        if button == pygame.BUTTON_LEFT:
            root = self.get_root()

            if isinstance(root, LameUI):
                root.set_selected(self)

    def on_release(self):
        root = self.get_root()
        if isinstance(root, LameUI):
            root.set_selected(None)

    def handle_mouse_selected(self, *args):
        mouse_x, mouse_y = args
        slider_x, slider_y = self.get_abs_pos()
        width, height = self.size
        knob_radius = height/2
        bar_width = width - knob_radius*2
        value = (mouse_x-(slider_x+knob_radius))/bar_width
        value = max(0, min(1, value))
        self.value = value

    def redraw(self):
        rect = self.surface.get_rect()
        self.surface.fill((0, 0, 0, 0), rect)

        pygame.draw.rect(self.surface, self.bg_color, rect)

        width, height = self.size
        knob_radius = height/2

        bar_width = width - knob_radius*2
        bar_height = height*0.45

        x = knob_radius
        y = height/2 - bar_height/2
        rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(self.surface, self.slider_color, rect)

        knob_x = bar_width*self.value+knob_radius

        knob_y = height/2

        pygame.draw.circle(self.surface, self.knob_color,
                           (knob_x, knob_y), knob_radius)


class Panel(Component):
    def __init__(self, size, pos, bg_color=None, name="", parent=None, border_radius=0):
        super().__init__(size=size, pos=pos, bg_color=bg_color, name=name, parent=parent)
        self.components: list[Component] = []
        self.sizer = Sizer(self)
        self.border_radius = border_radius

    def get_component_at(self, mouse_x, mouse_y) -> Component | None:
        pos_x, pos_y = self.get_abs_pos()

        rect = pygame.Rect(pos_x, pos_y,
                           self.size[0], self.size[1])
        if not rect.collidepoint(mouse_x, mouse_y):
            return None

        for comp in self.components:

            pos_x, pos_y = comp.get_abs_pos()
            comp_w, comp_h = comp.size

            rect = pygame.Rect(pos_x, pos_y, comp_w, comp_h)

            if rect.collidepoint(mouse_x, mouse_y):
                if isinstance(comp, Panel):
                    return comp.get_component_at(mouse_x, mouse_y)

                return comp

        return self

    def propagate_dt(self, dt):
        for component in self.components:
            component.process(dt)

    def process(self, dt):
        self.propagate_dt(dt)

    def get_all_components_of_type(self, component_type: type):
        components = []
        for component in self.components:
            if isinstance(component, component_type):
                components.append(component)

            if isinstance(component, Panel):
                components.extend(
                    component.get_all_components_of_type(component_type))

        return components

    def set_direction(self, direction: int):
        # direction : Sizer.VERTICAL | Sizer.HORIZONTAL
        self.sizer.set_direction(direction)
        self.recalculate()

    def set_space_between(self, value: int):
        self.sizer.space_between = value
        self.recalculate()

    def align(self, alignment: Alignment):
        self.sizer.set_alignment(alignment)
        self.recalculate()

    def get_direction(self) -> int:
        return self.sizer.direction

    def resize(self, size):
        self.size = size
        self.surface = pygame.transform.scale(self.surface, size)
        self.recalculate()

    def recalculate(self):
        self.sizer.calc_pos()
        self.redraw()

    def redraw(self):

        rect = self.surface.get_rect()
        self.surface.fill((0, 0, 0, 0), rect)

        pygame.draw.rect(self.surface, self.bg_color, rect,
                         border_radius=self.border_radius)
        for comp in self.components:
            comp.redraw()

            self.surface.blit(comp.get_surface(), comp.pos)

    def add(self, component: Component):
        component.parent = self
        self.components.append(component)
        self.recalculate()


class LameUI(Panel):
    def __init__(self, size, pos, bg_color=None, name="", parent=None):
        super().__init__(size, pos, bg_color, name, parent)

        self.selected_component: Component | None = None

    def process_mouse_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.selected_component is not None:
            self.selected_component.handle_mouse_selected(mouse_x, mouse_y)

        hovered_component = self.get_component_at(mouse_x, mouse_y)

        if isinstance(hovered_component, Button):
            hovered_component.hovered = True

        self.recalculate()

        buttons: list[Button] = self.get_all_components_of_type(Button)
        for button in buttons:
            button.hovered = False

    def handle_events(self):
        # TODO: what to do when children doesnt handle event
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                self.resize(event.size)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.on_mouse_press(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.on_mouse_release(event.button)

            elif event.type == pygame.KEYDOWN:
                if isinstance(self.selected_component, TextInput):
                    self.selected_component.handle_event(event)
            elif event.type == pygame.KEYUP:
                if isinstance(self.selected_component, TextInput):
                    self.selected_component.handle_event(event)

            elif event.type == pygame.TEXTINPUT:
                if isinstance(self.selected_component, TextInput):
                    self.selected_component.handle_event(event)

    def set_selected(self, component):
        if self.selected_component is not None:
            self.selected_component.on_unselect()

        self.selected_component = component
        if self.selected_component is not None:
            self.selected_component.on_select()

    def on_mouse_press(self, button):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered_component = self.get_component_at(mouse_x, mouse_y)

        if hovered_component is not None:
            hovered_component.on_press(button)
        else:
            self.set_selected(None)

    def on_mouse_release(self, button):
        if self.selected_component is not None:
            self.selected_component.on_release()
        # mouse_x, mouse_y = pygame.mouse.get_pos()
        # hovered_component = self.get_component_at(mouse_x, mouse_y)

        # if hovered_component is not None:
            # hovered_component.on_press(button)

    def draw_to(self, surface: pygame.Surface):
        surface.blit(self.get_surface(), self.pos)
