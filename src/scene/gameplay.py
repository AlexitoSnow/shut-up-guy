# Escena principal del juego
# Contiene la lógica principal del gameplay:
# spawning de enemigos, manejo de colisiones, puntuación, etc.
from math import ceil

import pygame
from pygame.locals import QUIT

from .pause import PauseScene
from ..config.constants import (
    SCREEN_WIDTH, BLACK, SCREEN_HEIGHT,
    TIMER_SIZE, TIMER_POSITION
)
from ..entity import Player, Obstacle
from .base_scene import Scene
from ..utils import Timer, CameraInput, collide_between, Text


class GameplayScene(Scene):
    def __init__(self, game, **kwargs):
        super().__init__(game)
        self.pause_scene = PauseScene(game, on_resume=self.on_resume)
        self.pause = False

        # Groups
        self.character = pygame.sprite.GroupSingle()
        self.obstacles = pygame.sprite.Group()
        self.killed_enemies = pygame.sprite.Group()

        # Timers
        self.level = kwargs.get('level')
        self.spawned_enemies = 0
        self.obstacle_timer_gen = Timer(self.level.spawn_interval * 1000, self.spawn_enemy, True)
        self.timer = Timer(self.level.time * 1000, autostart=True, reverse=True)

        # Text
        self.timer_text = Text('', 32, TIMER_POSITION)
        self.enemy_text = Text(f'x{self.level.enemy_count}', 36, (SCREEN_WIDTH - 150, 30))
        # Posicionamos el contador de balas al mismo nivel Y que el timer
        bullet_y = SCREEN_HEIGHT - TIMER_POSITION[1]
        self.bullet_text = Text('8' if self.level.bullet_count == -1 else f'x{self.level.bullet_count}', 32, (TIMER_POSITION[0] + 30, bullet_y))
        self.bullet_text_infinite = self.bullet_text.font.render('8', True, (255, 255, 255))
        self.bullet_text_infinite = pygame.transform.rotate(self.bullet_text_infinite, 90)
        self.time_count = '00:00'

        self.bullet_count = 'INFINITE'
        if self.level.bullet_count != -1: self.bullet_count = f'x{self.level.bullet_count}'

        # Input handlers - usar el índice de cámara de las configuraciones
        self.cam_handler = None
        if self.game.settings.select_controls != 'standard':
            camera_index = self.game.settings.camera_index
            self.cam_handler = CameraInput(camera_index)
            self.cam_handler.start()
            # Mostrar cámaras disponibles al inicializar
            print(f"Usando cámara con índice: {self.game.settings.camera_index}")

        self.load_images()

        # Crear player con el resource manager y el nivel actual
        self.character.add(Player(
            self.game.resources,
            self.game,
            self.cam_handler,
            self.level.bullet_count,
            self.level.number
        ))

        print(f'{self.level}')

        self.spawn_enemy()

    def update_timer_text(self):
        seconds = self.timer.get_time_in_seconds()
        # display the timer in mm:ss
        self.time_count = f'{seconds // 60:02}:{seconds % 60:02}'

    def update_bullet_remaining(self):
        remaining = '8' if self.level.bullet_count == -1 else f'x{self.character.sprite.bullet_count - self.character.sprite.shots_fired}'
        self.bullet_count = remaining

    def handle_events(self, events):
        for event in events:
            if event.type == QUIT:
                if self.cam_handler is not None: self.cam_handler.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.pause:
                    self.on_pause()
                elif event.key == pygame.K_ESCAPE and self.pause:
                    self.on_resume()
        if not self.pause:
            if self.timer.get_time_in_seconds() == self.level.time:
                self.game.change_scene('gameover', level=self.level, results=self.get_results())
                self.character.sprite.release()
        if self.level.bullet_count - self.character.sprite.shots_fired <= 0 and self.level.bullet_count != -1:
            self.game.change_scene('gameover', level=self.level, results=self.get_results())

    def get_results(self):
        return {
            'level': self.level,
            'time_remaining': self.timer.get_time_in_seconds(),
            'shots_fired': self.character.sprite.shots_fired,
            'bullet_count': self.character.sprite.bullet_count,
            'killed_enemies': len(self.killed_enemies)
        }

    def on_pause(self):
        if self.cam_handler is not None: self.cam_handler.stop()
        self.pause = True
        self.timer.pause()
        for obstacle in self.obstacles:
            obstacle.lifetime.pause()


    def on_resume(self):
        if self.cam_handler is not None: self.cam_handler.start()
        self.pause = False
        self.timer.resume()
        for obstacle in self.obstacles:
            obstacle.lifetime.resume()

    def update(self):
        if not self.pause:
            self.obstacle_timer_gen.update()
            self.timer.update()
            self.update_timer_text()
            self.character.update()
            self.character.sprite.projectile_group.update()
            self.obstacles.update()
            collide_between(self.obstacles, self.character.sprite.projectile_group, True, True, self.on_enemy_killed)
        else:
            self.pause_scene.update()

    def load_images(self):
        # Cargar y configurar el fondo según el nivel
        level_range = ceil(self.level.number / 5)
        self.background = self.game.resources.load_image(f'back_{(level_range-1)*5 + 1}_{level_range*5}.png', 'background')
        self.background = pygame.transform.scale(self.background, (800, 400))
        
        # Calcular la posición para centrar el fondo
        self.background_rect = self.background.get_rect()
        self.background_rect.centerx = SCREEN_WIDTH // 2
        self.background_rect.centery = SCREEN_HEIGHT // 2
        
        # Cargar y configurar los boards
        self.board = self.game.resources.load_image('board.png', 'background')
        self.board = pygame.transform.scale(self.board, (800, 100))
        
        # Crear los rects para los boards superior e inferior
        self.top_board_rect = self.board.get_rect()
        self.bottom_board_rect = self.board.get_rect()
        
        # Posicionar los boards
        self.top_board_rect.topleft = (0, 0)  # Board superior en la parte superior
        self.bottom_board_rect.topleft = (0, SCREEN_HEIGHT - 100)  # Board inferior 100px desde abajo

        # Cargar y configurar timer UI
        self.timer_ui = self.game.resources.load_image('timer.png', 'misc')
        self.timer_ui = pygame.transform.scale(self.timer_ui, TIMER_SIZE)
        self.timer_rect = self.timer_ui.get_rect(center=TIMER_POSITION)
        self.timer_text.position = self.timer_rect.center

        # Cargar y configurar bullet UI
        level_range = ceil(self.level.number / 5)
        bullet_image = self.game.resources.load_image(f'shoot_{(level_range-1)*5 + 1}_{level_range*5}.png', 'shoot')
        self.bullet_ui = pygame.transform.scale(bullet_image, (48, 48))  # Mitad del tamaño del timer
        bullet_y = SCREEN_HEIGHT - TIMER_POSITION[1]
        self.bullet_rect = self.bullet_ui.get_rect(center=(TIMER_POSITION[0], bullet_y))

        # Cargar y configurar el ícono de movimiento
        movement_icon = self.game.resources.load_image('movement_icon.png', 'misc')
        # Extraer los 3 frames (32x32 cada uno)
        for i in range(3):
            frame = pygame.Surface((32, 32), pygame.SRCALPHA)
            frame.blit(movement_icon, (0, 0), (i * 32, 0, 32, 32))
            frame = pygame.transform.scale(frame, (64, 64))  # Escalar a 64x64 para mejor visibilidad

    def draw(self, screen):
        screen.fill(BLACK)  # Llenar la pantalla con negro para los bordes
        screen.blit(self.background, self.background_rect)
        screen.blit(self.board, self.top_board_rect)
        screen.blit(self.board, self.bottom_board_rect)

        # Dibujar timer UI y texto
        screen.blit(self.timer_ui, self.timer_rect)
        timer_surface = self.timer_text.surf(self.time_count)
        # Centrar el texto en el área útil del timer
        timer_text_rect = timer_surface.get_rect(center=self.timer_rect.center)
        screen.blit(timer_surface, timer_text_rect)

        # Dibujar bullet UI y contador
        screen.blit(self.bullet_ui, self.bullet_rect)
        if self.level.bullet_count == -1:
            # Dibujar el 8 rotado como símbolo de infinito
            infinite_rect = self.bullet_text_infinite.get_rect(midleft=(self.bullet_rect.right + 10, self.bullet_rect.centery))
            screen.blit(self.bullet_text_infinite, infinite_rect)
        else:
            screen.blit(self.bullet_text.surf(self.bullet_count), self.bullet_text.rect)

        screen.blit(self.enemy_text.surf(f'{self.spawned_enemies}/{self.level.enemy_count}'), self.enemy_text.rect)
        self.character.draw(screen)
        self.character.sprite.projectile_group.draw(screen)
        self.obstacles.draw(screen)

        if self.pause:
            self.pause_scene.draw(screen)

    def spawn_enemy(self):
        if self.spawned_enemies < self.level.enemy_count:
            self.obstacles.add(Obstacle(
                self.game.resources,
                lifetime=self.level.enemy_lifetime * 1000,
                movement_speed=self.level.movement_speed
            ))
            self.spawned_enemies += 1
            print(f'Spawned enemies: {self.spawned_enemies}')
        else:
            self.obstacle_timer_gen.pause()

    def on_enemy_killed(self):
        self.update_bullet_remaining()
        # Agregar enemigos al grupo killed_enemies antes de que sean eliminados
        for enemy in self.obstacles:
            # Si el enemigo está muerto pero aún no ha sido contado
            if not enemy.alive() and enemy not in self.killed_enemies:
                self.killed_enemies.add(enemy)
