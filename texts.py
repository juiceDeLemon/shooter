import deeta.settings as settings

import pygame as pyg


class Score(pyg.sprite.Sprite):
    def __init__(self, size: int, score: int):
        super().__init__()
        self.max_size = self.current_size = size
        self.time = 0
        self.score = score
        self.image = pyg.font.Font(settings.NORMAL_F, self.max_size).render(
            f"{self.score}", False, "White")
        self.rect = self.image.get_rect(
            center=(settings.WIDTH/2, 17))

    def change_score(self):
        self.score += 1
        self.current_size *= 1.5

    def update(self):
        self.font = pyg.font.Font(
            f"{settings.NORMAL_F}", int(self.current_size))
        self.image = self.font.render(
            f"{self.score+self.time}", True, "White")
        self.rect = self.image.get_rect(
            center=(settings.WIDTH/2, 17))
        self.current_size += 0.2*(self.max_size-self.current_size)


class TimeText:
    def __init__(self, screen: pyg.Surface):
        self.font = pyg.font.Font(settings.NORMAL_F, 50)
        self.pos = (settings.WIDTH/2, settings.HEIGHT/2-20)
        self.screen = screen

    def get_time(self):
        import time
        current_time = time.strftime("%H:%M", time.localtime())
        self.image = self.font.render(current_time, False, "white")

    def update(self):
        self.get_time()
        self.screen.blit(self.image, self.pos)
