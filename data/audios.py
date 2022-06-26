import pygame as pg
from random import choice

pg.mixer.init()


def get_random_audio(sounds: list[pg.mixer.Sound]) -> pg.mixer.Sound:
    return choice(sounds)


ENEMIES_DIE = [
    pg.mixer.Sound("audios/enemies/die/1.wav"),
    pg.mixer.Sound("audios/enemies/die/2.wav"),
    pg.mixer.Sound("audios/enemies/die/3.wav"),
    pg.mixer.Sound("audios/enemies/die/4.wav"),
    pg.mixer.Sound("audios/enemies/die/5.wav")
]

PLAYER_ATTACK = [
    pg.mixer.Sound("audios/player/attack/1.wav"),
    pg.mixer.Sound("audios/player/attack/2.wav"),
    pg.mixer.Sound("audios/player/attack/3.wav"),
    pg.mixer.Sound("audios/player/attack/4.wav")
]
for sound in PLAYER_ATTACK:
    sound.set_volume(0.3)

DAMAGED = [
    pg.mixer.Sound("audios/shared/damaged/1.wav"),
    pg.mixer.Sound("audios/shared/damaged/2.wav"),
    pg.mixer.Sound("audios/shared/damaged/3.wav"),
    pg.mixer.Sound("audios/shared/damaged/4.wav")
]
for sound in DAMAGED:
    sound.set_volume(2)

HOVER = pg.mixer.Sound("audios/ui/hover.wav")
SELECT = pg.mixer.Sound("audios/ui/select.wav")
SELECT.set_volume(0.12)

BG_MUSIC = None
