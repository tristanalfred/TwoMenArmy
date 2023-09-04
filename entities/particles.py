import datetime
import random
import pygame as pg


class Particle:
    def __init__(self, game, center):
        self.game = game
        self.center = center
        self.start_time = datetime.datetime.now()

    def update(self):
        pass

    def display(self):
        pass


class GroupParticle(Particle):
    def __init__(self, game, center):
        super().__init__(game, center)
        self.children_particles = []
        self.num_children_created = 0
        self.max_children = 0

    def display(self):
        for particle in self.children_particles:
            particle.display()


class DestroyGroupParticle(GroupParticle):
    def __init__(self, game, center):
        super().__init__(game, center)
        self.max_children = 15

    def update(self):
        if self.num_children_created < self.max_children:
            new_particle = DestroyParticle(self.game,
                                           (self.center[0] + random.randint(-15, 15),
                                            self.center[1] + random.randint(-15, 15)),
                                           self)
            self.children_particles.append(new_particle)
            self.num_children_created += 1

        for particle in self.children_particles:
            particle.update()


class DestroyParticle(Particle):
    def __init__(self, game, center, group_particle):
        super().__init__(game, center)
        self.group_particle = group_particle
        self.life_span_ms = random.randint(150000, 200000)
        self.max_radius = random.randint(15, 20)
        self.radius = 0
        self.max_width = 5
        self.color = random.choice(["grey", (120, 120, 120)])

    def update(self):
        delta_life = (datetime.datetime.now() - self.start_time).microseconds
        self.radius = delta_life / self.life_span_ms * self.max_radius  # Radius grow with time

        if (datetime.datetime.now() - self.start_time).microseconds > self.life_span_ms:
            self.group_particle.children_particles.remove(self)

    def display(self):
        pg.draw.circle(self.game.game_mgmt.screen, self.color, self.center, self.radius)


class HitParticle(Particle):
    def __init__(self, game, center):
        super().__init__(game, center)
        self.life_span_ms = random.randint(150000, 200000)
        self.max_radius = random.randint(15, 20)
        self.radius = 0
        self.max_width = 5
        self.width = 1
        self.color = "grey"

    def update(self):
        delta_life = (datetime.datetime.now() - self.start_time).microseconds
        self.radius = delta_life / self.life_span_ms * self.max_radius  # Radius grow with time
        self.width = self.max_width - int((delta_life/self.life_span_ms) * self.max_width)  # Thickness reduce with time

        if (datetime.datetime.now() - self.start_time).microseconds > self.life_span_ms:
            self.game.all_particles.remove(self)

    def display(self):
        pg.draw.circle(self.game.game_mgmt.screen, self.color, self.center, self.radius, width=self.width)
