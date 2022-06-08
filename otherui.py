import pygame as pyg


class Cursor(pyg.sprite.Sprite):
    def __init__(self, cursor):
        super().__init__()
        self.image = pyg.image.load(cursor).convert_alpha()
        self.rect = self.image.get_rect(center=pyg.mouse.get_pos())

    def update(self):
        self.rect = self.image.get_rect(center=pyg.mouse.get_pos())
