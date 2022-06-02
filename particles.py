import math
import pygame as pyg
import random


class GunShotParticle:
    def __init__(self, max_rad, pos, width, decay_speed, fill_time, screen):
        self.pos = pos
        self.max_rad = self.radius = max_rad
        self.width = width
        self.decay_speed = decay_speed
        self.fill_time = fill_time
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


class ScoreParticle(pyg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pyg.image.load(
            "graphics/particles/score_particle.png").convert_alpha()
        self.image = pyg.transform.rotozoom(
            self.image, 0, random.uniform(1, 1.5))
        self.rect = self.image.get_rect(
            center=(random.randint(0, 20) + x, random.randint(0, 20) + y))
        self.dir = random.randint(-180, 180)
        self.speed = random.randint(4, 8)
        self.alpha = random.randint(180, 230)
        self.image.set_alpha(self.alpha)

    def add(self):
        keys = pyg.key.get_pressed()
        if keys[pyg.K_SPACE]:
            pyg.event.post(pyg.event.Event(pyg.USEREVENT+1))

    def movement(self):
        self.rect.x += self.speed * math.cos(math.radians(self.dir))
        self.rect.y += self.speed * math.sin(math.radians(self.dir))

    def animate(self):
        if self.alpha >= 0:
            self.alpha -= 5
            self.image.set_alpha(self.alpha)
        else:
            self.kill()

    def update(self):
        self.movement()
        self.animate()
