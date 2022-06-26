import pygame as pg


def flash(sprite: pg.sprite.Sprite, duration: int):
    if not hasattr(sprite, "alpha_frame"):
        sprite.alpha_frame = 0
    # alpha_frame is a special type of variable I created.
    # It's like a for loop but it's not.
    # Don't know if this has been done.
    # It is a boolean (0 or 1) and if it is 1 (True), it will be changed to being a counter,
    # like the i from for i in range(x)
    # Therefore, the counter reset point will be 1 bigger than the duration.
    # -------------------------
    if sprite.alpha_frame:  # "if True"
        if sprite.alpha_frame == 1:  # "initialise" when alpha_frame is "True"
            try:  # flash (decrease alpha)
                sprite.orig_img.set_alpha(50)
            except AttributeError:
                sprite.image.set_alpha(50)
        sprite.alpha_frame += 1  # counting
        if sprite.alpha_frame == duration + 1:  # max
            print(
                f"change_pls {sprite.orig_img.get_alpha()} {sprite.image.get_alpha()}")
            try:  # reset (max alpha) / ending code
                sprite.orig_img.set_alpha(255)
            except AttributeError:
                sprite.image.set_alpha(255)
            sprite.alpha_frame = 0  # reset
    # -------------------------

    # structure for this type of variable:
    # if variable:
    #     if variable == 1: # optional
    #         ...
    #     variable += 1
    #     if variable == max_duration + 1:
    #         ...
    #         variable = 0


class Cursor(pg.sprite.Sprite):
    def __init__(self, cursor: str):
        super().__init__()
        self.cursor = cursor
        self.image = pg.image.load(cursor).convert_alpha()
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pg.mouse.get_pos())

    def update(self):
        self.rect = self.image.get_rect(topleft=pg.mouse.get_pos()) \
            if self.cursor == "images/ui/cursors/arrow.png" \
            else \
            self.image.get_rect(center=pg.mouse.get_pos())
