import pygame
from pygame.locals import *
from os.path import join

from ..config.constants import GROUND, SCREEN_WIDTH, ENTITY_SIZE, ORIGINAL_ENTITY_SIZE, SOUNDS
from .projectile import Projectile
from ..utils.resource_manager import ResourceManager


class Player(pygame.sprite.Sprite):
    def __init__(self, resource_manager: ResourceManager, game, camera_input_handler=None, bullet_count=-1, current_level=1):
        super().__init__()
        self.game = game

        # Cargar sonidos
        self.walking_sound = pygame.mixer.Sound(join(SOUNDS, 'walking.mp3'))
        self.shooting_sound = pygame.mixer.Sound(join(SOUNDS, 'shooting.mp3'))

        # Ajustar volumen (opcional)
        self.walking_sound.set_volume(0.5)
        self.shooting_sound.set_volume(0.5)

        # Variable para controlar el sonido de caminar
        self.is_walking_sound_playing = False

        # Cargar spritesheets y recortar frames usando tamaño original
        width, height = ORIGINAL_ENTITY_SIZE

        # Standing tiene 3 frames
        standing_sheet = resource_manager.load_image('teacher_standing.png', 'teacher')
        self.standing_frames = []
        for i in range(3):
            frame = pygame.Surface((width, height), pygame.SRCALPHA)
            frame.blit(standing_sheet, (0, 0), (i * width, 0, width, height))
            # Escalar al tamaño de renderizado
            frame = pygame.transform.scale(frame, ENTITY_SIZE)
            self.standing_frames.append(frame)

        # Moving left/right tienen 2 frames cada uno
        moving_left_sheet = resource_manager.load_image('teacher_moving_left.png', 'teacher')
        self.moving_left = []
        for i in range(2):
            frame = pygame.Surface((width, height), pygame.SRCALPHA)
            frame.blit(moving_left_sheet, (0, 0), (i * width, 0, width, height))
            frame = pygame.transform.scale(frame, ENTITY_SIZE)
            self.moving_left.append(frame)

        moving_right_sheet = resource_manager.load_image('teacher_moving_right.png', 'teacher')
        self.moving_right = []
        for i in range(2):
            frame = pygame.Surface((width, height), pygame.SRCALPHA)
            frame.blit(moving_right_sheet, (0, 0), (i * width, 0, width, height))
            frame = pygame.transform.scale(frame, ENTITY_SIZE)
            self.moving_right.append(frame)

        # Shooting tiene 2 frames
        shooting_sheet = resource_manager.load_image('teacher_shoot.png', 'teacher')
        self.shooting_frames = []
        for i in range(2):
            frame = pygame.Surface((width, height), pygame.SRCALPHA)
            frame.blit(shooting_sheet, (0, 0), (i * width, 0, width, height))
            frame = pygame.transform.scale(frame, ENTITY_SIZE)
            self.shooting_frames.append(frame)

        # Inicializar con primer frame de standing
        self.image = self.standing_frames[0]
        self.rect = self.image.get_frect(midbottom=(100, GROUND))

        self.standing_index = 0
        self.animation_index = 0
        self.animation_timer = 0
        self.animation_speed = 150  # milisegundos entre frames

        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown_duration = 500

        self.direction = 1
        self.is_moving = False
        self.is_shooting = False

        self.projectile_group = pygame.sprite.Group()
        self.camera_input_handler = camera_input_handler

        self.bullet_count = bullet_count
        self.shots_fired = 0

        self.resource_manager = resource_manager

        self.shooting_frame_count = 0
        self.shooting_max_frames = 2  # Solo los 2 frames una vez

        self.current_level = current_level

    def animate(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.animation_timer >= self.animation_speed:
            self.animation_timer = current_time
            self.animation_index = (self.animation_index + 1) % 2
            self.standing_index = (self.standing_index + 1) % 3

            if self.is_shooting:
                self.image = self.shooting_frames[self.animation_index]
                self.shooting_frame_count += 1
                if self.shooting_frame_count >= self.shooting_max_frames:
                    self.is_shooting = False
                    self.shooting_frame_count = 0
            elif self.is_moving:
                if self.direction > 0:
                    self.image = self.moving_right[self.animation_index]
                else:
                    self.image = self.moving_left[self.animation_index]
            else:
                self.image = self.standing_frames[self.standing_index]

    def shoot_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def player_input(self):
        keys = pygame.key.get_pressed()
        direction = 0
        control_mode = self.game.settings.select_controls

        # Input por cámara (solo si está en modo dynamic o both)
        if self.camera_input_handler and control_mode in ['dynamic', 'both']:
            if self.camera_input_handler.is_index_extended():
                cam_dir = self.camera_input_handler.get_direction()
                if cam_dir != 0:
                    direction = cam_dir

            if not self.camera_input_handler.is_thumb_extended() and self.can_shoot:
                self.shoot()

        # Input por teclado (solo si está en modo standard o both)
        if control_mode in ['standard', 'both']:
            if keys[K_SPACE] and self.can_shoot:
                self.shoot()

            # Control de movimiento por teclado
            if direction == 0:  # Solo si la cámara no ha establecido una dirección
                if keys[K_LEFT]:
                    direction = -1
                elif keys[K_RIGHT]:
                    direction = 1

        if direction != 0:
            self.direction = direction
            self.is_moving = True
            self.rect.x += 5 * self.direction
            # Reproducir sonido de caminar si no está sonando
            if not self.is_walking_sound_playing:
                self.walking_sound.play(-1)  # -1 para loop continuo
                self.is_walking_sound_playing = True
        else:
            self.is_moving = False
            # Detener sonido de caminar
            if self.is_walking_sound_playing:
                self.walking_sound.stop()
                self.is_walking_sound_playing = False

        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0: self.rect.left = 0

    def shoot(self):
        if self.can_shoot:
            if self.bullet_count == -1 or self.shots_fired < self.bullet_count:
                self.projectile_group.add(Projectile(
                    self.rect.midtop,
                    self.projectile_group,
                    self.resource_manager,
                    self.current_level
                ))
                self.can_shoot = False
                self.shoot_time = pygame.time.get_ticks()
                if self.bullet_count != -1:
                    self.shots_fired += 1
                self.is_shooting = True
                self.shooting_frame_count = 0  # Reiniciar el contador al disparar
                # Reproducir sonido de disparo
                self.shooting_sound.play()

    def update(self):
        self.player_input()
        self.animate()
        self.shoot_timer()

    def release(self):
        self.walking_sound.stop()