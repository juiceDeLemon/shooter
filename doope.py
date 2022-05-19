import pygame as pyg
import math
import random
import json
from sys import exit

# todo: fix bouncy meatball

SCN_W, SCN_H = 1200, 900  # screen width and height

pyg.init()
screen = pyg.display.set_mode((SCN_W, SCN_H))
clock = pyg.time.Clock()
background_surf = pyg.image.load("graphics/background.png").convert_alpha()
pyg.mouse.set_visible(False)


class Player(pyg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        with open("deeta/deeta.json", "r") as f:
            data = json.load(f)

        self.image = pyg.image.load("graphics/player/gun.png").convert_alpha()
        self.orig_img = self.image
        self.rect = self.image.get_rect(  # spawn in the centre of the screen
            center=(SCN_W/2, SCN_H/2))
        self.pos = pyg.math.Vector2(SCN_W/2, SCN_H/2)

        self.type = "basic"

        self.health = data["player"][self.type]["health"]
        self.speed = data["player"][self.type]["speed"]
        self.max_ammo = data["player"][self.type]["max_ammo"]
        self.cool_down = data["player"][self.type]["cool_down"]

    def movement(self):
        """
        Player is moved when key pressed.
        """
        keys = pyg.key.get_pressed()
        if keys[pyg.K_w]:
            self.rect.y -= self.speed
        elif keys[pyg.K_a]:
            self.rect.x -= self.speed
        elif keys[pyg.K_s]:
            self.rect.y += self.speed
        elif keys[pyg.K_d]:
            self.rect.x += self.speed
        return self.rect.centerx, self.rect.centery

    def rotation(self):
        """
        Make player rotate towards mouse.
        Bullet also shoot in this direction, but uses a different function
        (same mechanism).
        """
        _, angle = (pyg.mouse.get_pos()-self.pos).as_polar()
        self.image = pyg.transform.rotozoom(self.orig_img, -angle-90, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.pos = pyg.Vector2(self.rect.centerx, self.rect.centery)
        self.movement()
        self.rotation()


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


class GunParticle(pyg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pyg.image.load("graphics/particles/gun_particle.png")
        # self.pos = pos
        self.rect = self.image.get_rect(center=pos)
        self.list = []

    def emit(self):
        pass

    def add(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass


class Enemies(pyg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.type = random.choice(
        #     ("asteroid", "fast", "comet", "sniper"), weights=(40, 30, 10, 20))

        with open("deeta/deeta.json", "r") as f:
            data = json.load(f)

        # self.health = data["enemies"][self.type]["health"]
        # self.damage = data["enemies"][self.type]["damage"]

        self.image = pyg.image.load(
            "graphics/enemies/asteroid/asteroid.png").convert_alpha()
        self.orig_img = self.image
        self.mask = pyg.mask.from_surface(self.image)
        self.seat = random.choices(
            (range(1, 13)), weights=(1, 3, 3, 1, 3, 3, 1, 3, 3, 1, 3, 3))[0]
        self.SPIN_ANGLE = 2
        self.spin = 0

        """
        Using self.seat that is randomly chosen earlier,
        each case have different positions to choose from.
        Different positions have different chances to enhance hit rate.
        """
        match self.seat:
            case 1:
                self.dir = 315
                self.rect = self.image.get_rect(bottomright=(0, 0))
            case 2:
                self.dir = random.choices(
                    (225, 270, 315), weights=(1, 2, 2))[0]
                self.rect = self.image.get_rect(midbottom=(SCN_W/3, 0))
            case 3:
                self.dir = random.choices(
                    (225, 270, 315), weights=(2, 2, 1))[0]
                self.rect = self.image.get_rect(midbottom=(SCN_W/3*2, 0))
            case 4:
                self.dir = 225
                self.rect = self.image.get_rect(bottomleft=(SCN_W, 0))
            case 5:
                self.dir = random.choices(
                    (135, 180, 225), weights=(1, 2, 2))[0]
                self.rect = self.image.get_rect(midleft=(SCN_W, SCN_H/3))
            case 6:
                self.dir = random.choices(
                    (135, 180, 225), weights=(2, 2, 1))[0]
                self.rect = self.image.get_rect(midleft=(SCN_W, SCN_H/3*2))
            case 7:
                self.dir = 135
                self.rect = self.image.get_rect(topleft=(SCN_W, SCN_H))
            case 8:
                self.dir = random.choices((45, 90, 135), weights=(1, 2, 2))[0]
                self.rect = self.image.get_rect(midtop=(SCN_W, SCN_H/3*2))
            case 9:
                self.dir = random.choices((45, 90, 135), weights=(2, 2, 1))[0]
                self.rect = self.image.get_rect(midtop=(SCN_W, SCN_H/3))
            case 10:
                self.dir = 45
                self.rect = self.image.get_rect(topright=(0, SCN_H))
            case 11:
                self.dir = random.choices((315, 0, 45), weights=(1, 2, 2))[0]
                self.rect = self.image.get_rect(midright=(0, SCN_H/3*2))
            case 12:
                self.dir = random.choices((315, 0, 45), weights=(2, 2, 1))[0]
                self.rect = self.image.get_rect(midright=(0, SCN_H/3))

        self.dir += random.randint(-35, 35)
        self.speed = data["enemies"]["asteroid"]["speed"]

    def movement(self):
        """
        Move self.speed tiles in the direction self.dir per frame.
        Speed is defined in deeta.json and direction is chose in def __init__.
        """
        self.rect.x += math.cos(math.radians(self.dir))*self.speed
        self.rect.y -= math.sin(math.radians(self.dir))*self.speed

    def bouncy_meetball(self):  # pointless extra code but it's god damn funny
        """
        Pointless code that slows down the code but this is god damn funny.
        """
        self.image = pyg.transform.rotozoom(self.orig_img, self.spin, 1)
        self.spin += self.SPIN_ANGLE
        self.spin = 0 if self.spin == 360 else self.spin

    def spin_enemy(self):
        """
        This is bouncy meatball with fix.
        """
        self.bouncy_meetball()

    def collision(self, object, pierce):
        """This is pixel perfect collision. """
        pyg.sprite.spritecollide()

    def delete(self):
        """
        Deletes enemies that when whatever reason.
        """
        self.kill()

    def update(self):
        self.movement()
        # self.spin_enemy()


class Cursor(pyg.sprite.Sprite):
    def __init__(self, cursor):
        super().__init__()
        self.image = pyg.image.load(cursor).convert_alpha()
        self.rect = self.image.get_rect()

    def follow(self):
        self.rect.x, self.rect.y = pyg.mouse.get_pos()

    def update(self):
        self.follow()


# sprites
player = Player()
player_group = pyg.sprite.GroupSingle()
player_group.add(player)
bullets_group = pyg.sprite.Group()
enemies_group = pyg.sprite.Group()
cursor_group = pyg.sprite.GroupSingle()
cursor_group.add(Cursor("graphics/cursors/cross.png"))
# - gun_particle_group = pyg.sprite.Group()

# technical
timer = 0
spawn_frequency = 45
spawn_enemy = pyg.event.Event(pyg.USEREVENT + 0)

while True:
    screen.blit(background_surf, (0, 0))
    player_x, player_y = player.movement()

    # enemy spawning?!
    timer += 1
    if timer % 45 == 0:
        pyg.event.post(spawn_enemy)
        spawn_frequency = random.randint(35, 50)

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            exit()

        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_SPACE:
                bullets_group.add(Bullets(player_x, player_y))
                # GunParticle().add()

        if event.type == pyg.USEREVENT + 0:
            enemies_group.add(Enemies())

    cursor_group.draw(screen)
    cursor_group.update()

    player_group.draw(screen)
    player_group.update()

    bullets_group.draw(screen)
    bullets_group.update()
    # if not screen.get_rect().collidepoint(bullet.pos):
    #     bullets.remove(bullet)

    enemies_group.draw(screen)
    enemies_group.update()

    pyg.display.flip()
    clock.tick(60)
