import pygame as pyg
import math
import random
# --------------------------------------------------
import particles
import buttons
import otherui
import texts
import deeta.settings as settings
# --------------------------------------------------
from json import load
from sys import exit


def logo():
    print(" ____    __  __  _____   _____   ______ ____    ____        ______            ")
    print("/\\  _`\\ /\\ \\/\\ \\/\\  __`\\/\\  __`\\/\\__  _/\\  _`\\ /\\  _`\\     /\\__  _\\/'\\_/`\\    ")
    print("\\ \\,\\L\\_\\ \\ \\_\\ \\ \\ \\/\\ \\ \\ \\/\\ \\/_/\\ \\\\ \\ \\L\\_\\ \\ \\L\\ \\   \\/_/\\ \\/\\      \\   ")
    print(" \\/_\\__ \\\\ \\  _  \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\\\ \\  _\\L\\ \\ ,  /      \\ \\ \\ \\ \\__\\ \\  ")
    print("   /\\ \\L\\ \\ \\ \\ \\ \\ \\ \\_\\ \\ \\ \\_\\ \\ \\ \\ \\\\ \\ \\L\\ \\ \\ \\\\ \\      \\ \\ \\ \\ \\_/\\ \\ ")
    print("   \\ `\\____\\ \\_\\ \\_\\ \\_____\\ \\_____\\ \\ \\_\\\\ \\____/\\ \\_\\ \\_\\     \\ \\_\\ \\_\\\\ \\_\\")
    print("    \\/_____/\\/_/\\/_/\\/_____/\\/_____/  \\/_/ \\/___/  \\/_/\\/ /      \\/_/\\/_/ \\/_/")


pyg.init()
screen = pyg.display.set_mode(
    (settings.WIDTH, settings.HEIGHT))
bg_colour = "#1D282E"
clock = pyg.time.Clock()
fps = 60
pyg.mouse.set_visible(False)


class Player(pyg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        with open("deeta/deeta.json", "r") as f:
            data = load(f)

        self.image = self.orig_img = pyg.image.load(
            "graphics/player/gun.png").convert_alpha()
        self.rect = self.image.get_rect(  # spawn at the centre of the screen
            center=(settings.WIDTH/2, settings.HEIGHT/2))
        self.pos = pyg.math.Vector2(settings.WIDTH/2, settings.HEIGHT/2)

        self.type = "basic"
        self.health = self.max_health = self.ani_health = data["player"][self.type]["health"]
        self.speed = data["player"][self.type]["speed"]
        self.max_ammo = data["player"][self.type]["max_ammo"]
        self.cool_down = data["player"][self.type]["cool_down"]

        self.max_health_to_health_bar_max_length_ratio = self.max_health / 400
        self.heart_img = pyg.image.load(
            "graphics/ui/health_bar/heart.png").convert_alpha()
        self.heart_rect = self.heart_img.get_rect(topleft=(10, 10))

    def movement(self):
        keys = pyg.key.get_pressed()
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

        _, angle = (pyg.mouse.get_pos()-self.pos).as_polar()
        # picture rotated 90°
        self.image = pyg.transform.rotate(self.orig_img, -angle-90)
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
                self.max_health_to_health_bar_max_length_ratio

        # x = 70, y = 25 is the offset from the top left corner of the screen
        # 54, 400 is the height and the max length of the health bar

        # background
        pyg.draw.rect(screen, bg_colour, pyg.Rect(70, 25, 400, 54))
        # bar rect
        bar_rect = pyg.Rect(
            70, 25, int(self.ani_health / self.max_health_to_health_bar_max_length_ratio), 54)
        # animation bar
        ani_bar_rect = pyg.Rect(bar_rect.right, 70, ani_width, 54)
        pyg.draw.rect(screen, "#646464", ani_bar_rect)
        # bar
        pyg.draw.rect(screen, "#dddddd", bar_rect, 0, 12)
        # bar shade
        # 25+54-20 = offset + (height - shade height)
        pyg.draw.rect(screen, "#afafaf", pyg.Rect(
            70, 25+54-20, self.health / self.max_health_to_health_bar_max_length_ratio, 20),
            0, border_bottom_left_radius=12, border_bottom_right_radius=12)
        # frame
        pyg.draw.rect(screen, "#ffffff", pyg.Rect(
            70, 25, 400, 54), 5, border_top_right_radius=12, border_bottom_right_radius=12)
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
        length = math.hypot(*self.dir)
        self.dir = (
            0, -1) if length == 0.0 else (self.dir[0]/length, self.dir[1]/length)
        self.angle = math.atan2(-self.dir[1], self.dir[0])
        self.image = pyg.image.load(
            "graphics/bullets/gun.png").convert_alpha()
        self.image = pyg.transform.rotate(self.image, math.degrees(self.angle))
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = data["player"]["basic"]["bullet_speed"]
        self.damage = data["player"]["basic"]["damage"]

    def movement(self):
        angle = math.atan2(self.dir[1], self.dir[0])
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)

    def update(self):
        self.movement()


