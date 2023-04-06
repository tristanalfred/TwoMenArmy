import datetime
import random


class Particle:
    def __init__(self, game, center):
        self.game = game
        self.center = center
        self.start_time = datetime.datetime.now()

    def update(self):
        pass


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
