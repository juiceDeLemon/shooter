import pygame as pg

# stuffs
WIDTH, HEIGHT = 1200, 900
FPS = 60
CLOCK = pg.time.Clock()

# fonts
NORMAL_F = "fonts/normal.otf"
ITALIC_F = "fonts/italic.otf"

# visuals
BG_COLOUR = "#1D282E"
FLASH_DUR = 6  # frames (1/10 * 60 = 6)
CURSORS = [
    "images/ui/cursors/circle_dot.png",
    "images/ui/cursors/cross.png",
    "images/ui/cursors/arrow.png"
]
