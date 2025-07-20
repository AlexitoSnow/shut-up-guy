from os.path import join

import pygame.sprite

from config import IMAGES


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join(IMAGES, 'char_jump.png')).convert_alpha()
        self.rect = self.image.get_frect(midbottom=pos)
        self.speed = 10

        #self.mask = pygame.mask.from_surface(self.image)

    def movement(self):
        self.rect.y -= self.speed
        if self.rect.top <= 0:
            self.kill()

    def update(self):
        self.movement()