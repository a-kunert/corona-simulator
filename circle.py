import math
import random

import pygame
from pygame.sprite import Sprite

from settings import Settings


class Circle(Sprite):

    def __init__(self, game, position=(0, 0), velocity=(1, 1)):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.radius = game.settings.radius
        self.speed = game.settings.speed
        self.colors = {
            's': game.settings.susceptible_color,
            'i': game.settings.infected_color,
            'r': game.settings.recovered_color
        }
        self.rect = pygame.Rect(position[0], position[1], 2 * self.radius, 2 * self.radius)
        self.x = self.rect.x
        self.y = self.rect.y
        self.direction = velocity
        self.temp_direction = None
        self.infected_at = None
        self.mode = 's'  # susceptible

    def update(self):

        self._recover()

        if self.rect.left < 0 or self.rect.right > self.screen_rect.width:
            self.direction = (-self.direction[0], self.direction[1])
        if self.rect.top < 0 or self.rect.bottom > self.screen_rect.height:
            self.direction = (self.direction[0], -self.direction[1])

        direction = tuple(coord * self.speed for coord in self._normalize(self.direction))
        self.x += direction[0]
        self.y += direction[1]
        self.rect.x = self.x
        self.rect.y = self.y

    def collide(self, circle):
        if self.is_infected():
            circle.contaminate()
        if circle.temp_direction:
            self.direction = (circle.temp_direction[0] + random.randrange(-10, 10) / 50,
                              circle.temp_direction[1] + random.randrange(-10, 10) / 50)
            circle.temp_direction = None
        else:
            self.temp_direction = self.direction
            self.direction = (circle.direction[0], circle.direction[1])

    def draw(self):
        pygame.draw.circle(self.screen, self._color(), self.rect.center, self.radius)

    def infect(self):
        if self.mode == 's':
            self.mode = 'i'
            self.infected_at = pygame.time.get_ticks()
        return self

    def contaminate(self):
        if random.randrange(1, 100) < Settings().infection_probability:
            self.infect()

    def _color(self):
        return self.colors[self.mode]

    def is_infected(self):
        return self.mode == 'i'

    @staticmethod
    def _normalize(vector):
        length = sum([coord ** 2 for coord in vector])
        length = math.sqrt(length)
        return (coord / length for coord in vector)

    @staticmethod
    def create(game):
        settings = Settings()
        screen_rect = game.screen.get_rect()
        x = random.randint(settings.radius, screen_rect.width - settings.radius)
        y = random.randint(settings.radius, screen_rect.height - settings.radius)
        position = (x, y)
        direction = random.randint(0, int(1000 * math.pi)) / 1000
        velocity = (math.sin(direction), math.cos(direction))
        return Circle(game, position, velocity)

    def _recover(self):
        if not self.is_infected():
            return
        if pygame.time.get_ticks() - self.infected_at > 15000:
            self.mode = 'r'
