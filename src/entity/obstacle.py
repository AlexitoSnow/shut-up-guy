from os.path import join
from random import randint, choice, random

import pygame.sprite

from ..config.constants import SCREEN_WIDTH, ENTITY_SIZE, ORIGINAL_ENTITY_SIZE, SOUNDS
from src.utils import Timer
from src.utils.resource_manager import ResourceManager

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, resources: ResourceManager, lifetime=5000, movement_speed=5):
        super().__init__()

        # Cargar sonidos de risa
        self.laugh_sounds = [
            pygame.mixer.Sound(join(SOUNDS, 'child_laugh_1.mp3')),
            pygame.mixer.Sound(join(SOUNDS, 'child_laugh_2.mp3'))
        ]

        self.kill_sound = pygame.mixer.Sound(join(SOUNDS, 'child_dying.mp3'))

        # Ajustar volumen de las risas
        for sound in self.laugh_sounds:
            sound.set_volume(0.4)

        self.kill_sound.set_volume(0.4)

        # Posiciones posibles en Y
        self.POSITIONS_Y = [100, 200]
        y_pos = choice(self.POSITIONS_Y)

        # Elegir aleatoriamente entre boy y girl
        enemy_type = choice(['boy', 'girl'])
        frames_count = 4 if enemy_type == 'boy' else 2  # boy tiene 4 frames, girl tiene 2

        # Cargar spritesheets según el tipo elegido
        width, height = ORIGINAL_ENTITY_SIZE

        moving_left_sheet = resources.load_image(f'{enemy_type}_left.png', enemy_type)
        self.moving_left = []
        for i in range(frames_count):
            frame = pygame.Surface((width, height), pygame.SRCALPHA)
            frame.blit(moving_left_sheet, (0, 0), (i * width, 0, width, height))
            frame = pygame.transform.scale(frame, ENTITY_SIZE)
            self.moving_left.append(frame)

        moving_right_sheet = resources.load_image(f'{enemy_type}_right.png', enemy_type)
        self.moving_right = []
        for i in range(frames_count):
            frame = pygame.Surface((width, height), pygame.SRCALPHA)
            frame.blit(moving_right_sheet, (0, 0), (i * width, 0, width, height))
            frame = pygame.transform.scale(frame, ENTITY_SIZE)
            self.moving_right.append(frame)

        self.direction = 1
        self.animation_index = 0
        self.animation_speed = 0.2
        self.movement_speed = movement_speed
        self.frames_count = frames_count

        # Variables para el movimiento aleatorio
        self.direction_timer = 0
        self.min_direction_time = 800  # Reducido de 1000 para cambios más frecuentes
        self.max_direction_time = 2000  # Reducido de 3000 para más dinamismo
        self.next_direction_change = randint(self.min_direction_time, self.max_direction_time)
        self.direction_change_chance = 0.4  # 40% de probabilidad (reducido de 60% para no ser tan errático)

        # Probabilidad de cambiar dirección al tocar borde
        self.border_bounce_chance = 0.7  # 70% de probabilidad de rebotar en bordes

        # Inicializar con el primer frame
        self.frames = self.moving_right if self.direction == 1 else self.moving_left
        self.image = self.frames[0]
        self.rect = self.image.get_frect(center=(randint(100, SCREEN_WIDTH - 100), y_pos))

        self.lifetime = Timer(lifetime, autostart=True, func=self.kill)

    def play_random_laugh(self):
        if random() < 0.5:  # 50% de probabilidad de reír
            choice(self.laugh_sounds).play()

    def animation_state(self):
        self.animation_index = (self.animation_index + self.animation_speed) % self.frames_count
        self.frames = self.moving_right if self.direction == 1 else self.moving_left
        self.image = self.frames[int(self.animation_index)]

    def movement(self):
        current_time = pygame.time.get_ticks()
        self.direction_timer += pygame.time.get_delta_time() if hasattr(pygame.time, 'get_delta_time') else 16

        # Cambiar dirección aleatoriamente
        if self.direction_timer >= self.next_direction_change:
            if random() < self.direction_change_chance:
                self.direction *= -1
            self.direction_timer = 0
            self.next_direction_change = randint(self.min_direction_time, self.max_direction_time)

        # Mover el enemigo
        self.rect.x += self.movement_speed * self.direction

        # Verificar bordes con probabilidad de rebote o wrap-around
        if self.rect.left <= 0:
            if random() < self.border_bounce_chance:
                self.direction = 1
                self.rect.left = 0
            else:
                # Si no rebota, aparece por el otro lado
                self.rect.left = SCREEN_WIDTH - self.rect.width
        elif self.rect.right >= SCREEN_WIDTH:
            if random() < self.border_bounce_chance:
                self.direction = -1
                self.rect.right = SCREEN_WIDTH
            else:
                # Si no rebota, aparece por el otro lado
                self.rect.right = self.rect.width

    def update(self):
        self.movement()
        self.animation_state()
        self.lifetime.update()

    def kill(self):
        self.kill_sound.play()
        super().kill()
