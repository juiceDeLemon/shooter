import pygame as pyg
import math
import random
import json
import deeta.settings as settings
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
            data = json.load(f)

        self.image = pyg.image.load("graphics/player/gun.png").convert_alpha()
        self.orig_img = self.image
        self.rect = self.image.get_rect(  # spawn in the centre of the screen
            center=(settings.WIDTH/2, settings.HEIGHT/2))
        self.pos = pyg.math.Vector2(settings.WIDTH/2, settings.HEIGHT/2)

        self.type = "basic"
        self.health = data["player"][self.type]["health"]
        self.speed = data["player"][self.type]["speed"]
        self.max_ammo = data["player"][self.type]["max_ammo"]
        self.cool_down = data["player"][self.type]["cool_down"]

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
        self.image = pyg.transform.rotate(self.orig_img, -angle-90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def die(self):
        if self.health <= 0:
            print("You died")
            pyg.event.post(pyg.event.Event(pyg.QUIT))

    def update(self):
        self.die()
        self.pos = pyg.Vector2(self.rect.centerx, self.rect.centery)
        self.movement()


class Bullets(pyg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        with open("deeta/deeta.json", "r") as f:
            data = json.load(f)

        mouse_x, mouse_y = pyg.mouse.get_pos()
        self.dir = (mouse_x - x, mouse_y - y)
        length = math.hypot(*self.dir)
        self.dir = (
            0, -1) if length == 0.0 else (self.dir[0]/length, self.dir[1]/length)
        self.angle = math.atan2(-self.dir[1], self.dir[0])
        self.image = pyg.image.load(
            "graphics/bullets/gun_bullet.png").convert_alpha()
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
            data = json.load(f)

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
        self.despawn_timer += 1
        if self.despawn_timer >= 5*fps:
            self.kill()
        if self.health <= 0:
            self.kill()

    def collision(self):
        # bullets (take damage)
        for bullets in bullets_group:
            if self.rect.colliderect(bullets.rect):
                bullets.kill()
                self.health -= bullets.damage
                self.alpha_frame = 1
                self.image.set_alpha(50)

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


class PlayerHealth:
    def __init__(self):
        self.font = pyg.font.Font(settings.NORMAL_F, 75)
        self.get_health()
        self.rect = self.image.get_rect(center=(settings.WIDTH/2, 25))

    def get_health(self):
        current_health = f"{player.health}"
        self.image = self.font.render(current_health, False, "white")

    def update(self):
        self.get_health()
        screen.blit(self.image, self.rect)


class Cursor(pyg.sprite.Sprite):
    def __init__(self, cursor):
        super().__init__()
        self.image = pyg.image.load(cursor).convert_alpha()
        self.rect = self.image.get_rect()

    def move(self):
        self.rect.x, self.rect.y = pyg.mouse.get_pos()

    def update(self):
        self.move()


# sprites:
# player
player = Player()
player_group = pyg.sprite.GroupSingle()
player_group.add(player)
bullets_group = pyg.sprite.Group()
# enemies
enemies_group = pyg.sprite.Group()
# cursor
cursor_group = pyg.sprite.GroupSingle()
cursor_group.add(Cursor("graphics/cursors/cross.png"))

# others
enemy_spawn_timer = 0
spawn_rate = 40

logo()

while True:
    screen.fill(bg_colour)

    # enemy spawning
    enemy_spawn_timer += 1
    if enemy_spawn_timer == spawn_rate:
        enemy_spawn_timer = 0
        enemies_group.add(Enemies())
        spawn_rate = random.randint(40, 65)

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            exit()

        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_SPACE:  # shoot bullet
                bullets_group.add(
                    Bullets(player.rect.centerx, player.rect.centery))

    # draw and update groups/classes
    cursor_group.draw(screen)
    cursor_group.update()

    player_group.draw(screen)
    player_group.update()

    bullets_group.draw(screen)
    bullets_group.update()

    enemies_group.draw(screen)
    enemies_group.update()

    PlayerHealth().update()

    pyg.display.flip()
    clock.tick(fps)
