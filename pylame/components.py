from __future__ import annotations
import pygame


class Component:
    def __init__(self, size, pos, bg_color=None, name="", parent=None):
        self.size = size
        self.pos = pos
        self.base_pos = pos
        self.bg_color = bg_color
        self.name = name
        self.parent: Component | None = parent
        self.surface = pygame.Surface(size, pygame.SRCALPHA)

        self.highlight_color = None
        scale = 1.3
        if self.bg_color:
            self.highlight_color = (min(self.bg_color[0]*scale, 255), min(
                self.bg_color[1]*scale, 255), min(self.bg_color[2]*scale, 255))

    def get_surface(self):
        return self.surface

    def redraw(self):
        assert False, "unimplemented"

    def __str__(self) -> str:
        if self.name:
            return self.name
        return self.__repr__

    def on_hover(self):
        pass

    def on_press(self, *args, **kwargs):
        pass


class Text(Component):
    def __init__(self, text, font_size=None, font_color=None):
        super().__init__((0, 0), (0, 0))
        self.font_size = 10
        if font_size:
            self.font_size = font_size

        self.font_color = (240, 240, 240)
        if font_color:
            self.font_color = font_color

        self.text = text

        font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        self.render = font.render(self.text, True, self.font_color)
        self.size = self.render.get_size()

        # width, height = self.parent.size
        # rect = rendered_text.get_rect()
        # rect.center = (width/2, height/2)

    def redraw(self):
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface.blit(self.render, (0, 0))


class Button(Component):
    def __init__(self, size, pos, color=None, name="", parent=None, text="", font_size=None, font_color=None, border_radius=0):
        super().__init__(size, pos, color, name, parent)
        self.hovered = False
        self.border_radius = border_radius

        self.components = []
        self.sizer = Sizer(self)
        self.sizer.set_alignment(Alignment.CENTER)

        self.text = Text(text, font_size, font_color)
        self.components.append(self.text)

    def redraw(self):
        self.sizer.calc_pos()

        rect = self.surface.get_rect()

        if self.bg_color is not None:
            pygame.draw.rect(self.surface, self.bg_color,
                             rect, border_radius=self.border_radius)
            # self.surface.fill(self.bg_color)

        if self.hovered and self.highlight_color:
            pygame.draw.rect(self.surface, self.highlight_color,
                             rect, border_radius=self.border_radius)
            # self.surface.fill(self.highlight_color)

        self.surface.blit(self.text.get_surface(), self.text.pos)
        # rendered_text = self.text.render()
        # width, height = self.size
        # rect = rendered_text.get_rect()
        # rect.center = (width/2, height/2)

        # self.surface.blit(rendered_text, rect)

    def on_hover(self):
        self.hovered = True


class Alignment:
    CENTER_HORIZONTAL = 0
    CENTER_VERTICAL = 1
    CENTER = 2


class Sizer:
    VERTICAL = 0
    HORIZONTAL = 1

    def __init__(self, parent: Panel, direction: int = 0):
        self.parent = parent
        self.direction = direction
        self.center_h = False
        self.center_v = False

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
            if self.direction == Sizer.HORIZONTAL:
                total_component_width += comp_width

            elif self.direction == Sizer.VERTICAL:
                total_component_height += comp_height

        for comp in self.parent.components:
            if isinstance(comp, Panel):
                comp.sizer.calc_pos()
            comp.redraw()

            width, height = self.parent.size
            center_x = width/2
            center_y = height/2

            x, y = comp.base_pos
            comp_width, comp_height = comp.size

            if self.direction == Sizer.VERTICAL:
                y += offset
                offset += comp_height

            elif self.direction == Sizer.HORIZONTAL:
                x += offset
                offset += comp_width

            if self.center_v:
                y += center_y - total_component_height/2
            if self.center_h:
                x += center_x - total_component_width/2
            comp.pos = (x, y)


class Panel(Component):
    def __init__(self, size, pos, bg_color=None, name="", parent=None):
        super().__init__(size, pos, bg_color, name, parent)
        self.components: list[Component] = []
        self.sizer = Sizer(self)

    def get_component_at(self, mouse_x, mouse_y) -> Component | None:
        # print(self, "get_component_at", mouse_x, mouse_y)
        rect = pygame.Rect(self.pos[0], self.pos[1],
                           self.size[0], self.size[1])
        if not rect.collidepoint(mouse_x, mouse_y):
            return None

        for comp in self.components:
            # print("component:", comp)
            # print("   pos :", comp.pos)
            # print("   size:", comp.size)

            pos_x, pos_y = comp.pos

            if isinstance(comp, Panel):
                panel_comp = comp.get_component_at(mouse_x, mouse_y)
                if panel_comp is not None:
                    return panel_comp

            comp_parent_x, comp_parent_y = comp.parent.pos

            pos_x += comp_parent_x
            pos_y += comp_parent_y

            rect = pygame.Rect(
                pos_x, pos_y, comp.size[0], comp.size[1])

            if rect.collidepoint(mouse_x, mouse_y):
                return comp

        return self

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
        self.surface.fill(self.bg_color)
        for comp in self.components:
            comp.redraw()

            self.surface.blit(comp.get_surface(), comp.pos)

    def add(self, component: Component):
        component.parent = self
        self.components.append(component)
        self.recalculate()


class LameUI(Panel):
    def process_mouse_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered_component = self.get_component_at(mouse_x, mouse_y)

        if isinstance(hovered_component, Button):
            hovered_component.hovered = True

        self.recalculate()

        buttons: list[Button] = self.get_all_components_of_type(Button)
        for button in buttons:
            button.hovered = False

    def on_mouse_press(self, button):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered_component = self.get_component_at(mouse_x, mouse_y)

        if hovered_component is not None:
            hovered_component.on_press(button)
