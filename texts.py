import pygame as pyg
import deeta.settings as settings


pyg.font.init()


class Score(pyg.sprite.Sprite):
    def __init__(self, size: int):
        super().__init__()
        self.max_size = self.current_size = size
        self.image = pyg.font.Font(settings.NORMAL_F, self.max_size).render(
            "", False, "White")
        self.rect = self.image.get_rect(
            center=(settings.WIDTH / 2, 40))

    def change_score(self):
        self.current_size *= 1.2

    def update(self):
        import main
        self.font = pyg.font.Font(
            f"{settings.NORMAL_F}", int(self.current_size))
        self.image = self.font.render(
            f"{int(main.score)}", True, "White")
        self.rect = self.image.get_rect(
            center=(settings.WIDTH / 2, 40))
        self.current_size += 0.2 * (self.max_size - self.current_size)


class TimeText:
    def __init__(self, screen: pyg.Surface):
        self.font = pyg.font.Font(settings.NORMAL_F, 50)
        self.pos = (settings.WIDTH / 2, settings.HEIGHT / 2 - 20)
        self.screen = screen

    def get_time(self):
        import time
        current_time = time.strftime("%H:%M", time.localtime())
        self.image = self.font.render(current_time, False, "white")

    def update(self):
        self.get_time()
        self.screen.blit(self.image, self.pos)


class Stats:
    def __init__(self, screen: pyg.Surface):
        super().__init__()
        self.font = pyg.font.Font(settings.NORMAL_F, 20)
        self.texts_left: list[str] = []  # texts to be blitted
        self.texts_right: list[str] = []
        self.y = 80  # starting y pos
        self.screen = screen

    def get_stats_left(self):
        import main
        import platform
        return [
            int(settings.CLOCK.get_fps()),  # fps
            len(main.enemies_group),  # current amount of enemies
            len(main.bullets_group),  # current amount of bullets
            main.player.health,  # health
            str(main.player.rect.center)[1:-1],  # player pos no brackets
            str(pyg.mouse.get_pos())[1:-1],  # cursor pos no brackets
            platform.processor()  # processor
        ]

    def stats_stats_right(self):
        from main import total_bullets, enemies_killed, time_played
        return [
            total_bullets,  # total bullets
            enemies_killed,  # enemies killed
            time_played // 60  # time played
        ]

    def update(self):
        new_line_spacing = 0
        # left
        stats_left = self.get_stats_left()
        self.texts_left = [
            f"FPS: {stats_left[0]}",
            f"Enemies: {stats_left[1]}",
            f"Bullets: {stats_left[2]}",
            f"Health: {stats_left[3]}",
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
            f"Time played: {stats_right[2]}"
        ]
        for text in self.texts_right:
            text = self.font.render(text, False, "white")
            new_line_spacing += 20
            self.screen.blit(
                text, (settings.WIDTH - 20 - text.get_width(), self.y + new_line_spacing))


title = pyg.font.Font(settings.NORMAL_F, 120).render(
    "SHOOTER", False, "White")
