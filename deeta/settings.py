import pygame as pyg

# stuffs
WIDTH, HEIGHT = 1200, 900
FPS = 60
CLOCK = pyg.time.Clock()

# fonts
NORMAL_F = "fonts/normal.otf"
ITALIC_F = "fonts/italic.otf"

# colours
BG_COLOUR = "#1D282E"

# events
SPLASH_SCREEN = pyg.USEREVENT + 0

# cursors
CURSORS = [
    "graphics/ui/cursors/circle_dot.png",
    "graphics/ui/cursors/cross.png",
    "graphics/ui/cursors/arrow.png"
]
