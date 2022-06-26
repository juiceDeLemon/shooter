from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame as pg
import buttons
import otherui
import particles
import texts
import data.configuration as config
import data.audios as audios

from random import choices, choice, randrange, uniform
from math import hypot, atan2, degrees, cos, sin, radians
from sys import exit
from json import load


pg.init()
pg.display.set_caption("SHOOTER")
pg.mouse.set_visible(False)
pg.mixer.pre_init(44100, -16, 2, 512)
pg.mixer.set_num_channels(32)
pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.MOUSEBUTTONDOWN])
screen = pg.display.set_mode(
    (config.WIDTH, config.HEIGHT), pg.HWSURFACE | pg.DOUBLEBUF)
monitor_info = pg.display.Info()
version = "v0.2.1"
# for later use: start = 0, game = 1, menu = 2, settings = 3, end = 4
game_state = 1


def change_score(amount: int):
    global score
    score += amount
    score_class.change_score()


def change_game_state(state: int):
    global game_state
    game_state = state


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        with open("data/data.json", "r") as f:
            data = load(f)

        self.image = self.orig_img = pg.image.load(
            "images/player/gun.png").convert_alpha()
        self.rect = self.image.get_rect(  # spawn at the centre of the screen
            center=(config.WIDTH / 2, config.HEIGHT / 2))
        self.pos = pg.math.Vector2(
            config.WIDTH / 2, config.HEIGHT / 2)
        self.mask = pg.mask.from_surface(self.image)
        self.mask.fill()
        self.alpha_frame = 0

        self.type = "basic"
        self.health = self.max_health = self.ani_health = data["player"][self.type]["health"]
        self.speed = data["player"][self.type]["speed"]
        self.max_ammo = data["player"][self.type]["max_ammo"]
        self.cool_down = data["player"][self.type]["cool_down"]

        # self.ratio refers to [max health : health bar max length] ratio
        self.ratio = self.max_health / (config.WIDTH / 3)
        self.heart_img = pg.image.load(
            "images/ui/health_bar/heart.png").convert_alpha()
        self.heart_rect = self.heart_img.get_rect(topleft=(10, 10))

    def movement(self):
        if keys[pg.K_w]:
            if self.rect.midtop[1] >= 0:
                self.rect.y -= self.speed
        elif keys[pg.K_a]:
            if self.rect.midleft[0] >= 0:
                self.rect.x -= self.speed
        elif keys[pg.K_s]:
            if self.rect.midbottom[1] <= config.HEIGHT:
                self.rect.y += self.speed
        elif keys[pg.K_d]:
            if self.rect.midright[0] <= config.WIDTH:
                self.rect.x += self.speed

        _, angle = (pg.mouse.get_pos() - self.pos).as_polar()
        # picture rotated 90°
        self.image = pg.transform.rotate(self.orig_img, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def die_test(self):
        if self.health <= 0:
            pg.event.post(pg.event.Event(pg.QUIT))

    def attack(self):
        choice(audios.PLAYER_ATTACK).play()
        bullets_group.add(Bullets())

    def health_bar(self):
        ani_width = 0

        # 1 is transition speed
        if not self.ani_health == self.health:
            if self.ani_health < self.health - 1:
                self.ani_health += 1
            elif self.ani_health > self.health + 1:
                self.ani_health -= 1
            else:
                self.ani_health = self.health
            ani_width = (self.health - self.ani_health) / \
                self.ratio

        # x = 70, y = 25 is the offset from the top left corner of the screen
        # 54, config.WIDTH/3 (400) is the height and the max length of the health bar
        # 5 is frame width, 12 is corner radius

        # background
        pg.draw.rect(screen, config.BG_COLOUR, pg.Rect(
            70, 25, config.WIDTH / 3, 54),
            border_top_right_radius=12, border_bottom_right_radius=12)

        # bar rect
        bar_rect = pg.Rect(
            70, 25, int(self.ani_health / self.ratio), 54)
        # animation bar
        ani_bar_rect = pg.Rect(bar_rect.right, 70, ani_width, 54)
        pg.draw.rect(screen, "#646464", ani_bar_rect)
        # bar
        pg.draw.rect(screen, "#dddddd", bar_rect, 0, 12)
        # bar shade
        # 25 + 54 - 20 = offset + (height - shade height)
        pg.draw.rect(screen, "#afafaf", pg.Rect(
            70, 25 + 54 - 20, self.health / self.ratio, 20),
            0, border_bottom_left_radius=12, border_bottom_right_radius=12)
        # frame
        pg.draw.rect(screen, "#ffffff", pg.Rect(
            70, 25, config.WIDTH / 3, 54), 5,
            border_top_right_radius=12, border_bottom_right_radius=12)
        # heart
        screen.blit(self.heart_img, self.heart_rect)

    def update(self):
        self.pos = pg.Vector2(self.rect.centerx, self.rect.centery)
        self.die_test()
        self.movement()
        otherui.flash(self, config.FLASH_DUR)
        self.health_bar()


class Bullets(pg.sprite.Sprite):
    """
    I have no idea what this does. 
    Don't ask me where did I got this.
    The site probably starts with "s" and ends with "s".
    Props to that guy. I forgot his name.
    # 
    """

    def __init__(self):
        super().__init__()
        with open("data/data.json", "r") as f:
            data = load(f)

        mouse_x, mouse_y = pg.mouse.get_pos()
        self.dir = (mouse_x - player_class.rect.centerx,
                    mouse_y - player_class.rect.centery)
        length = hypot(*self.dir)
        self.dir = (
            0, -1) if length == 0.0 else (self.dir[0] / length, self.dir[1] / length)
        self.angle = atan2(-self.dir[1], self.dir[0])
        self.image = pg.image.load(
            "images/bullets/gun.png").convert_alpha()
        self.image = pg.transform.rotate(self.image, degrees(self.angle))
        self.rect = self.image.get_rect(
            center=(player_class.rect.centerx, player_class.rect.centery))
        self.mask = pg.mask.from_surface(self.image)

        self.speed = data["player"]["basic"]["bullet_speed"]
        self.damage = data["player"]["basic"]["damage"]

        self.despawn_timer = 0

    def movement(self):
        angle = atan2(self.dir[1], self.dir[0])
        self.rect.x += self.speed * cos(angle)
        self.rect.y += self.speed * sin(angle)

    def despawn(self):
        self.despawn_timer += 1
        if self.despawn_timer >= 5 * config.FPS:
            self.kill()

    def update(self):
        self.despawn()
        self.movement()


class Enemies(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        with open("data/data.json", "r") as f:
            data = load(f)

        self.image = self.orig_img = pg.image.load(
            "images/enemies/asteroid/asteroid.png").convert_alpha()
        self.spawn_pt = choices(
            (range(1, 13)), weights=(1, 3, 3, 1, 3, 3, 1, 3, 3, 1, 3, 3))[0]
        self.mask = pg.mask.from_surface(self.image); self.mask.fill()

        self.alpha_frame = 0
        self.despawn_timer = 0
        self.rotation_angle = randrange(2, 4)

        match self.spawn_pt:
            case 1:
                self.dir = 315
                self.rect = self.image.get_rect(bottomright=(0, 0))
            case 2:
                self.dir = choices(
                    (225, 270, 315), weights=(1, 2, 2))[0]
                self.rect = self.image.get_rect(
                    midbottom=(config.WIDTH / 3, 0))
            case 3:
                self.dir = choices(
                    (225, 270, 315), weights=(2, 2, 1))[0]
                self.rect = self.image.get_rect(
                    midbottom=(config.WIDTH / 3 * 2, 0))
            case 4:
                self.dir = 225
                self.rect = self.image.get_rect(
                    bottomleft=(config.WIDTH, 0))
            case 5:
                self.dir = choices(
                    (135, 180, 225), weights=(1, 2, 2))[0]
                self.rect = self.image.get_rect(
                    midleft=(config.WIDTH, config.HEIGHT / 3))
            case 6:
                self.dir = choices(
                    (135, 180, 225), weights=(2, 2, 1))[0]
                self.rect = self.image.get_rect(
                    midleft=(config.WIDTH, config.HEIGHT / 3 * 2))
            case 7:
                self.dir = 135
                self.rect = self.image.get_rect(
                    topleft=(config.WIDTH, config.HEIGHT))
            case 8:
                self.dir = choices((45, 90, 135), weights=(1, 2, 2))[0]
                self.rect = self.image.get_rect(
                    midtop=(config.WIDTH, config.HEIGHT / 3 * 2))
            case 9:
                self.dir = choices((45, 90, 135), weights=(2, 2, 1))[0]
                self.rect = self.image.get_rect(
                    midtop=(config.WIDTH, config.HEIGHT / 3))
            case 10:
                self.dir = 45
                self.rect = self.image.get_rect(
                    topright=(0, config.HEIGHT))
            case 11:
                self.dir = choices((315, 0, 45), weights=(1, 2, 2))[0]
                self.rect = self.image.get_rect(
                    midright=(0, config.HEIGHT / 3 * 2))
            case 12:
                self.dir = choices((315, 0, 45), weights=(2, 2, 1))[0]
                self.rect = self.image.get_rect(
                    midright=(0, config.HEIGHT / 3))

        self.dir += randrange(-35, 35)
        self.angle = 0

        self.speed = data["enemies"]["asteroid"]["speed"] + \
            uniform(-0.7, 0.7)
        self.speed = round(self.speed, 4)
        self.health = data["enemies"]["asteroid"]["health"]
        self.damage = data["enemies"]["asteroid"]["damage"]
        self.cool_down = data["enemies"]["asteroid"]["cool_down"]

    def movement(self):
        self.rect.x += self.speed * cos(radians(self.dir))
        self.rect.y -= self.speed * sin(radians(self.dir))

    def despawn(self):
        global enemies_killed
        self.despawn_timer += 1
        if self.despawn_timer >= 5 * config.FPS:
            self.kill()
        elif self.health <= 0:
            for _ in range(50):
                particles_group.add(
                    particles.Particle1(self.rect.centerx, self.rect.centery, 5))
            enemies_killed += 1
            choice(audios.ENEMIES_DIE).play()
            change_score(2 + self.speed)
            self.kill()

    def collision(self):
        # bullets (take damage)
        for bullet in bullets_group:
            if self.rect.colliderect(bullet.rect):
                if pg.sprite.collide_mask(bullet, self):
                    choice(audios.DAMAGED).play()
                    change_score(1)
                    bullet.kill()
                    gun_shot_particle_list.append(
                        particles.GunShot((bullet.rect.x, bullet.rect.y), screen))
                    self.health -= bullet.damage
                    self.alpha_frame = 1

        # player (deal damage)
        if self.rect.colliderect(player_class.rect):
            if pg.sprite.collide_mask(player_class, self):
                choice(audios.DAMAGED).play()
                player_class.alpha_frame = 1
                player_class.health -= self.damage
                self.kill()

    def rotation(self):
        self.angle = 0 if self.angle == 360 else self.angle + self.rotation_angle
        self.image = pg.transform.rotate(
            self.orig_img, self.angle)
        self.rect = self.image.get_rect(topleft=(self.rect.centerx - int(
            self.image.get_width() / 2), self.rect.centery - int(self.image.get_height() / 2)))

    def update(self):
        self.mask = pg.mask.from_surface(self.image)
        self.despawn()
        self.collision()
        self.movement()
        self.rotation()
        otherui.flash(self, config.FLASH_DUR)


# variables:
score = 0
spawn_rate = 40
total_bullets = 0
enemies_killed = 0
time_played = 0
# timers:
enemy_spawn_timer = 0
score_timer = 0
# entities:
# player
player_class = Player()
player_group = pg.sprite.GroupSingle(player_class)
bullets_group = pg.sprite.Group()
# enemies
enemies_group = pg.sprite.Group()
# ui elements:
# particles
gun_shot_particle_list: list[particles.GunShot] = []
particles_group = pg.sprite.Group()
# cursor
cursor_class = otherui.Cursor("images/ui/cursors/cross.png")
cursor_group = pg.sprite.GroupSingle(cursor_class)
# health bar
health_bar_group = pg.sprite.Group()
# texts
version_surf = pg.font.Font(
    "fonts/menlo.ttf", 20).render(version, False, "white")
# menu
menu_title = pg.image.load("images/ui/menu/paused.png").convert_alpha()
menu_title = pg.transform.rotozoom(menu_title, 0, 0.9)
menu_title_rect = menu_title.get_rect(midtop=(config.WIDTH / 2, 70))
# score_class = texts.Score(50, score)
score_class = texts.Score(70)
score_group = pg.sprite.GroupSingle(score_class)
# stats
stats_class = texts.Stats(screen)
# buttons:
resume_button_class = buttons.Resume()
settings_button_class = buttons.Settings()
quit_button_class = buttons.Quit()
menu_buttons_group = pg.sprite.Group(
    resume_button_class,
    settings_button_class,
    quit_button_class
)
# sliders:
# music_slider_class = buttons.MusicVol(screen)
# settings_sliders_group = pg.sprite.Group(
#     music_slider_class
# )

while True:
    screen.fill(config.BG_COLOUR)
    time_played += 1
    keys = pg.key.get_pressed()

    # event loop
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:  # shoot bullet
                player_class.attack()
                total_bullets += 1
            if event.key == pg.K_ESCAPE:
                audios.HOVER.play()
                change_game_state(2 if game_state != 2 else 1)

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if game_state == 2:
                    if resume_button_class.rect.collidepoint(event.pos):
                        resume_button_class()
                        audios.SELECT.play()
                    if settings_button_class.rect.collidepoint(event.pos):
                        settings_button_class()
                        audios.SELECT.play()
                    if quit_button_class.rect.collidepoint(event.pos):
                        quit_button_class()
                        audios.SELECT.play()

        if event.type == pg.QUIT:
            print(
                f"-------------------------------------------------------------------------------\n{int(score)}")
            pg.quit()
            exit()

    if game_state == 1:  # game
        score = round(score, 4)  # prevent crazy digits
        # enemy spawning
        enemy_spawn_timer += 1
        if enemy_spawn_timer == spawn_rate:
            enemy_spawn_timer = 0
            enemies_group.add(Enemies())
            spawn_rate = randrange(40, 65)

        # 1 pt/sec
        score_timer += 1
        if score_timer == config.FPS:
            score_timer = 0
            change_score(1)

        # draw and update groups/classes
        particles_group.update()
        particles_group.draw(screen)

        bullets_group.update()
        bullets_group.draw(screen)

        enemies_group.update()
        enemies_group.draw(screen)

        for particle in gun_shot_particle_list:
            particle.update()
            if particle.radius <= 0:
                gun_shot_particle_list.remove(particle)

        player_group.update()
        player_group.draw(screen)

        score_group.update()
        score_group.draw(screen)

        if keys[pg.K_TAB]:
            stats_class.update()
    elif game_state == 2:  # menu
        # title
        screen.blit(menu_title, menu_title_rect)
        # group
        menu_buttons_group.update()
        menu_buttons_group.draw(screen)
        # version number
        screen.blit(
            version_surf, ((config.WIDTH - version_surf.get_width()) / 2, 700))
    elif game_state == 3:  # settings
        # pg.draw.rect(screen, "white", pg.Rect(200, 200, 375, 45))
        # pg.draw.rect(screen, "red", pg.Rect(250, 200 - (60 - 45) / 2, 45, 60))
        # settings_sliders_group.update()
        # settings_sliders_group.draw(screen)
        ...

    cursor_group.update()
    cursor_group.draw(screen)

    pg.display.flip()
    config.CLOCK.tick(config.FPS)
