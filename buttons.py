import pygame as pyg
import deeta.settings as settings

button_off_set = 100 // 4
pyg.font.init()


def combine_surface(surf_1: pyg.Surface, surf_2: pyg.Surface, orientation: str) -> pyg.Surface  :
    """Returns an empty surface to blit the surfaces onto. Good for "merging" surfaces."""
    if orientation == "horizontal":
        return pyg.Surface((surf_1.get_width() + surf_2.get_width(),
                            max(surf_1.get_height(), surf_2.get_height()) + 70), pyg.SRCALPHA)
    elif orientation == "vertical":
        return pyg.Surface((max(surf_1.get_width(), surf_2.get_width()) + 7,
                            surf_1.get_height() + surf_2.get_height()), pyg.SRCALPHA)
    else:
        raise AttributeError("'orientation' must be either 'horizontal' or 'vertical'.")


class QuitButton:
    def __init__(self, screen: pyg.Surface):
        self.image = pyg.image.load(
            "graphics/buttons/quit.png").convert_alpha()
        self.text = pyg.font.Font(settings.NORMAL_F, 70).render(
            "Quit: ", False, "white")
        self.surface = combine_surface(self.text, self.image, "horizontal")
        self.rect = self.surface.get_rect(
            center=(settings.WIDTH / 2, 700))
        self.screen = screen

    def __call__(self):
        pyg.event.post(pyg.event.Event(pyg.QUIT))

    def animation(self):
        self.surface.set_alpha(100 if self.rect.collidepoint(
            pyg.mouse.get_pos()) else 255)

    def draw(self):
        self.screen.blit(self.surface, self.rect)
        # magic number: 0 + button_off_set - 5 (spacing)
        self.surface.blit(
            self.image, (self.text.get_width(), button_off_set - 5))
        self.surface.blit(self.text, (0, 0))

    def update(self):
        self.animation()
        self.draw()


class ChangeCursorButton:
    def __init__(self, screen: pyg.Surface):
        self.image = pyg.image.load(
            "graphics/buttons/change_cursor.png").convert_alpha()
        self.text = pyg.font.Font(settings.NORMAL_F, 70).render(
            "Change cursor: ", False, "white")
        self.surface = combine_surface(self.text, self.image, "horizontal")
        self.rect = self.surface.get_rect(
            center=(settings.WIDTH / 2, 550))
        self.screen = screen
        self.cursor = 0

    def __call__(self):
        from main import cursor_group
        from otherui import Cursor
        # if self.cursor == len(settings.CURSORS) + 1:
        #     self.cursor = 0
        self.cursor = 0 if self.cursor == len(
            settings.CURSORS) else self.cursor
        cursor_group.empty()
        cursor_group.add(Cursor(settings.CURSORS[self.cursor]))
        self.cursor += 1

    def animation(self):
        self.surface.set_alpha(100 if self.rect.collidepoint(
            pyg.mouse.get_pos()) else 255)

    def draw(self):
        self.screen.blit(self.surface, self.rect)
        # magic number: 0 + button_off_set - 5 (spacing)
        self.surface.blit(
            self.image, (self.text.get_width(), button_off_set - 5))
        self.surface.blit(self.text, (0, 0))

    def update(self):
        self.animation()
        self.draw()
