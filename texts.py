import pygame as pg
import data.configuration as config


pg.font.init()


class Score(pg.sprite.Sprite):
    def __init__(self, size: int):
        super().__init__()
        self.max_size = self.current_size = size
        self.image = pg.font.Font(config.NORMAL_F, self.max_size).render(
            "", False, "White")
        self.rect = self.image.get_rect(
            center=(config.WIDTH / 2, 40))

    def change_score(self):
        self.current_size *= 1.2

    def update(self):
        import main
        self.font = pg.font.Font(
            f"{config.NORMAL_F}", int(self.current_size))
        self.image = self.font.render(
            f"{int(main.score)}", True, "White")
        self.rect = self.image.get_rect(
            center=(config.WIDTH / 2, 40))
        self.current_size += 0.2 * (self.max_size - self.current_size)


class TimeText:
    def __init__(self, screen: pg.Surface):
        self.font = pg.font.Font(config.NORMAL_F, 50)
        self.pos = (config.WIDTH / 2, config.HEIGHT / 2 - 20)
        self.screen = screen

    def get_time(self):
        import time
        current_time = time.strftime("%H:%M", time.localtime())
        self.image = self.font.render(current_time, False, "white")

    def update(self):
        self.get_time()
        self.screen.blit(self.image, self.pos)


class Stats:
    def __init__(self, screen: pg.Surface):
        super().__init__()
        # self.font = pg.font.Font(config.NORMAL_F, 20)
        self.font = pg.font.Font("fonts/menlo.ttf", 20)
        self.texts_left: list[str] = []  # texts to be blitted
        self.texts_right: list[str] = []
        self.y = 80  # starting y pos
        self.screen = screen

    def get_stats_left(self):
        import main
        import platform
        return [
            int(config.CLOCK.get_fps()),  # fps
            len(main.enemies_group),  # current amount of enemies
            len(main.bullets_group),  # current amount of bullets
            len(main.enemies_group) + len(main.bullets_group) + \
            len(main.particles_group) + \
            len(main.player_group),  # total entities
            str(main.player_class.rect.center)[1:-1],  # player pos no brackets
            str(pg.mouse.get_pos())[1:-1],  # cursor pos no brackets
            platform.processor()  # processor
        ]

    def stats_stats_right(self):
        import main
        return [
            main.total_bullets,  # total bullets
            main.enemies_killed,  # enemies killed
            main.player_class.health,  # health
            f"{format(main.score, '.4f')}",  # actual score
            main.time_played // 60  # time played
        ]

    def update(self):
        new_line_spacing = 0
        # left
        stats_left = self.get_stats_left()
        self.texts_left = [
            f"FPS: {stats_left[0]}",
            f"Enemies: {stats_left[1]}",
            f"Bullets: {stats_left[2]}",
            f"Entities: {stats_left[3]}",
            f"Player pos: {stats_left[4]}",
            f"Cursor pos: {stats_left[5]}",
            f"Processor: {stats_left[6]}"
        ]
        for text in self.texts_left:
            text = self.font.render(text, False, "white")
            new_line_spacing += 20  # 20 is the font size
            self.screen.blit(
                text, (20, self.y + new_line_spacing))  # 20 is the x
        new_line_spacing = 0
        # right
        stats_right = self.stats_stats_right()
        self.texts_right = [
            f"Total bullets: {stats_right[0]}",
            f"Enemies killed: {stats_right[1]}",
            f"Health: {stats_right[2]}",
            f"Actual score: {stats_right[3]}",
            f"Time played: {stats_right[4]}"
        ]
        for text in self.texts_right:
            text = self.font.render(text, False, "white")
            new_line_spacing += 20
            self.screen.blit(
                text, (config.WIDTH - 20 - text.get_width(), self.y + new_line_spacing))


title = pg.font.Font(config.NORMAL_F, 120).render(
    "SHOOTER", False, "White")
