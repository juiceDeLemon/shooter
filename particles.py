import pygame as pg
from random import randrange, uniform
from math import cos, sin, radians
from data.configuration import FPS


class GunShot:
    def __init__(self, pos: tuple[int], screen: pg.Surface):
        self.pos = pos
        self.max_rad = self.radius = 20
        self.width = 2
        self.decay_speed = 1.5
        self.fill_time = 1.7
        self.screen = screen

    def change_size(self):
        if self.radius:
            self.radius -= self.decay_speed

    def draw(self):
        if self.max_rad >= self.radius >= self.max_rad - self.decay_speed * self.fill_time:
            pg.draw.circle(
                self.screen, "white", self.pos, self.radius, 0
            )
        else:
            pg.draw.circle(
                self.screen, "white", self.pos, self.radius, self.width
            )

    def update(self):
        self.change_size()
        self.draw()


class Particle1(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, alpha_decay_speed: int):
        super().__init__()
        self.image = pg.image.load(
            "images/particles/particle_1.png").convert_alpha()
        self.image = pg.transform.rotozoom(
            self.image, 0, uniform(0.8, 1.5))
        self.rect = self.image.get_rect(
            center=(randrange(0, 20) + x, randrange(0, 20) + y))
        self.dir = randrange(-180, 180)
        self.speed = randrange(4, 8)
        self.image.set_alpha(randrange(180, 255))
        self.alpha_decay_speed = alpha_decay_speed
        self.despawn_timer = 0

    def movement(self):
        self.rect.x += self.speed * cos(radians(self.dir))
        self.rect.y += self.speed * sin(radians(self.dir))

    def animate(self):
        alpha = self.image.get_alpha()
        if alpha > 0:
            self.image.set_alpha(alpha - self.alpha_decay_speed)
        else:
            self.kill()

    def update(self):
        self.movement()
        self.animate()
        self.despawn_timer += 1
