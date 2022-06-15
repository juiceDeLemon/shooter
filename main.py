from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame as pyg
import buttons
import otherui
import particles
import texts
import deeta.settings as settings

from random import randint, choices, uniform
from math import hypot, atan2, degrees, cos, sin, radians
from sys import exit
from json import load


pyg.init()
pyg.display.set_caption("SHOOTER")
pyg.mouse.set_visible(False)
screen = pyg.display.set_mode(
    (settings.WIDTH, settings.HEIGHT), pyg.HWSURFACE | pyg.DOUBLEBUF)
monitor_info = pyg.display.Info()
pyg.event.set_allowed([pyg.QUIT, pyg.KEYDOWN, pyg.MOUSEBUTTONDOWN])
# for later use: start = -1, game = 0, menu = 1, end = 2
# play again = start
game_state = False


def shake(*sprites: pyg.sprite.Sprite):
    for sprite in sprites:
        sprite.rect.x += randint(-1, 1)
    yield
    for sprite in sprites:
        sprite.rect.x -= randint(-1, 1)
    yield


def change_score(amount):
    global score
    score += amount
    score_class.change_score()


class Player(pyg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        with open("deeta/deeta.json", "r") as f:
            data = load(f)

        self.image = self.orig_img = pyg.image.load(
            "graphics/player/gun.png").convert_alpha()
        self.rect = self.image.get_rect(  # spawn at the centre of the screen
            center=(settings.WIDTH / 2, settings.HEIGHT / 2))
        self.pos = pyg.math.Vector2(settings.WIDTH / 2, settings.HEIGHT / 2)
        self.mask = pyg.mask.from_surface(self.image)
        self.mask.fill()

        self.type = "basic"
        self.health = self.max_health = self.ani_health = data["player"][self.type]["health"]
        self.speed = data["player"][self.type]["speed"]
        self.max_ammo = data["player"][self.type]["max_ammo"]
        self.cool_down = data["player"][self.type]["cool_down"]

        # the following variable refers to [max health:health bar max length] ratio
        self.ratio = self.max_health / (settings.WIDTH / 3)
        self.heart_img = pyg.image.load(
            "graphics/ui/health_bar/heart.png").convert_alpha()
        self.heart_rect = self.heart_img.get_rect(topleft=(10, 10))

    def movement(self):
        # keys = pyg.key.get_pressed()
        if keys[pyg.K_w]:
            if self.rect.midtop[1] >= 0:
                self.rect.y -= self.speed
        elif keys[pyg.K_a]:
            if self.rect.midleft[0] >= 0:
                self.rect.x -= self.speed
        elif keys[pyg.K_s]:
            if self.rect.midbottom[1] <= settings.HEIGHT:
                self.rect.y += self.speed
        elif keys[pyg.K_d]:
            if self.rect.midright[0] <= settings.WIDTH:
                self.rect.x += self.speed

        _, angle = (pyg.mouse.get_pos() - self.pos).as_polar()
        # picture rotated 90°
        self.image = pyg.transform.rotate(self.orig_img, -angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def die_test(self):
        if self.health <= 0:
            pyg.event.post(pyg.event.Event(pyg.QUIT))

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
        # 54, settings.WIDTH is the height and the max length of the health bar

        # background
        pyg.draw.rect(screen, settings.BG_COLOUR, pyg.Rect(
            70, 25, settings.WIDTH / 3, 54),
            border_top_right_radius=12, border_bottom_right_radius=12)

        # bar rect
        bar_rect = pyg.Rect(
            70, 25, int(self.ani_health / self.ratio), 54)
        # animation bar
        ani_bar_rect = pyg.Rect(bar_rect.right, 70, ani_width, 54)
        pyg.draw.rect(screen, "#646464", ani_bar_rect)
        # bar
        pyg.draw.rect(screen, "#dddddd", bar_rect, 0, 12)
        # bar shade
        # 25+54-20 = offset + (height - shade height)
        pyg.draw.rect(screen, "#afafaf", pyg.Rect(
            70, 25 + 54 - 20, self.health / self.ratio, 20),
            0, border_bottom_left_radius=12, border_bottom_right_radius=12)
        # frame
        pyg.draw.rect(screen, "#ffffff", pyg.Rect(
            70, 25, settings.WIDTH / 3, 54), 5,
            border_top_right_radius=12, border_bottom_right_radius=12)
        # heart
        screen.blit(self.heart_img, self.heart_rect)

    def update(self):
        self.die_test()
        self.pos = pyg.Vector2(self.rect.centerx, self.rect.centery)
        self.movement()
        self.health_bar()


class Bullets(pyg.sprite.Sprite):
    """
    I have no idea what this does. 
    Don't ask me where did I got this.
    It probably starts with "S" and ends with "W".
    """

    def __init__(self, x, y):
        super().__init__()
        with open("deeta/deeta.json", "r") as f:
            data = load(f)

        mouse_x, mouse_y = pyg.mouse.get_pos()
        self.dir = (mouse_x - x, mouse_y - y)
        length = hypot(*self.dir)
        self.dir = (
            0, -1) if length == 0.0 else (self.dir[0] / length, self.dir[1] / length)
        self.angle = atan2(-self.dir[1], self.dir[0])
        self.image = pyg.image.load(
            "graphics/bullets/gun.png").convert_alpha()
        self.image = pyg.transform.rotate(self.image, degrees(self.angle))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pyg.mask.from_surface(self.image)

        self.speed = data["player"]["basic"]["bullet_speed"]
        self.damage = data["player"]["basic"]["damage"]

        self.despawn_timer = 0

    def movement(self):
        angle = atan2(self.dir[1], self.dir[0])
        self.rect.x += self.speed * cos(angle)
        self.rect.y += self.speed * sin(angle)

    def despawn(self):
        self.despawn_timer += 1
        if self.despawn_timer >= 5 * settings.FPS:
            self.kill()

    def update(self):
        self.despawn()
        self.movement()


class Enemies(pyg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        with open("deeta/deeta.json", "r") as f:
            data = load(f)

        self.image = self.orig_img = pyg.image.load(
            "graphics/enemies/asteroid/asteroid.png").convert_alpha()
        self.spawn_pt = choices(
            (range(1, 13)), weights=(1, 3, 3, 1, 3, 3, 1, 3, 3, 1, 3, 3))[0]
        self.mask = pyg.mask.from_surface(self.image)
        self.mask.fill()

        self.alpha_frame = 0
        self.despawn_timer = 0
        self.rotation_angle = randint(2, 4)

        match self.spawn_pt:
            case 1:
                self.dir = 315
                self.rect = self.image.get_rect(bottomright=(0, 0))
            case 2:
                self.dir = choices(
                    (225, 270, 315), weights=(1, 2, 2))[0]
                self.rect = self.image.get_rect(
                    midbottom=(settings.WIDTH / 3, 0))
            case 3:
                self.dir = choices(
                    (225, 270, 315), weights=(2, 2, 1))[0]
                self.rect = self.image.get_rect(
                    midbottom=(settings.WIDTH / 3 * 2, 0))
            case 4:
                self.dir = 225
                self.rect = self.image.get_rect(bottomleft=(settings.WIDTH, 0))
            case 5:
                self.dir = choices(
                    (135, 180, 225), weights=(1, 2, 2))[0]
                self.rect = self.image.get_rect(
                    midleft=(settings.WIDTH, settings.HEIGHT / 3))
            case 6:
                self.dir = choices(
                    (135, 180, 225), weights=(2, 2, 1))[0]
                self.rect = self.image.get_rect(
                    midleft=(settings.WIDTH, settings.HEIGHT / 3 * 2))
            case 7:
                self.dir = 135
                self.rect = self.image.get_rect(
                    topleft=(settings.WIDTH, settings.HEIGHT))
            case 8:
                self.dir = choices((45, 90, 135), weights=(1, 2, 2))[0]
                self.rect = self.image.get_rect(
                    midtop=(settings.WIDTH, settings.HEIGHT / 3 * 2))
            case 9:
                self.dir = choices((45, 90, 135), weights=(2, 2, 1))[0]
                self.rect = self.image.get_rect(
                    midtop=(settings.WIDTH, settings.HEIGHT / 3))
            case 10:
                self.dir = 45
                self.rect = self.image.get_rect(topright=(0, settings.HEIGHT))
            case 11:
                self.dir = choices((315, 0, 45), weights=(1, 2, 2))[0]
                self.rect = self.image.get_rect(
                    midright=(0, settings.HEIGHT / 3 * 2))
            case 12:
                self.dir = choices((315, 0, 45), weights=(2, 2, 1))[0]
                self.rect = self.image.get_rect(
                    midright=(0, settings.HEIGHT / 3))

        self.dir += randint(-35, 35)
        self.angle = 0

        self.speed = data["enemies"]["asteroid"]["speed"] + \
            uniform(-0.7, 0.7)
        self.health = data["enemies"]["asteroid"]["health"]
        self.damage = data["enemies"]["asteroid"]["damage"]
        self.cool_down = data["enemies"]["asteroid"]["cool_down"]

    def movement(self):
        self.rect.x += self.speed * cos(radians(self.dir))
        self.rect.y -= self.speed * sin(radians(self.dir))

    def despawn(self):
        global enemies_killed
        self.despawn_timer += 1
        if self.despawn_timer >= 5 * settings.FPS:
            self.kill()
        elif self.health <= 0:
            enemies_killed += 1
            change_score(2 + self.speed)
            self.kill()

    def collision(self):
        # bullets (take damage)
        for bullet in bullets_group:
            if self.rect.colliderect(bullet.rect):
                print("collide rect")
                # if self.mask.overlap(bullet.mask, bullet_offset):
                if pyg.sprite.collide_mask(bullet, self):
                    change_score(1)
                    bullet.kill()
                    gun_shot_particle_list.append(
                        particles.GunShot((bullet.rect.x, bullet.rect.y), screen))
                    self.health -= bullet.damage
                    self.alpha_frame = 1
                    # self.image.set_alpha(50)

        # player (deal damage)
        if self.rect.colliderect(player.rect):
            if pyg.sprite.collide_mask(player, self):
                player.health -= self.damage
                self.kill()

    def rotation(self):
        self.angle = 0 if self.angle == 360 else self.angle + self.rotation_angle
        self.image = pyg.transform.rotate(
            self.orig_img, self.angle)
        self.rect = self.image.get_rect(topleft=(self.rect.centerx - int(
            self.image.get_width() / 2), self.rect.centery - int(self.image.get_height() / 2)))

    def flash(self):
        if self.alpha_frame:
            self.alpha_frame += 1
            # 0 = False, 1 = True, 2 = Start, End at 6. ↓
            if self.alpha_frame == 5 + 1:
                self.image.set_alpha(255)
                self.alpha_frame = 0

    def update(self):
        self.mask = pyg.mask.from_surface(self.image)
        self.despawn()
        self.collision()
        self.movement()
        self.rotation()
        # self.flash()


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
player = Player()
player_group = pyg.sprite.GroupSingle()
player_group.add(player)

bullets_group = pyg.sprite.Group()
# enemies
enemies_group = pyg.sprite.Group()
# ui element:
# particles
gun_shot_particle_list: list[particles.GunShot] = []
# cursor
cursor_group = pyg.sprite.GroupSingle()
cursor_group.add(otherui.Cursor("graphics/ui/cursors/cross.png"))
# health bar
health_bar_group = pyg.sprite.Group()
# texts
# score_class = texts.Score(50, score)
score_class = texts.Score(70)
score_group = pyg.sprite.GroupSingle()
score_group.add(score_class)
# stats
stats_class = texts.Stats(screen)
# buttons:
quit_button = buttons.QuitButton(screen)
change_cursor_button = buttons.ChangeCursorButton(screen)

while True:
    screen.fill(settings.BG_COLOUR)
    time_played += 1
    keys = pyg.key.get_pressed()

    # event loop
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            print(
                f"-------------------------------------------------------------------------------\n{int(score)}")
            pyg.quit()
            exit()

        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_SPACE:  # shoot bullet
                bullets_group.add(
                    Bullets(player.rect.centerx, player.rect.centery))
                total_bullets += 1
            if event.key == pyg.K_ESCAPE:
                game_state = not game_state

        if event.type == pyg.MOUSEBUTTONDOWN:
            # quit button
            if quit_button.rect.collidepoint(event.pos):
                if event.button == 1:
                    quit_button()
            # change cursor button
            if change_cursor_button.rect.collidepoint(event.pos):
                if event.button == 1:
                    change_cursor_button()

    if game_state:
        # title
        screen.blit(texts.title, (settings.WIDTH /
                    2 - texts.title.get_width() / 2, 50))
        # quit button
        quit_button.update()
        # change cursor button
        change_cursor_button.update()
    else:
        # enemy spawning
        enemy_spawn_timer += 1
        if enemy_spawn_timer == spawn_rate:
            enemy_spawn_timer = 0
            enemies_group.add(Enemies())
            spawn_rate = randint(40, 65)

        # 1 pt/sec
        score_timer += 1
        if score_timer == settings.FPS:
            score_timer = 0
            change_score(1)

        # draw and update groups/classes
        bullets_group.draw(screen)
        bullets_group.update()

        enemies_group.draw(screen)
        enemies_group.update()

        for particle in gun_shot_particle_list:
            particle.update()
            if particle.radius <= 0:
                gun_shot_particle_list.remove(particle)

        player_group.draw(screen)
        player_group.update()

        score_group.draw(screen)
        score_group.update()

        if keys[pyg.K_TAB]:
            stats_class.update()

    cursor_group.draw(screen)
    cursor_group.update()

    pyg.display.flip()
    settings.CLOCK.tick(settings.FPS)
