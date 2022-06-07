import pygame as pyg
import deeta.settings as settings


class QuitButton:
    def __init__(self, screen: pyg.Surface):
        self.image = pyg.image.load(
            "graphics/buttons/quit.png").convert_alpha()
        offset = self.image.get_width() // 4
        self.rect = self.image.get_rect(
            bottomright=(settings.WIDTH-offset, settings.HEIGHT-offset))
        self.screen = screen

    def __call__(self):
        pyg.event.post(pyg.event.Event(pyg.QUIT))

    def animation(self):
        if self.rect.collidepoint(pyg.mouse.get_pos()):
            self.image.set_alpha(100)
            # self.image = pyg.transform.rotozoom(self.image, 0, 1.2)
        else:
            self.image.set_alpha(255)
            # self.image = pyg.transform.rotozoom(self.image, 0, 0.8)

    def update(self):
        self.animation()
        self.screen.blit(self.image, self.rect)
