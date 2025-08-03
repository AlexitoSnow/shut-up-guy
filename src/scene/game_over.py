# Escena de game over
# Pantalla que se muestra cuando el jugador pierde,
# con opciones para reiniciar, volver al menú o salir
import pygame

from .base_scene import Scene
from .levels import Level
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT
from ..utils import Button, Text


class GameOverScene(Scene):
    def __init__(self, game, level: Level=None, results=None):
        super().__init__(game)
        self.game = game
        self.level = level
        self.results = results

        # Calcular score y estado de victoria
        self.score = self.calculate_score()
        self.victory = self.results['killed_enemies'] == self.level.enemy_count

        # Preparar textos
        title_text = "¡VICTORIA!" if self.victory else "GAME OVER"
        self.title = Text(title_text, 48, (SCREEN_WIDTH // 2, 150))

        # Crear textos de resultados
        score_text = f"Score: {self.score}"
        kills_text = f"Enemigos eliminados: {self.results['killed_enemies']} x 100"
        shoots_text = f"Disparos restantes: {self.results['shoots_remaining']} x 10"
        time_text = f"Tiempo restante: {self.results['time_remaining']} segundos x 10"

        y_pos = 200
        self.score_display = Text(score_text, 30, (SCREEN_WIDTH // 2, y_pos))
        self.time_display = Text(time_text, 30, (SCREEN_WIDTH // 2, y_pos + 50))
        self.kills_display = Text(kills_text, 30, (SCREEN_WIDTH // 2, y_pos + 100))
        self.shoots_display = Text(shoots_text, 30, (SCREEN_WIDTH // 2, y_pos + 150))

        # Botón de continuar
        self.resume_button = Button("Continuar", (SCREEN_WIDTH // 2, y_pos + 250), 48, self.on_tap_quit)

        # Fondo semi-transparente
        self.container_surf = pygame.Surface((600, 500))
        self.container_surf.set_alpha(200)
        self.container_surf.fill((0, 0, 0))

    def calculate_score(self):
        # Base score por enemigos eliminados
        kill_score = self.results['killed_enemies'] * 100
        # Bonus por tiempo restante
        time_bonus = self.results['time_remaining'] * 10
        # Bonus por disparos restantes
        shoot_bonus = 0 if self.level.bullet_count == -1 else self.results['shoots_remaining'] * 10

        # Score final
        return kill_score + time_bonus + shoot_bonus

    def on_tap_quit(self):
        if self.victory: self.game.progress.add_level({'number': self.level.number, f'{self.level.difficulty}': self.score})
        self.game.change_scene('levels')

    def update(self):
        cursor_type = pygame.SYSTEM_CURSOR_ARROW
        if self.resume_button.rect.collidepoint(pygame.mouse.get_pos()):
            cursor_type = pygame.SYSTEM_CURSOR_HAND
            if pygame.mouse.get_pressed()[0]:
                self.resume_button.on_tap()
                cursor_type = pygame.SYSTEM_CURSOR_ARROW
        pygame.mouse.set_cursor(cursor_type)

    def draw(self, screen):
        # Dibujar fondo semi-transparente
        screen.blit(self.container_surf, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 250))

        # Dibujar todos los textos
        screen.blit(self.title.surf(), self.title.rect)
        screen.blit(self.time_display.surf(), self.time_display.rect)
        screen.blit(self.kills_display.surf(), self.kills_display.rect)
        if self.level.bullet_count != -1: screen.blit(self.shoots_display.surf(), self.shoots_display.rect)
        screen.blit(self.score_display.surf(), self.score_display.rect)

        # Dibujar botón
        self.resume_button.draw(screen)