class Enemies(pyg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        with open("deeta/deeta.json", "r") as f:
            data = load(f)

        self.image = self.orig_img = pyg.image.load(
            "graphics/enemies/asteroid/asteroid.png").convert_alpha()
        self.spawn_pt = random.choices(
            (range(1, 13)), weights=(1, 3, 3, 1, 3, 3, 1, 3, 3, 1, 3, 3))[0]

        self.alpha_frame = 0
        self.despawn_timer = 0

        match self.spawn_pt:
            case 1:
                self.dir = 315
                self.rect = self.image.get_rect(bottomright=(0, 0))
            case 2:
                self.dir = random.choices(
                    (225, 270, 315), weights=(1, 2, 2))[0]
                self.rect = self.image.get_rect(
                    midbottom=(settings.WIDTH/3, 0))
            case 3:
                self.dir = random.choices(
                    (225, 270, 315), weights=(2, 2, 1))[0]
                self.rect = self.image.get_rect(
                    midbottom=(settings.WIDTH/3*2, 0))
            case 4:
                self.dir = 225
                self.rect = self.image.get_rect(bottomleft=(settings.WIDTH, 0))
            case 5:
                self.dir = random.choices(
                    (135, 180, 225), weights=(1, 2, 2))[0]
                self.rect = self.image.get_rect(
                    midleft=(settings.WIDTH, settings.HEIGHT/3))
            case 6:
                self.dir = random.choices(
                    (135, 180, 225), weights=(2, 2, 1))[0]
                self.rect = self.image.get_rect(
                    midleft=(settings.WIDTH, settings.HEIGHT/3*2))
            case 7:
                self.dir = 135
                self.rect = self.image.get_rect(
                    topleft=(settings.WIDTH, settings.HEIGHT))
            case 8:
                self.dir = random.choices((45, 90, 135), weights=(1, 2, 2))[0]
                self.rect = self.image.get_rect(
                    midtop=(settings.WIDTH, settings.HEIGHT/3*2))
            case 9:
                self.dir = random.choices((45, 90, 135), weights=(2, 2, 1))[0]
                self.rect = self.image.get_rect(
                    midtop=(settings.WIDTH, settings.HEIGHT/3))
            case 10:
                self.dir = 45
                self.rect = self.image.get_rect(topright=(0, settings.HEIGHT))
            case 11:
                self.dir = random.choices((315, 0, 45), weights=(1, 2, 2))[0]
                self.rect = self.image.get_rect(
                    midright=(0, settings.HEIGHT/3*2))
            case 12:
                self.dir = random.choices((315, 0, 45), weights=(2, 2, 1))[0]
                self.rect = self.image.get_rect(
                    midright=(0, settings.HEIGHT/3))

        self.dir += random.randint(-35, 35)
        self.angle = 0

        self.speed = data["enemies"]["asteroid"]["speed"] + \
            random.uniform(-0.7, 0.7)
        self.health = data["enemies"]["asteroid"]["health"]
        self.damage = data["enemies"]["asteroid"]["damage"]
        self.cool_down = data["enemies"]["asteroid"]["cool_down"]

    def movement(self):
        self.rect.x += self.speed * math.cos(math.radians(self.dir))
        self.rect.y -= self.speed * math.sin(math.radians(self.dir))

    def despawn(self):
        global score
        self.despawn_timer += 1
        if self.despawn_timer >= 5*fps:
            self.kill()
        if self.health <= 0:
            score_class.change_score()
            score += 2 + self.speed
            self.kill()

    def collision(self):
        global score
        # bullets (take damage)
        for bullet in bullets_group:
            if self.rect.colliderect(bullet.rect):
                score += 1
                score_class.change_score()
                bullet.kill()
                gun_shot_particle_list.append(
                    particles.GunShot((bullet.rect.x, bullet.rect.y), screen))
                self.health -= bullet.damage
                self.alpha_frame = 1
                # self.image.set_alpha(50)

        # player (deal damage)
        if self.rect.colliderect(player.rect):
            player.health -= self.damage
            self.kill()

    def animation(self):
        self.angle = 0 if self.angle == 360 else self.angle + 3
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
        self.despawn()
        self.collision()
        self.movement()
        self.animation()
        # self.flash()


# variables
score = 0
spawn_rate = 40
# timers
enemy_spawn_timer = 0
score_timer = 0
# sprites:
# player
player = Player()
player_group = pyg.sprite.GroupSingle()
player_group.add(player)
# --------------------------------------------------
bullets_group = pyg.sprite.Group()
# enemies
enemies_group = pyg.sprite.Group()
# particles
gun_shot_particle_list = []
# cursor
cursor_group = pyg.sprite.GroupSingle()
cursor_group.add(otherui.Cursor("graphics/ui/cursors/cross.png"))
# texts
# score_class = texts.Score(50, score)
score_class = texts.Score(70)
score_group = pyg.sprite.GroupSingle()
score_group.add(score_class)
# buttons:
# quit button
quit_button = buttons.QuitButton(screen)


logo()

while True:
    screen.fill(bg_colour)

    # enemy spawning
    enemy_spawn_timer += 1
    if enemy_spawn_timer == spawn_rate:
        enemy_spawn_timer = 0
        enemies_group.add(Enemies())
        spawn_rate = random.randint(40, 65)

    score_timer += 1
    if score_timer == fps:
        score_timer = 0
        score += 1
        score_class.change_score()

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            print(
                "-------------------------------------------------------------------------------\n")
            pyg.quit()
            exit()

        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_SPACE:  # shoot bullet
                bullets_group.add(
                    Bullets(player.rect.centerx, player.rect.centery))
            elif event.key == pyg.K_ESCAPE:
                player.health += 17
                score -= 30
            elif event.key == pyg.K_1:
                cursor_group.empty()
                cursor_group.add(otherui.Cursor(
                    "graphics/ui/cursors/cross.png"))
            elif event.key == pyg.K_2:
                cursor_group.empty()
                cursor_group.add(otherui.Cursor(
                    "graphics/ui/cursors/circle_dot.png"))

        if event.type == pyg.MOUSEBUTTONDOWN:
            # quit button
            if quit_button.rect.collidepoint(event.pos):
                quit_button.image.set_alpha(100)
                if event.button == 1:
                    quit_button()

    # draw and update groups/classes
    bullets_group.draw(screen)
    bullets_group.update()

    enemies_group.draw(screen)
    enemies_group.update()

    for particle in gun_shot_particle_list:
        particle.update()
        if particle.radius <= 0:
            gun_shot_particle_list.remove(particle)

    quit_button.update()

    player_group.draw(screen)
    player_group.update()

    score_group.draw(screen)
    score_group.update()

    cursor_group.draw(screen)
    cursor_group.update()

    pyg.display.flip()
    clock.tick(fps)
