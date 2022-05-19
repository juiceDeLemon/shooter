import pygame as pyg
import math

class Bullets(pyg.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        mouse_x, mouse_y = pyg.mouse.get_pos()
        self.dir = (mouse_x - x, mouse_y - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        self.angle = math.atan2(-self.dir[1], self.dir[0])
        self.image = pyg.image.load(
            "graphics/bullets/gun_bullet.png").convert_alpha()
        self.image = pyg.transform.rotate(self.image, math.degrees(self.angle))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 25
        self.mask = pyg.mask.from_surface(self.image)

    def movement(self):
        angle = math.atan2(self.dir[1], self.dir[0])
        self.rect.x += math.cos(angle)*self.speed
        self.rect.y += math.sin(angle)*self.speed

    def update(self):
        self.movement()

bullets_group = pyg.sprite.Group()

while True:
    screen.blit(background_surf, (0, 0))
    player_x, player_y = player.movement()

    for event in pyg.event.get():

        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_SPACE:
                bullets_group.add(Bullets(player_x, player_y))

    bullets_group.draw(screen)
    bullets_group.update()

    pyg.display.flip()
    clock.tick(60)
