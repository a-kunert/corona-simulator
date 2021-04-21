import sys
import random

import pygame

from circle import Circle
from settings import Settings


class Game:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Corona-Simulator')
        self.circles = pygame.sprite.Group()
        self.circles.add(Circle.create(self).infect())
        for k in range(1, self.settings.count):
            self.circles.add(Circle.create(self))

    def run_game(self):
        while True:
            self._check_events()
            self.circles.update()
            self._check_collisions()
            self._update_screen()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for circle in self.circles:
            circle.draw()
        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                sys.exit()
            if event.type == pygame.QUIT:
                sys.exit()

    def _check_collisions(self):
        collisions = pygame.sprite.groupcollide(self.circles, self.circles, False, False)
        for reference, colliding in collisions.items():
            colliding.remove(reference)
            for circle in colliding:
                reference.collide(circle)


if __name__ == "__main__":
    Game().run_game()
