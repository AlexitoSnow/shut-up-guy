import pygame.sprite
from math import ceil

from ..config.constants import PROJECTILE_SIZE, ORIGINAL_PROJECTILE_SIZE
from ..utils.resource_manager import ResourceManager


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, resource_manager: ResourceManager = None, level: int = 1):
        super().__init__(groups)

        # Determinar qué imagen usar según el rango de nivel (cada 5 niveles)
        level_range = ceil(level / 5)
        shoot_image = resource_manager.load_image(f'shoot_{(level_range-1)*5 + 1}_{level_range*5}.png', 'shoot')

        # Crear superficie temporal del tamaño original
        temp_surface = pygame.Surface(ORIGINAL_PROJECTILE_SIZE, pygame.SRCALPHA)
        temp_surface.blit(shoot_image, (0, 0))

        # Escalar al tamaño de renderizado
        self.original_image = pygame.transform.scale(temp_surface, PROJECTILE_SIZE)
        self.image = self.original_image
        self.rect = self.image.get_frect(midbottom=pos)

        self.angle = 0
        self.rotation_speed = 5

        # Velocidad inicial más baja y aceleración
        self.speed = 4  # Velocidad inicial reducida (antes era 10)
        self.max_speed = 7  # Velocidad máxima
        self.acceleration = 0.1  # Aceleración gradual

    def rotate(self):
        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        # Mantener el centro del rect en la posición correcta después de rotar
        center = self.rect.center
        self.rect = self.image.get_frect()
        self.rect.center = center

    def movement(self):
        # Aplicar aceleración hasta alcanzar la velocidad máxima
        if self.speed < self.max_speed:
            self.speed += self.acceleration

        self.rect.y -= self.speed

        # Si sale de la pantalla, destruir el proyectil
        if self.rect.bottom < 0:
            self.kill()

    def update(self):
        self.movement()
        self.rotate()
