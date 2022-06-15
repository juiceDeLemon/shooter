import pygame as pyg


class Cursor(pyg.sprite.Sprite):
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        self.image = pyg.image.load(cursor).convert_alpha()
        self.rect = self.image.get_rect(center=pyg.mouse.get_pos())

    def update(self):
        self.rect = self.image.get_rect(topleft=pyg.mouse.get_pos()) \
            if self.cursor == "graphics/ui/cursors/arrow.png" \
            else \
            self.image.get_rect(center=pyg.mouse.get_pos())


class Menu:
    ...

# class HealthBar():
#     ani_width = 0

#     # 1 is transition speed
#     if not self.ani_health == self.health:
#         if self.ani_health < self.health - 1:
#             self.ani_health += 1
#         elif self.ani_health > self.health + 1:
#             self.ani_health -= 1
#         else:
#             self.ani_health = self.health
#         ani_width = (self.health - self.ani_health) / \
#             self.max_health_to_health_bar_max_length_ratio

#     # x = 70, y = 25 is the offset from the top left corner of the screen
#     # 54, settings.WIDTH is the height and the max length of the health bar

#     # background
#     pyg.draw.rect(screen, bg_colour, pyg.Rect(
#         70, 25, settings.WIDTH/3, 54))

#     # bar rect
#     bar_rect = pyg.Rect(
#         70, 25, int(self.ani_health / self.max_health_to_health_bar_max_length_ratio), 54)
#     # animation bar
#     ani_bar_rect = pyg.Rect(bar_rect.right, 70, ani_width, 54)
#     pyg.draw.rect(screen, "#646464", ani_bar_rect)
#     # bar
#     pyg.draw.rect(screen, "#dddddd", bar_rect, 0, 12)
#     # bar shade
#     # 25+54-20 = offset + (height - shade height)
#     pyg.draw.rect(screen, "#afafaf", pyg.Rect(
#         70, 25+54-20, self.health / self.max_health_to_health_bar_max_length_ratio, 20),
#         0, border_bottom_left_radius=12, border_bottom_right_radius=12)
#     # frame
#     pyg.draw.rect(screen, "#ffffff", pyg.Rect(
#         70, 25, settings.WIDTH/3, 54), 5, border_top_right_radius=12, border_bottom_right_radius=12)
#     # heart
#     screen.blit(self.heart_img, self.heart_rect)
