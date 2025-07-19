import time
from random import randint
from os.path import join

import pygame.sprite

from src.config import IMAGES, SCREEN_WIDTH
from src.utils import Timer


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, surfaces: list, enemy_type: str):
        super().__init__()

        y_pos = 200

        self.original_surfaces = surfaces
        self.flipped_surfaces = [pygame.transform.flip(surface, True, False) for surface in surfaces]
        self.frames = surfaces

        if enemy_type == FLY:
            y_pos -= 100

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_frect(center=(randint(100, SCREEN_WIDTH - 100), y_pos))
        self.type = type
        self.direction = 1

        self.lifetime = Timer(5000, autostart=True, func=self.kill)

        #self.mask = pygame.mask.from_surface(self.image)

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        if self.direction == -1:
            self.image = self.flipped_surfaces[int(self.animation_index)]
        else:
            self.image = self.frames[int(self.animation_index)]

    # If the obstacle goes to the border, change direction
    def movement(self):
        self.rect.x += 5 * self.direction
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction *= -1

    def update(self):
        self.movement()
        self.animation_state()
        self.lifetime.update()

FLY = 'fly'
ENEMY = 'enemy'