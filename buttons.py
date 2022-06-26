import pygame as pg
import data.configuration as config
import data.audios as audios

button_off_set = 100 // 4
# pg.font.init()


# def combine_surface(surf_1: pg.Surface, surf_2: pg.Surface, orientation: str) -> pg.Surface:
#     """
#     Returns an empty surface to blit the surfaces onto. Good for "merging" surfaces.
#     """
#     if orientation == "horizontal":
#         return pg.Surface(
#             (surf_1.get_width() + surf_2.get_width(),
#                 max(surf_1.get_height(), surf_2.get_height()) + 70),
#             pg.SRCALPHA
#         )
#     elif orientation == "vertical":
#         return pg.Surface(
#             (max(surf_1.get_width(), surf_2.get_width()) + 7,
#                 surf_1.get_height() + surf_2.get_height()),
#             pg.SRCALPHA
#         )
#     else:
#         raise AttributeError(
#             "'orientation' must be either 'horizontal' or 'vertical'.")


class MenuButton(pg.sprite.Sprite):
    def __init__(self, image_path_prefix: str, pos: tuple[int]):
        """
        image_path_prefix example: "images/ui/menu/resume",
        only True or False as index
        ----
        button pos calculation:
        button no.: first button = 0, second button = 1 etc.
        x = centre, y = top button pos (400) + (height + tile_gap: 40)*button no.
        ----
        button style guide:
        font size 54, corner radius and frame width is the same with the health bar (12).
        flashed version of the button:
        https://www.youtube.com/watch?v=pakXbx4pv24 (use white background)
        """
        super().__init__()
        self.images = [
            f"{image_path_prefix}_0.png",
            f"{image_path_prefix}_1.png"
        ]
        self.image = pg.image.load(self.images[False]).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.was_hovered = self.is_hovered = False

    def __call__(self):
        ...

    def animation_sound(self):
        """This function controls the animation and sound effect."""
        # flash
        self.image = pg.image.load(
            self.images[self.is_hovered]).convert_alpha()
        # sound effect
        if not self.was_hovered and self.is_hovered:
            audios.HOVER.play()

    def update(self):
        self.is_hovered = self.rect.collidepoint(pg.mouse.get_pos())
        self.animation_sound()
        self.was_hovered = self.is_hovered


class Resume(MenuButton):
    def __init__(self):
        super().__init__("images/ui/menu/resume", (config.WIDTH / 2, 400))

    def __call__(self):
        from main import change_game_state, game_state
        if game_state == 2 or game_state == 3:
            change_game_state(1)


class Settings(MenuButton):
    def __init__(self):
        super().__init__("images/ui/menu/settings", (config.WIDTH / 2, 520))

    def __call__(self):
        from main import change_game_state, game_state
        if game_state == 2 or game_state == 3:
            change_game_state(3)


class Quit(MenuButton):
    def __init__(self):
        super().__init__("images/ui/menu/quit", (config.WIDTH / 2, 640))

    def __call__(self):
        pg.event.post(pg.event.Event(pg.QUIT))


# class Slider(pg.sprite.Sprite):
#     def __init__(self, screen: pg.Surface):
#         super().__init__()
#         self.images = [
#             "images/ui/settings/slider_button_0.png",
#             "images/ui/settings/slider_button_1.png"
#         ]
#         self.var, self.max = 20, 100
#         self.image = pg.image.load(self.images[False]).convert_alpha()
#         # self.rect = self.image.get_rect(topleft=(250, 200 - (60 - 45) / 2))
#         self.rect = self.image.get_rect(center=(250, 200))
#         self.screen = screen
#         self.was_hovered = False
#         self.is_hovered = False

#         self.start = pg.image.load(
#             "images/ui/settings/slider_start.png").convert_alpha()
#         self.end = pg.image.load(
#             "images/ui/settings/slider_end.png").convert_alpha()
#         self.bar = pg.image.load(
#             "images/ui/settings/slider_bar.png").convert_alpha()

#         self.spacing = 50

#     def control(self):
#         ...

#     def draw_bar(self):
#         # centerx = 250:
#         # start
#         self.screen.blit(self.start, (200, 200 - self.start.get_height() / 2))
#         # bar left
#         self.bar = pg.transform.scale(
#             self.bar,
#             ((self.rect.centerx - (200 + self.start.get_width())) -
#              (self.spacing), self.bar.get_height())
#         )
#         self.screen.blit(self.bar, (200 + self.start.get_width(),
#                          200 - self.start.get_height() / 2))
#         # bar right

#         # end

#     def animation_sound(self):
#         """This function controls the animation and sound effect."""
#         # flash
#         self.image = pg.image.load(
#             self.images[self.is_hovered]).convert_alpha()
#         # sound effect
#         if not self.was_hovered and self.is_hovered:
#             audios.HOVER.play()

#     def update(self):
#         self.is_hovered = self.rect.collidepoint(pg.mouse.get_pos())
#         self.draw_bar()
#         self.control()
#         self.animation_sound()
#         self.was_hovered = self.is_hovered


# class MusicVol(Slider):
#     def __init__(self, screen):
#         super().__init__(screen)


"""
## make a slider class with max value, width as attributes (also screen)
## if (thing := self.bar, (width-self.start.get_width()*2)) >= 0:
##     pg.transform.scale(self.bar, thing)
## else:
##     pg.transform.scale(same thing but size width = 0)
self.start.get_width()*2 = start and end
create a surface that have a certain area of the background (the slider button's place) (every frame)
blit it 
blit the slider button onto it
note that slider needs to be group.draw()-ed at Surface, not screen and update first then draw.
"""


# class Slider(pg.sprite.Sprite):
#     def __init__(self, screen: pg.Surface, bar_pos: tuple[int], max_value: int, width: int):
#         super().__init__()
#         self.images = [
#             "images/ui/settings/slider_button_0.png",
#             "images/ui/settings/slider_button_1.png"
#         ]
#         self.image = pg.image.load(self.images[False]).convert_alpha()
#         self.rect = self.image.get_rect(center=(250, 200))
#         self.max = max_value
#         self.screen = screen
#         self.was_hovered = self.is_hovered = False

#         self.start = pg.image.load(
#             "images/ui/settings/slider_start.png").convert_alpha()
#         self.bar = pg.image.load(
#             "images/ui/settings/slider_bar.png").convert_alpha()
#         self.bar = pg.transform.scale(self.bar, (width, self.bar.get_height()))
#         self.end = pg.image.load(
#             "images/ui/settings/slider_end.png").convert_alpha()
#         self.bar_pos = bar_pos

#     def create_surface(self):
#         value = 50
#         self.surface = pg.Surface(self.image.get_)

#     def draw_bar(self):
#         # centerx = 250 abdc
#         # start
#         self.screen.blit(self.start, (200, 200))
#         # bar
#         self.screen.blit(self.bar, (200 + self.start.get_width(), 200))
#         # end
#         self.screen.blit(
#             self.end, (200 + self.start.get_height() + self.bar.get_width()))

#     def update(self):
#         self.draw_bar()
#         self.create_surface()
