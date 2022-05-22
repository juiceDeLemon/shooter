import pygame as pyg
from random import uniform
from sys import exit


class Score(pyg.sprite.Sprite):
    def __init__(self, font, text, size, colour, position, score):
        super().__init__()
        self.text = text
        self.size = size
        self.font = pyg.font.Font(f"{font}", self.size)
        self.colour = colour
        self.time = 0
        self.score = score
        self.image = self.font.render(f"{self.score}", True, self.colour)
        self.orig_img = self.image
        self.rect = self.image.get_rect(center=position)

        self.change_timer = 0
        self.animation_state = 1

    def animation(self):
        if self.change_timer % 20 == 0:
            self.animation_state *= -1
        match self.animation_state:
            case 1:
                self.time += 1
            case -1:
                self.time -= 1
        self.font = pyg.font.Font(f"{font}", self.size+self.time)

        # see multithreading tutorial
        # or see griffpatch tutorial
        # if all of above doesn't work, then go see the basic tutorial lol

    def change_score(self):
        self.score += 1
        self.image = self.font.render(
            f"{self.score+self.time}", True, self.colour)

    def update(self):
        self.animation()


class ScoreParticle:
    def __init__(self):
        self.particles = []

    def emit(self):
        if self.particles:
            self.delete()
            for particle in self.particles:
                particle[0][1] += particle[2][0]
                particle[0][0] += particle[2][1]
                particle[1] -= 0.2
                pyg.draw.circle(screen, pyg.Color("White"),
                                particle[0], int(particle[1]))
                # screen.blit("graphics/particles/gun_particle.png", )

    def add(self):
        x = score_class.rect.centerx
        y = score_class.rect.y+40
        radius = 10
        dir_x = uniform(-3, 3)
        dir_y = uniform(-3, 3)
        particle_circle = [[x, y], radius, [dir_x, dir_y]]
        self.particles.append(particle_circle)

    def delete(self):
        particle_copy = [
            particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy

    def start(self):
        keys = pyg.key.get_pressed()
        if keys[pyg.K_SPACE]:
            self.emit()


pyg.init()

fps = 60
fps_clock = pyg.time.Clock()

width, height = 500, 500
screen = pyg.display.set_mode((width, height))

score = 0
font = "fonts/normal.otf"
timer = 0

score_class = Score(font, f"{score}", 50, "White", (width/2, 20), score)
score_group = pyg.sprite.GroupSingle()
score_group.add(score_class)

particles = ScoreParticle()
PARTICLE_EVENT = pyg.USEREVENT + 1
pyg.time.set_timer(PARTICLE_EVENT, 50)

while True:
    screen.fill((0, 0, 0))

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            exit()

        if event.type == PARTICLE_EVENT:
            particles.add()

        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_SPACE:  # shoot bullet
                score_class.change_score()
        elif event.type == pyg.KEYUP:
            particles.particles = []

    score_group.draw(screen)
    score_group.update()

    particles.start()

    pyg.display.flip()
    fps_clock.tick(fps)
