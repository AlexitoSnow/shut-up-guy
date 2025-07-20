import pygame
from pygame.locals import *

from config.constants import GROUND, SCREEN_WIDTH
from entity.Projectile import Projectile


class Player (pygame.sprite.Sprite):
    def __init__(self, surfaces: list, camera_input_handler=None):
        super().__init__()

        self.original_surfaces = surfaces
        self.flipped_surfaces = [pygame.transform.flip(surface, True, False) for surface in surfaces]
        self.char_run = surfaces

        self.run_index = 0
        self.image = self.char_run[self.run_index]
        self.rect = self.image.get_frect(midbottom=(100, GROUND))

        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown_duration = 500

        self.direction = 1

        self.projectile_group = pygame.sprite.Group()
        self.camera_input_handler = camera_input_handler

    def shoot_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def player_input(self):
        keys = pygame.key.get_pressed()
        direction = 0

        # Input por cámara
        if self.camera_input_handler:
            # Movimiento con dedos juntos
            if self.camera_input_handler.is_index_extended():
                cam_dir = self.camera_input_handler.get_direction()
                if cam_dir != 0:
                    direction = cam_dir

            # Disparo con pulgar recogido
            if not self.camera_input_handler.is_thumb_extended() and self.can_shoot:
                self.shoot()

        # Input por teclado
        if keys[K_SPACE] and self.can_shoot:
            self.shoot()

        # Control de movimiento por teclado
        if direction == 0:
            if keys[K_LEFT]:
                direction = -1
            elif keys[K_RIGHT]:
                direction = 1

        if direction != 0:
            self.direction = direction
            self.char_run = self.flipped_surfaces if direction == -1 else self.original_surfaces
            self.rect.x += 5 * self.direction

        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0: self.rect.left = 0

    def shoot(self):
        if self.can_shoot:
            print("¡Disparo detectado!") # Debug
            self.projectile_group.add(Projectile(self.rect.midtop, self.projectile_group))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def animation_state(self):
        self.run_index += 0.1
        if self.run_index >= len(self.char_run): self.run_index = 0
        if self.direction == -1:
            self.image = self.flipped_surfaces[int(self.run_index)]
        else:
            self.image = self.char_run[int(self.run_index)]
        # Update the rect to match the new image size
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def update(self):
        self.player_input()
        self.animation_state()
        self.shoot_timer()
