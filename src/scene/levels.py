import random

import pygame

from src.config import LEVEL_MAX, SCREEN_WIDTH, WHITE
from src.scene import Scene
from src.utils import Button, Text

BUTTON_WIDTH = 120
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20
BUTTONS_PER_ROW = 5

def get_button_rect(index, start_x, start_y):
    row = index // BUTTONS_PER_ROW
    col = index % BUTTONS_PER_ROW
    x = start_x + col * (BUTTON_WIDTH + BUTTON_MARGIN)
    y = start_y + row * (BUTTON_HEIGHT + BUTTON_MARGIN)
    return pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)

class LevelsScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.game = game

        # Título usando la clase Text
        self.title = Text("NIVELES", 48, (SCREEN_WIDTH // 2, 50))
        self.back_button = Button('<', (50, 50), 48, text_color=(255, 255, 0))
        self.levels = []
        for i in range(1, LEVEL_MAX + 1):
            self.levels.append(Level(i, self.game.settings.difficulty))
        self.level_buttons = []
        for i, level in enumerate(self.levels):
            rect = get_button_rect(i, 50, 100)
            button = Button(
                str(level.number),
                rect.center,
                36,
                bg_color=WHITE,
                text_color=(0, 0, 0)
            )
            self.level_buttons.append((button, level))
            print(f"{level}")  # Debug print for level details

    def update(self):
        cursor_type = pygame.SYSTEM_CURSOR_ARROW
        for button, level in self.level_buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                cursor_type = pygame.SYSTEM_CURSOR_HAND
                if pygame.mouse.get_pressed()[0]:
                    self.game.change_scene('game', level=level)
        if self.back_button.rect.collidepoint(pygame.mouse.get_pos()):
            cursor_type = pygame.SYSTEM_CURSOR_HAND
            if pygame.mouse.get_pressed()[0]:
                self.game.change_scene('menu')
        pygame.mouse.set_cursor(cursor_type)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.title.surf(), self.title.rect)
        for button, level in self.level_buttons:
            button.draw(screen)
        self.back_button.draw(screen)

class Level:
    def __init__(self, number, difficulty: str):
        """
        Initializes a level with:
        - enemy_count y time que se reinician cada 5 niveles
        - velocidad que aumenta gradualmente (0.5 por nivel)
        - lifetime que disminuye con cada nivel
        """
        self.number = number
        self.difficulty = difficulty

        # Calcular nivel base (1-5)
        self.base_level = ((number - 1) % 5) + 1

        # Calcular rango de nivel (1-5, 6-10, 11-15, etc)
        self.level_range = ((number - 1) // 5) + 1

        # Contadores base que se reinician cada 5 niveles
        # Reduciendo la progresión para que no sea tan tedioso
        self.enemy_count = 3 + (self.base_level - 1) * 4  # 3, 7, 11, 15, 19 enemigos
        self.time = 25 + (self.base_level - 1) * 8  # 25, 33, 41, 49, 57 segundos

        # La velocidad base de cada rango aumenta en 2
        # Y dentro de cada rango aumenta 0.5 por nivel
        base_speed = 5 + (self.level_range - 1) * 2.5  # Incremento más pronunciado entre rangos
        self.movement_speed = base_speed + (self.base_level - 1) * 0.5

        # El lifetime empieza alto y disminuye con cada nivel
        max_lifetime = 8  # Tiempo máximo en segundos
        lifetime_reduction = (self.base_level - 1) * 1.2  # Reducción más pronunciada
        self.enemy_lifetime = max(2, max_lifetime - lifetime_reduction)  # Mínimo 2 segundos

        # Calcular intervalo de spawn para distribuir enemigos en el tiempo disponible
        # El margen varía según el nivel para dar diferentes ritmos
        margin_time = 4 - (self.base_level - 1) * 0.5  # 4, 3.5, 3, 2.5, 2 segundos
        available_time = self.time - (2 * margin_time)
        self.spawn_interval = available_time / self.enemy_count  # distribuir uniformemente

        # Cantidad de balas según dificultad
        if difficulty == 'easy':
            self.bullet_count = -1  # infinite bullets
        elif difficulty == 'medium':
            self.bullet_count = self.enemy_count * 1.5  # 1.5 bullets per enemy
        else:
            self.bullet_count = self.enemy_count  # 1 bullet per enemy

    def __str__(self):
        return f"Level {self.number} (base {self.base_level}, range {self.level_range}): {self.enemy_count} enemies, {self.time}s, {self.bullet_count} bullets, speed {self.movement_speed:.1f}, spawn {self.spawn_interval:.1f}s, lifetime {self.enemy_lifetime:.1f}s"
