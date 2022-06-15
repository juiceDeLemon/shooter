import pygame as pyg
from random import randint, uniform
from math import cos, sin, radians


class GunShot:
    def __init__(self, pos, screen):
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
        if self.max_rad >= self.radius >= self.max_rad - self.decay_speed*self.fill_time:
            pyg.draw.circle(self.screen, "white", self.pos,
                            self.radius, 0)
        else:
            pyg.draw.circle(self.screen, "white", self.pos,
                            self.radius, self.width)

    def update(self):
        self.change_size()
        self.draw()


class Score(pyg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pyg.image.load(
            "graphics/particles/score.png").convert_alpha()
        self.image = pyg.transform.rotozoom(
            self.image, 0, uniform(1, 1.5))
        self.rect = self.image.get_rect(
            center=(randint(0, 20) + x, randint(0, 20) + y))
        self.dir = randint(-180, 180)
        self.speed = randint(4, 8)
        self.alpha = randint(180, 230)
        self.image.set_alpha(self.alpha)

    def add(self):
        keys = pyg.key.get_pressed()
        if keys[pyg.K_SPACE]:
            pyg.event.post(pyg.event.Event(pyg.USEREVENT+1))

    def movement(self):
        self.rect.x += self.speed * cos(radians(self.dir))
        self.rect.y += self.speed * sin(radians(self.dir))

    def animate(self):
        if self.alpha >= 0:
            self.alpha -= 5
            self.image.set_alpha(self.alpha)
        else:
            self.kill()

    def update(self):
        self.movement()
        self.animate()
